import json
import logging
import os
import smtplib
import sys
from collections import OrderedDict
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import urlencode

import requests

from helper import epoch_to_datetime


class EmailOutput:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            with open(os.path.join("resources", "settings", "email.config.json"), "r", encoding="utf-8") as email_config_file:
                email_config = json.load(email_config_file)
        except FileNotFoundError:
            self.logger.exception("email.config.json not found")
            sys.exit(1)

        self.host = email_config["HOST"]
        self.port = email_config["PORT"]

        self.api_endpoint = email_config["API_ENDPOINT"]
        self.api_port = email_config["API_PORT"]

        self.sender_email = email_config["SENDER_EMAIL"]
        self.sender_password = email_config["SENDER_PASSWORD"]
        self.recipient_emails = email_config["RECIPIENT_EMAILS"]
        self.message_subject = email_config["MESSAGE_SUBJECT"]
        self.message_body = email_config["MESSAGE_BODY"]

        self.hostname = os.popen(
            "env | grep HOSTNAME | cut -d '=' -f2").read().strip()
        self.addresses = os.popen(
            "env | grep HOSTADDRESS | cut -d '=' -f 2").read().strip(" ,\n")
        self.hostaddress = os.popen(
            "env | grep HOSTADDRESS | sed 's/ *$/ /' | cut -d '=' -f 2 | cut -d ' ' -f 1").read().strip(",\n")
        self.container_address = os.popen(
            "env | grep HOSTADDRESS | sed 's/ *$/ /' | cut -d ' ' -f 2 | cut -d ' ' -f 2").read().strip(",\n")
        self.container_id = os.popen(
            "cat /proc/self/cgroup | grep '\\/docker\\/' | head -n 1 | sed 's/.*\\/docker\\///'").read().strip()
        self.container_name = os.popen(
            "env | grep DOCKERNAME | cut -d '=' -f2").read().strip()

    def send(self, anomaly_data, image_path=None):
        permission = True
        feedback_url = "/api/metric"
        try:
            with requests.get(f"{self.api_endpoint}:{self.api_port}/api/metric/{anomaly_data.get_name()}") as response:
                if response.json()["found"]:
                    with requests.get(f"{self.api_endpoint}:{self.api_port}/api/permission?{get_uri(anomaly_data)}") as response_true:
                        self.logger.info(f"Request {anomaly_data.get_name()} permission from server.")
                        permission = response_true.json()["permission"]
                        feedback_url = response_true.json()["feedback_url"]
                else:
                    with requests.post(f"{self.api_endpoint}:{self.api_port}/api/metric", data=get_payload(anomaly_data)) as response_false:
                        self.logger.info(f"Register {anomaly_data.get_name()} to permission server.")
                        permission = response_false.json()["created"]
                        feedback_url = response_false.json()["feedback_url"]
        except requests.exceptions.ConnectionError:
            self.logger.exception("No response from server")

        if permission:
            message = MIMEMultipart("related")
            message["Subject"] = self.message_subject.format(name=anomaly_data.get_name())
            message["From"] = self.sender_email  # Can also be sender name

            message_alt = MIMEMultipart("alternative")
            message.attach(message_alt)
            try:
                message_text = MIMEText(
                    self.message_body.format(
                        name=anomaly_data.get_name(),
                        hostname=self.hostname,
                        hostaddress=self.addresses,
                        container_id=self.container_id,
                        container_name=f"({self.container_name})" if self.container_name else "",
                        start=epoch_to_datetime(anomaly_data.get_start()),
                        end=epoch_to_datetime(anomaly_data.get_end()),
                        endpoint=anomaly_data.get_endpoint(),
                        metric=anomaly_data.get_metric(),
                        uri=f"{self.hostaddress}:{self.api_port}{feedback_url}"
                    ),
                    "html"
                )
            except Exception:
                message_text = MIMEText(
                    self.message_body.format(
                        name=anomaly_data.get_name(),
                        hostname=self.hostname,
                        hostaddress=self.addresses,
                        container_id=self.container_id,
                        container_name="(" + self.container_name + ")" if self.container_name else "",
                        start=epoch_to_datetime(anomaly_data.get_start()),
                        end=epoch_to_datetime(anomaly_data.get_end()),
                        endpoint=anomaly_data.get_endpoint(),
                        metric=anomaly_data.get_metric()
                    ),
                    "html"
                )
            message_alt.attach(message_text)

            with open(image_path, "rb") as image_file:
                message_img = MIMEImage(image_file.read())
                message_img.add_header("Content-ID", "<plot>")
                message.attach(message_img)

            with smtplib.SMTP(host=self.host, port=self.port) as server:
                for recipient_email in self.recipient_emails:
                    message["To"] = recipient_email
                    self.logger.info(f"Sent message to {recipient_email}")
                    server.sendmail(self.sender_email, recipient_email, message.as_string())


def get_uri(anomaly_data):
    return urlencode(OrderedDict({"name": anomaly_data.get_name(), "start": anomaly_data.get_start(), "end": anomaly_data.get_end()}))


def get_payload(anomaly_data):
    return {"name": anomaly_data.get_name(), "start": anomaly_data.get_start(), "end": anomaly_data.get_end()}
