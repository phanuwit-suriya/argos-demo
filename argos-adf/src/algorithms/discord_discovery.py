import logging

import numpy as np

from .abc_algorithm import AbstractAlgorithm


class DiscordDiscovery(AbstractAlgorithm):

    def __init__(self, window_size):
        self.logger = logging.getLogger(__name__)
        self.window_size = window_size

    def fit(self, datapoints):
        windows = np.lib.stride_tricks.as_strided(
            datapoints,
            shape=(len(datapoints) - self.window_size + 1, self.window_size),
            strides=(datapoints.strides[0], datapoints.strides[0])
        )

        minimums = []
        for i in range(len(windows)):
            minuend = windows[i]
            if i < self.window_size:
                subtrahend = windows[i + self.window_size:]
            else:
                subtrahend = np.append(
                    windows[0:i - self.window_size + 1],
                    windows[i + self.window_size:],
                    axis=0
                )
            differences = minuend - subtrahend
            absolutes = np.abs(differences)
            summations = np.sum(absolutes, axis=1)
            minimum = np.min(summations)
            minimums.append(minimum)

        timestamps = list(zip(minimums, datapoints[:, 1]))

        [anomaly] = [
            {
                "start": datapoints[idx][1],
                "end": datapoints[idx + self.window_size - 1][1]
            }
            for idx, val in enumerate(timestamps)
            if val[0] == np.max(np.array(minimums))
        ][-1:]

        return anomaly

    def get_window_size(self):
        return self.window_size

    def set_window_size(self, window_size):
        self.window_size = window_size
