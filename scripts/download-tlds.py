#!/usr/bin/env python3

from shared_lib import download_file, unzip_file

import json
import os

SOURCES_PATH = os.path.join("sources", "tlds.json")
SOURCES = json.load(open(SOURCES_PATH))

OUTPUT_ROOT = os.path.join("lists", "tlds")

for tld_name, download_url in SOURCES.items():
    compressed_file = False
    file_name = download_url.rsplit("/", 1)[1]

    if file_name.endswith(".zip"):
        compressed_file = True

    temp_file_name = file_name + ".part"
    temp_file_path = os.path.join(OUTPUT_ROOT, temp_file_name)

    output_file_path = os.path.join(OUTPUT_ROOT, file_name)
    download_file(download_url, open(temp_file_path, "wb"))

    print(f"[+] Downloaded {tld_name}")

    os.rename(temp_file_path, output_file_path)
    
    if compressed_file:
        unzip_file(output_file_path, tld_name)