import sys
import re
from collections import Counter

def parse_log(file_path):
    entries = []
    with open(file_path, 'r', errors='ignore') as f:
        for line in f:
            entries.append(line.strip())
    return entries

def detect_failed_logins(log_entries):
    failed = [line for line in log_entries if 'Failed password' in line or 'authentication failure' in line]
    return failed

def detect_port_scans(log_entries):
    scan_regex = re.compile(r'port scan|nmap|masscan', re.IGNORECASE)
    scans = [line for line in log_entries if scan_regex.search(line)]
    return scans

def generate_report(failed_logins, port_scans):
    print("\n--- Security Event Report ---")
    print(f"Failed login attempts: {len(failed_logins)}")
    if failed_logins:
        users = [re.search(r'user (\w+)', l) for l in failed_logins]
        users = [m.group(1) for m in users if m]
        if users:
            print("Most targeted users:", Counter(users).most_common(3))
    print(f"Port scan events: {len(port_scans)}")
    if port_scans:
        print("Sample scan log:", port_scans[0])
    print("----------------------------\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python log_analyzer.py <path_to_log_file>")
        return
    file_path = sys.argv[1]
    log_entries = parse_log(file_path)
    failed_logins = detect_failed_logins(log_entries)
    port_scans = detect_port_scans(log_entries)
    generate_report(failed_logins, port_scans)

if __name__ == "__main__":
    main() 