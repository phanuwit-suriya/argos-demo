import collections
import datetime
import json
import logging
import re

import requests
from dateutil.relativedelta import relativedelta


class ContinuousGraphiteReader:

    def __init__(self, endpoint, metric, step_size, sample_size):
        self.logger = logging.getLogger(__name__)
        self.endpoint = endpoint
        self.metric = metric
        self.step_size = step_size
        self.sample_size = sample_size

    def read(self, argos_data):
        try:
            with requests.post(url=self.endpoint, data=self.payload()) as response:
                datapoints = response.json(encoding="utf-8")[0]["datapoints"]
                self.logger.info(f"HTTP response status code: {response.status_code}")
        except requests.exceptions.ConnectionError:
            self.logger.exception("Failed to connect to server")
        except ValueError:
            self.logger.exception("No response from server")
        else:
            self.logger.info("Successful request")

            while not datapoints[-1][0]:
                datapoints.pop()
            if argos_data.get_data() is not None:
                deque = collections.deque(
                    argos_data.get_data(), maxlen=len(argos_data))
                num_datapoints = 0
                for datapoint in datapoints:
                    if datapoint not in argos_data.get_data() and datapoint[0] is not None and datapoint[1] > argos_data.get_data()[-1][1]:
                        deque.append(datapoint)
                        num_datapoints += 1
                datapoints = list(deque)
            else:
                num_datapoints = len(datapoints)

            if argos_data.get_data() != datapoints:
                self.logger.info(f"{num_datapoints} new datapoint(s) found")
            else:
                self.logger.info("No new datapoint found")

            try:
                argos_data.set_data(datapoints)
            except ValueError:
                self.logger.exception("Step size has changed")
            else:
                argos_data.set_step(self.step_size )
                argos_data.set_start(datapoints[0][1])
                argos_data.set_end(datapoints[-1][1])
                argos_data.set_endpoint(self.endpoint)
                argos_data.set_metric(self.metric)

    def payload(self):
        # from_date = datetime.datetime.now() - relativedelta(seconds=self.sample_size)
        # from_date = int(from_date.timestamp())
        if "summarize" in self.metric:
            return f"target={self.metric}&from=now-{self.sample_size}&until=now-1h&format=json"
        return f"target=summarize({self.metric}, '{self.step_size // 60}minute')&from=now-{self.sample_size}&until=now-1h&format=json"
