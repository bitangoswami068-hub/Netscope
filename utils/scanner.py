import requests
import socket
from urllib.parse import urlparse

def scan_site(url):
    print("\n[+] Scanning:", url)

    score = 0   # risk score

    # ------------------ Reachability ------------------
    try:
        res = requests.get(url, timeout=5)
        html = res.text.lower()
        print("[✔] Website reachable")
    except:
        print("[!] Website not reachable")
        return

    # ------------------ HTTPS ------------------
    if url.startswith("https"):
        print("[✔] HTTPS Secure")
    else:
        print("[!] Not secure (HTTP)")
        score += 1

    # ------------------ Domain & IP ------------------
    domain = urlparse(url).netloc

    try:
        ip = socket.gethostbyname(domain)
        print("[+] IP Address:", ip)
    except:
        print("[!] Could not resolve IP")

    # ------------------ Port Scan ------------------
    print("\n[+] Checking ports...")
    for port in [80, 443]:
        s = socket.socket()
        s.settimeout(1)
        if s.connect_ex((domain, port)) == 0:
            print(f"[OPEN] Port {port}")
        s.close()

    # ------------------ Suspicious URL Keywords ------------------
    keywords = ["login", "secure", "verify", "account", "bank", "free"]

    found = [k for k in keywords if k in url.lower()]
    if found:
        print(f"[!] Suspicious keywords in URL: {found}")
        score += 1

    # ------------------ Fake Login Pattern ------------------
    if "password" in html or "enter your password" in html:
        print("[!] Possible Fake Login Page detected")
        score += 2
    else:
        print("[✔] No fake login pattern detected")

    # ------------------ FINAL VERDICT ------------------
    print("\n=== FINAL RESULT ===")

    if score >= 3:
        print("🚨 DANGEROUS WEBSITE")
    elif score >= 1:
        print("⚠️ SUSPICIOUS WEBSITE")
    else:
        print("✅ SAFE WEBSITE")

    print("\n[✓] Scan Complete")
