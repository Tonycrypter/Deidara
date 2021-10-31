import json
import requests
import threading


def subdomain_brute():
    domain = input("Please Enter the domain to be scanned: Example: test.com ")
    file = open("subdomains.txt")
    content = file.read()
    subdomains = content.splitlines()
    discovered_subdomains = []
    for subdomain in subdomains:
        url = f"https://{subdomain}.{domain}"
        try:
            requests.get(url)
        except requests.ConnectionError:
            pass
        else:
            d1 = {'subdomain': url}
            print (d1)
            discovered_subdomains.append(url)


threads = []

for _ in range(1):
    t = threading.Thread(target=subdomain_brute)
    t.start()
    threads.append(t)

for thread in threads:
    thread.join()
