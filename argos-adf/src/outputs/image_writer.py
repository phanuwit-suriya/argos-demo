import datetime
import json
import logging
import os
import sys

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from helper import data_parser, epoch_to_datetime, timestamp_to_datetime


class ImageWriter:

    def __init__(self, figsize=None, margins=None, grid=None):
        self.logger = logging.getLogger(__name__)

        try:
            with open(os.path.join("resources", "settings", "figure.config.json"), "r", encoding="utf-8") as figure_config_file:
                figure_config = json.load(figure_config_file)
        except FileNotFoundError:
            self.logger.exception("figure.config.json not found")
            sys.exit(1)

        if figsize is not None:
            fig = plt.figure(figsize=figsize)
        else:
            figsize = figure_config["figsize"]
            width = figsize["width"]
            height = figsize["height"]
            fig = plt.figure(figsize=(width, height))

        if margins is not None:
            self.margins = margins
        else:
            margins = figure_config["margins"]
            self.margins = (margins["x"], margins["y"])

        if grid is not None:
            self.grid = grid
        else:
            self.grid = figure_config["grid"]

        fig.subplots_adjust(
            left=figure_config["subplots_adjust"]["left"],
            bottom=figure_config["subplots_adjust"]["bottom"],
            right=figure_config["subplots_adjust"]["right"],
            top=figure_config["subplots_adjust"]["top"]
        )

        self.ax = fig.add_subplot(1, 1, 1)

    def write(self, argos_data, anomaly_data):
        timestamps, values = data_parser(argos_data.get_data())
        timestamps = [datetime.datetime.fromtimestamp(int(timestamp)) for timestamp in timestamps]

        metric_directory = os.path.join("resources", "images", argos_data.get_name())
        try:
            os.makedirs(metric_directory)
        except FileExistsError:
            pass

        if anomaly_data.get_found():
            image_file = os.path.join(metric_directory, timestamp_to_datetime("%Y%m%d_%H%M", anomaly_data.get_start_time()))
            [anomaly] = anomaly_data.get_anomalies()[-1:]
            self.ax.plot(timestamps, values)
            self.configure_ax()
            self.ax.axvspan(
                epoch_to_datetime(anomaly["start"]),
                epoch_to_datetime(anomaly["end"]),
                facecolor="tab:red",
                alpha=0.3
            )
            self.ax.set_title(
                f"{anomaly_data.get_metric()}\n"
                f"{anomaly_data.get_algo_name()}(sub_window_size={str(anomaly_data.get_algo_params()['sub_window_size'] * argos_data.get_step())})\n"
                f"{anomaly_data.get_detector_name()}({', '.join(f'{key}={val}' for key, val in anomaly_data.get_detector_params().items())})",
                fontsize=10
            )
            self.logger.info(f"Saved image: {image_file}")
            plt.savefig(image_file)
            plt.cla()
            return f"{image_file}.png"
        else:
            image_folder = os.path.join(metric_directory, f"a{timestamp_to_datetime('%Y%m%d_%H%M', anomaly_data.get_start_time())}")
            try:
                os.makedirs(image_folder)
            except FileExistsError:
                pass

            for idx, anomaly in enumerate(anomaly_data.get_anomalies()):
                image_file = os.path.join(image_folder, f"a{timestamp_to_datetime('%Y%m%d_%H%M', anomaly_data.get_start_time())}_{str(idx + 1)}")
                self.ax.plot(timestamps, values)
                self.configure_ax()
                self.ax.axvspan(
                    xmin=epoch_to_datetime(anomaly["start"]),
                    xmax=epoch_to_datetime(anomaly["end"]),
                    facecolor="tab:blue",
                    alpha=0.3
                )
                self.ax.set_title(
                    f"{anomaly_data.get_metric()}\n"
                    f"{anomaly_data.get_algo_name()}(sub_window_size={str(anomaly_data.get_algo_params()['sub_window_size'] * argos_data.get_step())}\n"
                    f"{anomaly_data.get_detector_name()}({', '.join(f'{key}={val}' for key, val in anomaly_data.get_detector_params().items())})-attemp#={idx + 1}",
                    fontsize=10
                )
                self.logger.info(f"Saved image: {image_file}")
                plt.savefig(image_file)
                plt.cla()
        return None

    def configure_ax(self):
        self.ax.grid(self.grid)
        self.ax.margins(*self.margins)
        self.ax.set_ylim([0, None])
        self.ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.setp(self.ax.xaxis.get_majorticklabels(), rotation=45, ha="right")
