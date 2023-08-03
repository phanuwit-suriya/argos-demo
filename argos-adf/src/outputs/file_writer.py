import json
import os

import numpy as np

from helper import timestamp_to_datetime


class FileWriter:

    def __init__(self, encoding="utf-8", _format="json"):
        self.encoding = encoding
        self.format = _format

    def write(self, argos_data):
        filename = (
            f"{argos_data.get_metric()}."
            f"{timestamp_to_datetime('%Y%m%d%H%M%S', argos_data.get_start())}-"
            f"{timestamp_to_datetime('%Y%m%d%H%M%S', argos_data.get_end())}"
            f".{self.format}"
        )
        with open(os.path.join("resources", "datasets", filename), "w", encoding=self.encoding) as outfile:
            json_data = {
                "data": argos_data.get_data(),
                "step": argos_data.get_step(),
                "start": argos_data.get_start(),
                "end": argos_data.get_end(),
                "source": {
                    "endpoint": argos_data.get_endpoint(),
                    "metric": argos_data.get_metric(),
                },
                "anomaly": argos_data.get_anomaly(),
            }
            json.dump(json_data, outfile, indent=4, default=self._default)

    def _default(self, obj):
        if isinstance(obj, (np.int64, np.int32, np.int16, np.int8, np.int)):
            return int(obj)
        elif isinstance(obj, (np.float64, np.float32, np.float)):
            return float(obj)
        elif isinstance(obj, (np.array)):
            return list(obj)
        else:
            raise TypeError
