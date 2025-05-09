import sys

# Placeholder for scanning functions
def scan_xss(url):
    pass  # TODO: Implement XSS scanning

def scan_sqli(url):
    pass  # TODO: Implement SQLi scanning

def main():
    if len(sys.argv) < 2:
        print("Usage: python web_vuln_scanner.py <url>")
        return
    url = sys.argv[1]
    # TODO: Call scan_xss and scan_sqli, print results

if __name__ == "__main__":
    main() 