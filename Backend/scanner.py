import requests
import nmap

# Scan open ports
def scan_ports(domain):
    nm = nmap.PortScanner()
    nm.scan(domain, '1-1024')  # Scans ports 1-1024
    open_ports = [port for port in nm[domain]['tcp'] if nm[domain]['tcp'][port]['state'] == 'open']
    return {"open_ports": open_ports}

# Check missing security headers
def check_http_headers(url):
    try:
        response = requests.get(url)
        headers = response.headers
        missing_headers = [h for h in ["Content-Security-Policy", "X-Frame-Options"] if h not in headers]
        return {"missing_headers": missing_headers}
    except:
        return {"error": "Unable to fetch headers"}

# Test for SQL Injection vulnerability
def test_sql_injection(url):
    payload = "' OR '1'='1"
    try:
        response = requests.get(url + payload)
        if "error" in response.text.lower() or "syntax" in response.text.lower():
            return {"sql_injection_vulnerable": True}
    except:
        return {"error": "Could not test SQL Injection"}
    
    return {"sql_injection_vulnerable": False}
