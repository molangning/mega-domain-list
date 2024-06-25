#!/usr/bin/env python3

from shared_lib import download_source, patch_sources

import json
import os

SOURCES_PATH = os.path.join("sources", "sources.json")
SOURCES = patch_sources(json.load(open(SOURCES_PATH)))

OUTPUT_ROOT = os.path.join("lists", "domains")

headers = {'Accept': '*/*', 
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.3',
            'Accept-Language': 'en-US;q=0.5,en;q=0.3',
            'Cache-Control': 'max-age=0'
            }

for tld_name, download_url in SOURCES.items():
    download_status = download_source(tld_name, download_url, OUTPUT_ROOT, headers)
    
    if not download_status:
        print(f"[!] Skipping {tld_name} as it is unreachable")