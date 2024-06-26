#!/usr/bin/env python3

from shared_lib import wrapped_requests

import json
import os
import random

import concurrent.futures

PROXY_LIST_URL = "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies.json"

SOURCES_PATH = os.path.join("sources", "sources.json")
SOURCES = json.load(open(SOURCES_PATH))

NEED_PROXY_PATH = os.path.join("sources", "need-proxy.json")
NEED_PROXY = json.load(open(NEED_PROXY_PATH))

proxy_list = []
working_proxies = []

print("[+] Loading proxy list from remote")
remote_proxy_list = wrapped_requests(PROXY_LIST_URL, json=True)
print("[+] Loaded proxy list from remote")

if not remote_proxy_list:
    print("[!] Unable to get proxies")
    exit(2)

for proxy in remote_proxy_list:
    proxy_protocol = proxy["protocol"]

    if proxy_protocol != "http":
        continue

    proxy_ip = proxy["host"]
    proxy_port = proxy["port"]

    proxy_list.append(f"{proxy_protocol}://{proxy_ip}:{proxy_port}")

for to_test in NEED_PROXY:
    url = SOURCES[to_test]

    for candidate in random.sample(proxy_list, len(proxy_list)):
        proxies = {
            'http': candidate,
            'https': candidate,
        }
        
        if not wrapped_requests("https://checkip.amazonaws.com", proxies=proxies, timeout=5, quiet=True, retries=1):
            continue

        r = wrapped_requests(url, proxies=proxies, timeout=5, quiet=True, head=True, retries=1)

        if r:
            working_proxies.append(candidate)
            print(f"[+] Found a working proxy (total {len(working_proxies)})")

        if len(working_proxies) > 2:
            break
    else:
        continue

    break

json.dump(working_proxies, open(os.path.join("sources", "working-proxies.json"), "w"), indent=4)