import argparse
import logging.config
import os
import time

import matplotlib as plt
plt.use("agg")

from algorithms import DiscordDiscovery, ModifiedDiscordDiscovery
from detectors import LatestDiscordAttempt, ModifiedLatestDiscordAttempt
from inputs import ContinuousGraphiteReader
from models import AnomalyData, ArgosData
from outputs import EmailOutput, ImageWriter


if __name__ == "__main__":
    """The top-level module to serve as the entry point

    This module parses the command-line arguments and handles the top-level initiations accordingly.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str)
    parser.add_argument("--endpoint", type=str)
    parser.add_argument("--metric", type=str)
    parser.add_argument("--sample-size", type=int)
    parser.add_argument("--window-size", type=int)
    parser.add_argument("--step-size", type=int)
    parser.add_argument("--attempt", type=int)
    parser.add_argument("--alert-window-size", type=int)
    parser.add_argument("--alert-threshold", type=int)
    parser.add_argument("--interval", type=int)
    args = parser.parse_args()

    try:
        os.makedirs(os.path.join("resources", "logs"))
    except FileExistsError:
        pass

    logging_config = os.path.join("resources", "settings", "logging.config.conf")
    error_file = os.path.join("resources", "logs", f"{args.name}-err.log")
    log_file = os.path.join("resources", "logs", f"{args.name}-out.log")

    try:
        logging.config.fileConfig(logging_config, defaults={"errorfilename": error_file, "logfilename": log_file})
    except ValueError:
        logging.config.fileConfig(logging_config, defaults={"errorfilename": error_file.replace("\\", "\\\\"), "logfilename": log_file.replace("\\", "\\\\")})

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    logger.info(f"{args.name} process has started")

    argos_data = ArgosData()
    argos_data.set_name(args.name)

    anomaly_data = AnomalyData()
    anomaly_data.set_name(args.name)

    writer = ImageWriter()
    email_sender = EmailOutput()
    algorithm = ModifiedDiscordDiscovery(
        window_size=args.window_size // args.step_size
    )
    detector = ModifiedLatestDiscordAttempt(
        algorithm=algorithm,
        attempt=args.attempt,
        alert_window_size=args.alert_window_size,
        alert_threshold=args.alert_threshold
    )
    reader = ContinuousGraphiteReader(
        endpoint=args.endpoint,
        metric=args.metric,
        step_size=args.step_size,
        sample_size=args.sample_size
    )

    while True:
        try:
            logger.info("Start pulling data from server....")
            reader.read(argos_data)

            logger.info("Detecting anomaly....")
            detector.fit(argos_data, anomaly_data)

            logger.info("Writing image(s)....")
            image_file = writer.write(argos_data, anomaly_data)

            if image_file is not None:
                logger.info("Sending email(s)....")
                email_sender.send(anomaly_data, image_file)

        except Exception as e:
            logger.critical(e, exc_info=True)
        else:
            time.sleep(args.interval)
