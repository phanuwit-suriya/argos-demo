import json
import logging.config
import os
import subprocess
import time

if __name__ == "__main__":
    try:
        with open(os.path.join("resources", "settings", "metrics.config.json"), "r", encoding="utf-8") as metrics_config_file:
            config = json.load(metrics_config_file)
    except FileNotFoundError as e:
        exit(1)

    for metric_name, metric_value in config.items():
        subprocess.run([
            # "C:\\Program Files\\nodejs\\node.exe",
            # "C:\\Users\\U6078687\\AppData\\Roaming\\npm\\node_modules\\pm2\\bin\\pm2",
            # "start",
            # "app.py",
            "pm2", "start", "app.py", "--interpreter", "python3",
            "--name", metric_name,
            "--",
            "--name", metric_name,
            "--endpoint", metric_value["endpoint"],
            "--metric", metric_value["metric"],
            "--sample-size", str(metric_value["sample_size"]),
            "--window-size", str(metric_value["window_size"]),
            "--step-size", str(metric_value["step_size"]),
            "--attempt", str(metric_value["attempt"]),
            "--alert-window-size", str(metric_value["alert_window_size"]),
            "--alert-threshold", str(metric_value["alert_threshold"]),
            "--interval", str(metric_value["interval"]),
        ])
        time.sleep(60)
