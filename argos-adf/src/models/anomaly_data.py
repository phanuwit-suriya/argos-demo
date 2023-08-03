import time


class AnomalyData:
    def __init__(self):
        self.name = None
        self.endpoint = None
        self.metric = None
        self.algo_name = None
        self.algo_params = {}
        self.detector_name = None
        self.detector_params = {}
        self.found = None
        self.start_time = None
        self.anomalies = []
        self.prev_anomaly = None

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_endpoint(self):
        return self.endpoint

    def set_endpoint(self, endpoint):
        self.endpoint = endpoint

    def get_metric(self):
        return self.metric

    def set_metric(self, metric):
        self.metric = metric

    def get_algo_name(self):
        return self.algo_name

    def set_algo_name(self, algo_name):
        self.algo_name = algo_name

    def get_algo_params(self):
        return self.algo_params

    def set_algo_params(self, algo_params):
        self.algo_params = algo_params

    def get_detector_name(self):
        return self.detector_name

    def set_detector_name(self, detector_name):
        self.detector_name = detector_name

    def get_detector_params(self):
        return self.detector_params

    def set_detector_params(self, detector_params):
        self.detector_params = detector_params

    def get_found(self):
        return self.found

    def set_found(self, found):
        self.found = found

    def get_start_time(self):
        return self.start_time

    def set_start_time(self):
        self.start_time = time.time()

    def get_anomalies(self):
        return self.anomalies

    def set_anomalies(self, anomalies):
        self.anomalies = anomalies

    def add_anomaly(self, anomaly):
        if anomaly not in self.anomalies:
            if isinstance(anomaly, dict):
                self.anomalies.append(anomaly)
            elif isinstance(anomaly, list):
                self.anomalies.extend(anomaly)
            else:
                raise TypeError("Expected anomaly to be type of list or dict")
    
    def clear_anomaly(self):
        self.anomalies = []

    def get_prev_anomaly(self):
        return self.prev_anomaly

    def set_prev_anomaly(self, anomaly):
        self.prev_anomaly = anomaly

    def get_start(self):
        try:
            return self.anomalies[-1]["start"]
        except IndexError:
            raise

    def get_end(self):
        try:
            return self.anomalies[-1]["end"]
        except IndexError:
            raise

    def __repr__(self):
        return f"AnomalyData: {self.metric}"

    def __len__(self):
        return len(self.anomalies)
