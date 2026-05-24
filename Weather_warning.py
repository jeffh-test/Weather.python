#!/usr/bin/env python3

import requests
import time
import smtplib
from email.mime.text import MIMEText
import json
import os

# ===== CONFIG =====
CHECK_INTERVAL = 5 * 60  # 5 minute notices
RECIPIENT_EMAIL = [
     "1st users email",
     "2nd user email"
 ]

EMAIL_FROM = "The name of the server sending it."

SMTP_SERVER = "You servers IP address here."
SMTP_PORT = 25
SMTP_USER = ""
SMTP_PASS = ""

STATE_FILE = "seen_alerts.json"

# UGC County Codes (Oklahoma counties between OKC and Tulsa)
TARGET_COUNTIES = {
    "OKC143",  # Tulsa
    "OKC145",  # Wagoner
    "OKC037",  # Creek
    "OKC113",  # Osage
    "OKC117",  # Pawnee
    "OKC081",  # Lincoln
    "OKC109",  # Oklahoma
    "OKC017",  # Canadian
}

RELEVANT_EVENTS = {
    "Severe Thunderstorm Warning",
    "Severe Thunderstorm Watch",
    "Tornado Warning",
    "Tornado Watch",
    "Hail",
}

# Optional severity filter
ALLOWED_SEVERITY = {"Severe", "Extreme"}

# ===== STATE HANDLING =====
def load_seen_alerts():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def save_seen_alerts(seen):
    with open(STATE_FILE, "w") as f:
        json.dump(list(seen), f)

# ===== EMAIL =====
def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = RECIPIENT_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            if SMTP_USER and SMTP_PASS:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(EMAIL_FROM, [RECIPIENT_EMAIL], msg.as_string())
        print(f"[+] Email sent: {subject}")
    except Exception as e:
        print(f"[!] Email failed: {e}")

# ===== FETCH ALERTS =====
def fetch_alerts():
    url = "https://api.weather.gov/alerts/active?area=OK"
    headers = {
        "User-Agent": "weather-bot (herdzina.net)",
        "Accept": "application/geo+json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json().get("features", [])
    except Exception as e:
        print(f"[!] Fetch failed: {e}")
        return []

# ===== FILTER ALERTS =====
def filter_alerts(alerts):
    filtered = []

    for feature in alerts:
        props = feature.get("properties", {})
        alert_id = props.get("id")
        event = props.get("event", "")
        severity = props.get("severity", "")
        geocodes = props.get("geocode", {}).get("UGC", [])

        # Keep only county codes
        geocodes = [c for c in geocodes if c.startswith("OKC")]

        county_match = any(code in TARGET_COUNTIES for code in geocodes)
        event_match = event in RELEVANT_EVENTS
        severity_match = severity in ALLOWED_SEVERITY

        if county_match and event_match and severity_match:
            filtered.append({
                "id": alert_id,
                "event": event,
                "area": props.get("areaDesc", ""),
                "severity": severity,
                "headline": props.get("headline", ""),
                "description": props.get("description", ""),
                "instruction": props.get("instruction", ""),
                "start": props.get("onset"),
                "end": props.get("ends"),
            })

    return filtered

# ===== FORMAT =====
def format_alert(alert):
    return "\n".join([
        f"Event: {alert['event']}",
        f"Severity: {alert['severity']}",
        f"Area: {alert['area']}",
        f"Start: {alert['start']}",
        f"End: {alert['end']}",
        "",
        f"Headline: {alert['headline']}",
        "",
        f"Description:\n{alert['description']}",
        "",
        f"Instructions:\n{alert['instruction']}",
    ])

# ===== MAIN LOGIC =====
def check_severe_weather():
    seen_alerts = load_seen_alerts()
    alerts = fetch_alerts()
    relevant_alerts = filter_alerts(alerts)

    new_alerts = []

    for alert in relevant_alerts:
        if alert["id"] not in seen_alerts:
            new_alerts.append(alert)
            seen_alerts.add(alert["id"])

    if new_alerts:
        print(f"[!] {len(new_alerts)} NEW alert(s) found")

        for alert in new_alerts:
            body = format_alert(alert)
            send_email(f"[Weather Alert] {alert['event']}", body)
    else:
        print("[+] No new alerts")

    save_seen_alerts(seen_alerts)

# ===== MAIN LOOP =====

if __name__ == "__main__":
    print("[*] Starting Severe Weather Bot (Improved)...")

if __name__ == "__main__":
    print("[*] Running Severe Weather Check...")
    check_severe_weather()