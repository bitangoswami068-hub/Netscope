import requests
import socket
from urllib.parse import urlparse

def scan_site(url):
    print("\n[+] Scanning:", url)

    try:
        requests.get(url, timeout=5)
        print("[✔] Website reachable")
    except:
        print("[!] Website not reachable")
        return

    if url.startswith("https"):
        print("[✔] HTTPS Secure")
    else:
        print("[!] Not secure (HTTP)")

    domain = urlparse(url).netloc

    try:
        ip = socket.gethostbyname(domain)
        print("[+] IP Address:", ip)
    except:
        print("[!] Could not resolve IP")

    print("\n[+] Checking ports...")
    for port in [80, 443]:
        s = socket.socket()
        s.settimeout(1)
        if s.connect_ex((domain, port)) == 0:
            print(f"[OPEN] Port {port}")
        s.close()

    print("\n[✓] Scan Complete")
