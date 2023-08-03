import json
import logging
import os
import sys

import jsonschema


class FileReader:

    def __init__(self, filepath, encoding="utf-8"):
        self.logger = logging.getLogger(__name__)

        try:
            with open(os.path.join("resources", "settings", "schema.config.json"), "r", encoding=encoding) as schema_file:
                self.schema = json.load(schema_file)
        except FileNotFoundError:
            self.logger.exception("schema.config.json not found")
            sys.exit(1)

        try:
            with open(filepath, "r", encoding=encoding) as input_file:
                self.json_data = json.load(input_file)
        except FileNotFoundError:
            self.logger.error(f"{filepath} not found")

    def read(self, argos_data):
        try:
            jsonschema.validate(self.json_data, self.schema)
        except jsonschema.ValidationError as e:
            self.logger.error(e, exc_info=True)
        except jsonschema.SchemaError as e:
            self.logger.error(e, exc_info=True)

        argos_data.set_data(self.json_data["data"])
        argos_data.set_step(self.json_data["step"])
        argos_data.set_start(self.json_data["start"])
        argos_data.set_end(self.json_data["end"])
        argos_data.set_endpoint(self.json_data["source"]["endpoint"])
        argos_data.set_metric(self.json_data["source"]["metric"])
        argos_data.set_anomaly(self.json_data["anomaly"])

        return argos_data
