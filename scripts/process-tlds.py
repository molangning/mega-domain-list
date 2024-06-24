#!/usr/bin/env python3

from shared_lib import process_csv_line, process_dat_line, process_plain_line

import json
import os

SOURCES_PATH = os.path.join("sources", "tlds.json")
SOURCES = json.load(open(SOURCES_PATH))

OUTPUT_ROOT = os.path.join("lists", "tlds")

tlds = {}

for i in range(1, 11):
    tlds[str(i)] = set()


def add_tlds(split_tld):
    if not split_tld:
        return

    if len(split_tld) == 1:
        tlds["1"].add(split_tld[0])
        return

    for i in range(1, len(split_tld) + 1):
        partial_tld = ".".join(split_tld[-i:])
        try:
            tlds[str(i)].add(partial_tld)
        except KeyError:
            tlds[str(i)] = set(partial_tld)


for dir_file in os.listdir(OUTPUT_ROOT):
    filename, ext = dir_file.rsplit(".", 1)

    if filename not in SOURCES.keys():
        continue

    if ext == "csv":
        processor = process_csv_line
    elif ext == "dat":
        processor = process_dat_line
    else:
        processor = process_plain_line

    filepath = os.path.join(OUTPUT_ROOT, dir_file)

    try:
        f = open(filepath)

    except FileNotFoundError:
        print(f"[!] Can't open {filepath}")
        continue

    for line in f:
        add_tlds(processor(line.strip()))

for levels in tlds.copy().keys():
    if not tlds[levels]:
        del tlds[levels]
        continue

    tlds[levels] = sorted(tlds[levels])

    open(os.path.join(OUTPUT_ROOT, f"tld-level-{levels}.txt"), "w").write(
        "\n".join(tlds[levels])
    )

if tlds:
    json.dump(
        tlds, open(os.path.join(OUTPUT_ROOT, "tld-all-levels.json"), "w"), indent=4
    )
