import sys
import requests
from urllib.parse import urlparse, urljoin

# Simple payloads for demonstration
XSS_PAYLOAD = '<script>alert(1)</script>'
SQLI_PAYLOAD = "' OR '1'='1"

# Helper to inject payload into query param
def inject_payload(url, param, payload):
    from urllib.parse import parse_qs, urlencode
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    qs[param] = payload
    new_query = urlencode(qs, doseq=True)
    return parsed._replace(query=new_query).geturl()

def scan_xss(url):
    print("[XSS] Scanning for reflected XSS...")
    parsed = urlparse(url)
    if not parsed.query:
        print("[XSS] No query parameters to test.")
        return
    params = [p.split('=')[0] for p in parsed.query.split('&')]
    for param in params:
        test_url = inject_payload(url, param, XSS_PAYLOAD)
        try:
            resp = requests.get(test_url, timeout=5)
            if XSS_PAYLOAD in resp.text:
                print(f"[!] Possible XSS vulnerability in parameter '{param}'!")
        except Exception as e:
            print(f"[XSS] Error testing {param}: {e}")

def scan_sqli(url):
    print("[SQLi] Scanning for SQL injection...")
    parsed = urlparse(url)
    if not parsed.query:
        print("[SQLi] No query parameters to test.")
        return
    params = [p.split('=')[0] for p in parsed.query.split('&')]
    for param in params:
        test_url = inject_payload(url, param, SQLI_PAYLOAD)
        try:
            resp = requests.get(test_url, timeout=5)
            errors = [
                'You have an error in your SQL syntax',
                'Warning: mysql_',
                'unclosed quotation mark',
                'quoted string not properly terminated',
            ]
            if any(e in resp.text for e in errors):
                print(f"[!] Possible SQL injection in parameter '{param}'!")
        except Exception as e:
            print(f"[SQLi] Error testing {param}: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python web_vuln_scanner.py <url>")
        return
    url = sys.argv[1]
    if not url.startswith('http'):
        url = 'http://' + url
    print(f"Scanning {url}...")
    scan_xss(url)
    scan_sqli(url)
    print("Scan complete.")

if __name__ == "__main__":
    main() 