import logging

import numpy as np

from .abc_detector import AbstractDetector


class ModifiedLatestDiscordAttempt(AbstractDetector):

    def __init__(self, algorithm, attempt, alert_window_size, alert_threshold):
        self.logger = logging.getLogger(__name__)
        
        self.algorithm = algorithm
        self.attempt = attempt
        self.alert_window_size = alert_window_size
        self.alert_threshold = alert_threshold 

    def fit(self, argos_data, anomaly_data):
        datapoints = np.array(argos_data.get_data(), dtype=np.float32)

        anomaly_data.clear_anomaly()
        anomaly_data.set_start_time()
        anomaly_data.set_endpoint(argos_data.get_endpoint())
        anomaly_data.set_metric(argos_data.get_metric())
        
        alert_window_size = datapoints[-1][1] - self.alert_window_size
        is_found = False
        attempt = 0
        while not is_found:
            if attempt >= self.attempt:
                break
            anomalies = anomaly_data.get_anomalies()
            anomaly = self.algorithm.fit(datapoints, anomalies)
            anomaly_data.add_anomaly(anomaly)
            if anomaly["end"] > alert_window_size:
                prev_anomaly = anomaly_data.get_prev_anomaly()
                if prev_anomaly is not None:
                    if anomaly["end"] - prev_anomaly["end"] > self.alert_threshold:
                        anomaly_data.set_prev_anomaly(anomaly)
                        is_found = True
                else:
                    anomaly_data.set_prev_anomaly(anomaly)
                    is_found = True
            attempt += 1

        if is_found:
            self.logger.info("Anomaly(s) found")
        else:
            self.logger.info("Anomaly(s) not found")
        
        anomaly_data.set_found(is_found)
        anomaly_data.set_algo_name(type(self.algorithm).__name__)
        anomaly_data.set_algo_params({
            "sub_window_size": self.algorithm.get_window_size()
        })
        anomaly_data.set_detector_name(ModifiedLatestDiscordAttempt.__name__)
        anomaly_data.set_detector_params({
            "alert_window_size": self.alert_window_size,
            "alert_threshold": self.alert_threshold,
            "n_attempt": attempt,
            "max_attempt": self.attempt
        })
        
        return anomaly_data
