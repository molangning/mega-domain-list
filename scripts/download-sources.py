#!/usr/bin/env python3

from shared_lib import download_source, patch_sources

import json
import os

SOURCES_PATH = os.path.join("sources", "sources.json")
SOURCES = patch_sources(json.load(open(SOURCES_PATH)))

NEED_PROXIES_PATH = os.path.join("sources", "need-proxy.json")
NEED_PROXIES = json.load(open(NEED_PROXIES_PATH))

WORKING_PROXIES_PATH = os.path.join("sources", "working-proxies.json")
WORKING_PROXIES = json.load(open(WORKING_PROXIES_PATH))

OUTPUT_ROOT = os.path.join("lists", "domains")

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/124.0.6367.88 Mobile/15E148 Safari/604.1",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US;q=1.0",
    "Sec-Fetch-Dest": "navigate",
    "Sec-Fetch-Mode": "same-site",
    "Sec-Fetch-Site": "?1",
}


for source_name, download_url in SOURCES.items():
    if source_name in NEED_PROXIES:
        download_status = download_source(
            source_name, download_url, OUTPUT_ROOT, headers, WORKING_PROXIES
        )
    else:
        download_status = download_source(
            source_name, download_url, OUTPUT_ROOT, headers
        )

    if not download_status:
        print(f"[!] Skipping {source_name} as it is unreachable")
