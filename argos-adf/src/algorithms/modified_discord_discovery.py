import logging
import sys
import time

import numpy as np

from .abc_algorithm import AbstractAlgorithm


class ModifiedDiscordDiscovery(AbstractAlgorithm):

    def __init__(self, window_size, null_as_zero=False):
        self.logger = logging.getLogger(__name__)
        self.window_size = window_size
        self.null_as_zero = null_as_zero

    def fit(self, datapoints, anomalies):
        # Axes understanding
        #   0-axis : ax running vertically downwards across rows
        #   1-axis : ax running horizontally across columns
        #   2-axis : ax running horizontally through all windows or length of windows
        r_stride, c_stride = datapoints.strides
        rows, cols = datapoints.shape
        shape = rows - self.window_size + 1, self.window_size, cols
        strides = r_stride, r_stride, c_stride

        # Create windows from given datapoints
        windows = np.lib.stride_tricks.as_strided(
            x=datapoints,
            shape=shape,
            strides=strides,
            writeable=False
        )

        # if null_as_zero is true, replace all nans with zeros
        if self.null_as_zero:
            windows[np.isnan(windows)] = 0

        # Skip windows contain datapoint(s) overlapping with datapoint(s) in anomaly(s)
        for anomaly in anomalies:
            windows = windows[
                (windows[:, -1, 1] <= anomaly["start"]) |
                (windows[:, 0, 1] >= anomaly["end"])
            ]

        # for i in range(windows.shape[1]):
        #     windows = windows[~np.isnan(windows[:,  i, 0])]
        # windows = windows[~np.any(np.isnan(windows), axis=(1, 2))]

        minimums = []
        for i, window in enumerate(windows):
            # minuend: target window
            # subtrahends: all windows excluding target window
            minuend = window
            if i < self.window_size:
                subtrahends = windows[i + self.window_size:]
            else:
                subtrahends = np.append(
                    windows[0:i - self.window_size + 1],
                    windows[i + self.window_size:],
                    axis=0
                )

            # Check if target window contains nan(s)
            if not np.any(np.isnan(minuend), axis=(0, 1)):
                # Boolean array to select non-nan windows
                #   1. Check each window whether it contains nan(s) or not
                #   2. If window contains nan(s) set it to false otherwise true
                #   3. Select windows with true value
                subtrahends = subtrahends[~np.any(np.isnan(subtrahends), axis=(1, 2))]

                # Try appending list of minimum value, start timestamp, and end timestamp to minimums list
                try:
                    minimums.append([
                        np.min(np.sum(np.abs(minuend[:, 0] - subtrahends[:, :, 0]), axis=1)),
                        minuend[0][1],
                        minuend[-1][1]
                    ])
                except ValueError:
                    self.logger.exception("Not enough windows to calculate")
                    sys.exit(1)

        # Select latest found anomaly
        [anomaly] = [
            {"start": start, "end": end}
            for idx, (minimum, start, end) in enumerate(minimums)
            if minimum == np.max(np.array(minimums)[:, 0])
        ][-1:]

        return anomaly

    def get_window_size(self):
        return self.window_size

    def set_window_size(self, window_size):
        self.window_size = window_size
