# Weather Alert Automation Script (Python)

Python-based weather monitoring script that sends alerts for severe weather conditions such as thunderstorms, severe thunderstorms, tornado warnings, and hail events using weather data sources and SMTP email notifications.

---

## Features

- Monitors severe weather conditions using weather API data sources
- Detects: thunderstorms, severe thunderstorms, tornado warnings, hail events
- Sends automated email alerts via SMTP (Postfix compatible)
- Configurable geographic targeting by county or region
- Designed for scheduled execution (cron-friendly Linux automation)

---

## How It Works

1. Fetch weather data from external API source
2. Parse and evaluate current weather conditions
3. Compare conditions against severe weather thresholds
4. Trigger alert logic if conditions match defined rules
5. Send notification via SMTP email server

---
This currently runs on a AlmaLinux server. Your results may very.

## Configuration

### Location Settings
Update the county/region list inside the script to match your location.

Example:
- Tulsa County, OK
- Oklahoma County, OK

---

### SMTP Setup
This script supports any SMTP-compatible mail server.

Recommended setup:
- SMTP_HOST = localhost
- SMTP_PORT = 25
- Mail system: Postfix (recommended for Linux environments)

---

## Requirements

- Python 3.x
- Internet access for weather API requests
- SMTP server (Postfix recommended)
- Python libraries:
  - requests
  - smtplib

---

## Usage Notes

This script is intended for educational and personal automation use.

Before running:

- Configure target counties or regions
- Ensure SMTP settings are properly configured
- Validate weather data source availability

---

## Example Output

Severe Weather Alert:
- Tornado Warning detected in Tulsa County
- Email notification sent to admin@example.com

---

## Automation Example (Cron Job)

Run every 10 minutes:

*/10 * * * * /usr/bin/python3 weather.py

---

## Disclaimer

This script is provided as-is without guarantees of accuracy or reliability.
Weather data should always be verified through official sources for safety-critical decisions.

---

## Author

Jeff Herdzina  
Linux Systems Engineer / Infrastructure Automation  
