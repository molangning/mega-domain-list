#!/usr/bin/env python3

from shared_lib import find_offset

import json
import os
import time

SOURCES_PATH = os.path.join("sources", "sources.json")
SOURCES = json.load(open(SOURCES_PATH))

OUTPUT_ROOT = os.path.join("lists", "domains")

domains = set()


for dir_file in os.listdir(OUTPUT_ROOT):
    filepath = os.path.join(OUTPUT_ROOT, dir_file)

    if not os.path.isfile(filepath):
        continue

    filename, ext = dir_file.rsplit(".", 1)

    if filename not in SOURCES.keys():
        continue

    try:
        f = open(filepath)

    except FileNotFoundError:
        print(f"[!] Can't open {filepath}")
        continue

    print(f"[+] Merging {filename}")
    start_time = time.time()

    offset = 0

    for line in f:
        fields = line.split(",")

        if not fields[0].strip('"\n').isnumeric():
            continue

        offset = find_offset(fields)

        if not offset:
            continue

        domains.add(fields[offset].strip('"\n'))
        break

    for line in f:
        fields = line.split(",")
        domains.add(fields[offset].strip('"\n'))

print("[+] Writing to domains.txt")

open(os.path.join(OUTPUT_ROOT, "domains.txt"), "w").write("\n".join(sorted(domains)))
