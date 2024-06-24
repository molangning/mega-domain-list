#!/usr/bin/env python3

from shared_lib import process_csv_line, process_dat_line, process_plain_line

import json
import os

SOURCES_PATH = os.path.join("sources", "sources.json")
SOURCES = json.load(open(SOURCES_PATH))

TLDS_PATH = os.path.join("list", "tlds", "tld-all-levels.json")
TLDS = json.load(open(SOURCES_PATH))

OUTPUT_ROOT = os.path.join("lists", "domains")

for dir_file in os.listdir(OUTPUT_ROOT):
    filename, ext = dir_file.rsplit(".", 1)

    if filename not in SOURCES.keys():
        continue

    print(filename)
