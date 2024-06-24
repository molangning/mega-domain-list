#!/usr/bin/env python3

from shared_lib import download_source

import json
import os

SOURCES_PATH = os.path.join("sources", "sources.json")
SOURCES = json.load(open(SOURCES_PATH))

OUTPUT_ROOT = os.path.join("lists", "domains")

for tld_name, download_url in SOURCES.items():
    download_source(tld_name, download_url, OUTPUT_ROOT)
