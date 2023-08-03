import numpy as np

from detectors.abc_detector import AbstractDetector


class NaiveDiscord(AbstractDetector):
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def fit(self, argos_data, anomaly_data):
        window = np.array(argos_data.get_data(), dtype=np.float)
        for anomaly in argos_data.get_anomalies():
            window = window[(window[:, 1] < anomaly["start"]) | (window[:, 1] > anomaly["end"])]
        window[np.isnan(window)] = 0

        anomaly = self.algorithm.find_anomaly(window)
        anomaly_data.add_anomaly(anomaly)

        return anomaly_data
