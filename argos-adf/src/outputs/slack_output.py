import asyncio
import json
import logging
import os
import sys

import slack


class SlackOutput:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            with open(os.path.join("resources", "settings", "slack.config.json"), "r", encoding="utf-8") as slack_config_file:
                slack_config = json.load(slack_config_file)
        except FileNotFoundError:
            self.logger.exception("slack.config.json not found")
            sys.exit(1)

        self.client = slack.WebClient(token=slack_config["SLACK_TOKEN"])
        self.channel = slack_config["SLACK_CHANNEL"]

        self.loop = asyncio.get_event_loop()

    def send(self, anomaly_data, img_path):
        message = (
            f"*Name:*\t{'ANOMALY NAME'}\n"
            f"*Anomaly:*\t{'ANOMALY START'} to {'ANOMALY END'}\n"
            f"*Metric:*\t{'ANOMALY METRIC'}\n"
            f"*Feedback:*\t{'ANOMALY FEEDBACK'}"
        )

        self.send_message(message)
        self.send_file(img_path)

    def send_message(self, _text):
        response = self.loop.run_until_complete(
            self.client.chat_postMessage(
                channel=self.channel,
                text=_text,
            ))

        assert response["ok"]
        assert response["message"]["text"] == _text

    def send_file(self, _file):
        response = self.loop.run_until_complete(
            self.client.files_upload(
                channels=self.channel,
                file=_file,
            ))

        assert response["ok"]
