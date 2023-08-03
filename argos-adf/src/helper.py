import datetime
import json
import os
import time

import jsonschema
import matplotlib.pyplot as plt
from jsonschema.exceptions import SchemaError, ValidationError


class Timer:
    def __init__(self):
        self.start = None
        self.end = None

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.end = time.time()
        print(f"Total time taken: {self.duration()}")

    def duration(self):
        return f"{str((self.end - self.start) * 1000)} milliseconds"


def data_parser(data):
    w, t = list(map(list, zip(*data)))
    return t, w


def plot_from_file(filepath, show_anomaly=False):
    try:
        with open(os.path.join("resources", "settings", "schema.config.json"), "r", encoding="utf-8") as schema_config_file:
            schema = json.load(schema_config_file)
    except FileNotFoundError as e:
        print(e)

    try:
        with open(os.path.join("resources", "settings", "figure.config.json"), "r", encoding="utf-8") as figure_config_file:
            figure_config = json.load(figure_config_file)
    except FileNotFoundError as e:
        print(e)

    try:
        with open(filepath, "r", encoding="utf-8") as data_file:
            json_data = json.load(data_file)
    except FileNotFoundError as e:
        print(e)

    try:
        jsonschema.validate(json_data, schema)
    except (ValidationError, SchemaError) as e:
        print(e)

    timestamps, values = data_parser(json_data["data"])
    timestamps = [datetime.datetime.fromtimestamp(int(timestamp)) for timestamp in timestamps]
    plt.figure(figsize=(figure_config["figsize"]["width"],
                        figure_config["figsize"]["height"]))
    plt.subplots_adjust(left=figure_config["subplots_adjust"]["left"],
                        bottom=figure_config["subplots_adjust"]["bottom"],
                        right=figure_config["subplots_adjust"]["right"],
                        top=figure_config["subplots_adjust"]["top"])
    plt.plot(timestamps, values)
    if show_anomaly:
        for _, anomaly in enumerate(json_data["anomaly"]):
            plt.axvspan(xmin=datetime.datetime.fromtimestamp(anomaly["start"]),
                        xmax=datetime.datetime.fromtimestamp(anomaly["end"]),
                        facecolor="tab:red",
                        alpha=0.3)
    plt.margins(figure_config["margins"]["x"], figure_config["margins"]["y"])
    plt.grid(figure_config["grid"])
    plt.show()


def epoch_to_datetime(epoch):
    return datetime.datetime.fromtimestamp(int(epoch))


def timestamp_to_datetime(format, timestamp):
    return time.strftime(format, time.localtime(timestamp))
