import datetime
import json
import logging

import requests


class ConstantGraphiteReader:

    def __init__(self, endpoint, metric, step_size, from_date, until_date):
        self.logger = logging.getLogger(__name__)
        self.endpoint = endpoint
        self.metric = metric
        self.step_size = step_size
        self.from_date = from_date
        self.until_date = until_date

    def read(self, argos_data):
        try:
            with requests.post(url=self.endpoint, data=self.payload()) as response:
                datapoints = response.json(encoding="utf-8")[0]["datapoints"]
                self.logger.info(f"Response status code: {response.status_code}")
        except ValueError:
            self.logger.exception("No response from server")
        else:
            self.logger.info("Successful response")
            argos_data.set_data(datapoints)
            argos_data.set_step(self.step_size)
            argos_data.set_start(datapoints[0][1])
            argos_data.set_end(datapoints[-1][1])
            argos_data.set_endpoint(self.endpoint)
            argos_data.set_metric(self.metric)

    def payload(self):
        return f"target=summarize({self.metric}, '{self.step_size // 60}minute')&from={self.from_date}&until={self.until_date}&format=json"
