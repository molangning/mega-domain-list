#!/usr/bin/env python3

from shared_lib import unzip_file

import json
import os

SOURCES_PATH = os.path.join("sources", "tlds.json")
SOURCES = json.load(open(SOURCES_PATH))

OUTPUT_ROOT = os.path.join("lists", "tlds")

tlds = {}

for i in range(1, 11):
    tlds[str(i)] = set()

for tld_name in SOURCES.keys():
    filepath = os.path.join(OUTPUT_ROOT, tld_name + ".csv")
    
    try:
        f = open(filepath)
    except FileNotFoundError:
        print(f"[!] Can't open {filepath}")
        continue
    
    for line in f:
        split_tld = line.strip().split(",")[1].split(".")
        
        if len(split_tld) == 1:
            tlds["1"].add(split_tld[0])
            continue

        for i in range(1, len(split_tld) + 1):
            partial_tld = ".".join(split_tld[-i:])
            try:
                tlds[str(i)].add(partial_tld)
            except KeyError:
                tlds[str(i)] = set(partial_tld)

for levels in tlds.copy().keys():
    if not tlds[levels]:
        del tlds[levels]
        continue

    tlds[levels] = sorted(tlds[levels])

    open(os.path.join(OUTPUT_ROOT, f"tld-level-{levels}.txt"), "w").write("\n".join(tlds[levels]))

json.dump(tlds, open(os.path.join(OUTPUT_ROOT, f"tld-all-levels-{levels}.txt"), "w"), indent=4)