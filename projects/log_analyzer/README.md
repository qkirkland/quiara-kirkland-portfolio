# Log Analyzer for Security Events

A Python script that parses server logs to detect suspicious activity and generates security reports.

## Features
- Parse server logs (e.g., auth.log, syslog)
- Detect failed logins, port scans, and other suspicious events
- Generate summary reports

## Setup
1. Install Python 3.7+
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python log_analyzer.py <path_to_log_file>`

## Usage
Customize detection rules in the script as needed. 