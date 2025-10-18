import requests
import time
import os

PROMETHEUS_URL = "http://prometheus:9090/api/v1/alerts"

while True:
    try:
        res = requests.get(PROMETHEUS_URL)
        alerts = res.json().get("data", {}).get("alerts", [])
        for alert in alerts:
            if alert["labels"]["severity"] in ["critical", "warning"]:
                print(f"Received alert: {alert['labels']['alertname']}")
                os.system("docker restart flask_api")
        time.sleep(30)
    except Exception as e:
        print(f"Error fetching alerts: {e}")
        time.sleep(30)