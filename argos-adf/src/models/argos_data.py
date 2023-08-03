import datetime


class ArgosData:
    def __init__(self):
        self.name = None
        self.datapoints = None
        self.step_size = None
        self.start_time = None
        self.end_time = None
        self.endpoint = None
        self.metric = None
        self.anomalies = []

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_data(self):
        return self.datapoints

    def set_data(self, datapoints):
        if self.datapoints is not None:
            if not self.check_step(datapoints):
                raise ValueError("Step size has changed")
        self.datapoints = datapoints

    def get_step(self):
        return self.step_size

    def set_step(self, step_size):
        self.step_size = step_size

    def get_start(self):
        return self.start_time

    def set_start(self, start_time):
        self.start_time = start_time

    def get_end(self):
        return self.end_time

    def set_end(self, end_time):
        self.end_time = end_time

    def get_endpoint(self):
        return self.endpoint

    def set_endpoint(self, endpoint):
        self.endpoint = endpoint

    def get_metric(self):
        return self.metric

    def set_metric(self, metric):
        self.metric = metric

    def get_anomalies(self):
        return self.anomalies

    def set_anomalies(self, anomalies):
        self.anomalies = anomalies

    def add_anomaly(self, anomaly):
        if isinstance(anomaly, dict):
            self.anomalies.append(anomaly)
        elif isinstance(anomaly, list):
            self.anomalies.extend(anomaly)
        else:
            raise TypeError("Expected anomaly to be type of list or dict")

    def check_step(self, datapoints):
        for i in range(1, len(datapoints) - 1):
            if int(datapoints[i + 1][1]) - int(datapoints[i][1]) != self.step_size:
                return False
        return True

    # def get_noised_data(self):
    #     noised_data = np.array(self.datapoints.copy())
    #     noised_data[:, 0] += np.random.normal(0, 0.1, len(self.datapoints))
    #     return noised_data

    def __repr__(self):
        return f"ArgosData: {self.metric}"

    def __len__(self):
        return len(self.datapoints)
