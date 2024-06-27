#!/usr/bin/env python3

from shared_lib import wrapped_requests
from multiprocessing.pool import ThreadPool

import json
import os
import random
import time

PROXY_LIST_URL = (
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies.json"
)

SOURCES_PATH = os.path.join("sources", "sources.json")
SOURCES = json.load(open(SOURCES_PATH))

NEED_PROXY_PATH = os.path.join("sources", "need-proxy.json")
NEED_PROXY = json.load(open(NEED_PROXY_PATH))


def check_proxy(candidate):
    proxies = {
        "http": candidate,
        "https": candidate,
    }

    if not wrapped_requests(
        "https://checkip.amazonaws.com",
        proxies=proxies,
        timeout=5,
        quiet=True,
        retries=1,
    ):
        return False

    r = wrapped_requests(
        url, proxies=proxies, timeout=5, quiet=True, head=True, retries=1
    )

    if r:
        print("[+] Found a working proxy")
        return candidate


proxy_list = []
working_proxies = []

start_time = time.time()

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

    pool = ThreadPool(16)

    for result in pool.imap(check_proxy, random.sample(proxy_list, len(proxy_list))):
        if result:
            working_proxies.append(result)

        if len(working_proxies) > 4:
            break


json.dump(
    working_proxies,
    open(os.path.join("sources", "working-proxies.json"), "w"),
    indent=4,
)

print(f"[+] Finished in {round(time.time()-start_time, 2)}")
