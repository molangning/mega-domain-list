#!/usr/bin/env python3
from shared_lib import chunk_list

import os

OUTPUT_ROOT = os.path.join("lists", "domains", "split")
WITHOUT_SUBDOMAIN_LIST = open(
    os.path.join("lists", "domains", "domains-without-subdomains.txt")
).readlines()
DOMAIN_LIST = open(os.path.join("lists", "domains", "domains.txt")).readlines()

counter = 1

for to_remove in os.listdir(os.path.join(OUTPUT_ROOT, "domains-without-subdomains")):
    os.remove(os.path.join(OUTPUT_ROOT, "domains-without-subdomains", to_remove))

for to_remove in os.listdir(os.path.join(OUTPUT_ROOT, "domains")):
    os.remove(os.path.join(OUTPUT_ROOT, "domains", to_remove))

for chunk in chunk_list(DOMAIN_LIST, 4000000):
    open(
        os.path.join(
            OUTPUT_ROOT,
            "domains",
            f"domains-split-{counter}.txt",
        ),
        "w",
    ).write("".join(chunk))

    counter += 1

counter = 1
for chunk in chunk_list(WITHOUT_SUBDOMAIN_LIST, 4000000):
    open(
        os.path.join(
            OUTPUT_ROOT,
            "domains-without-subdomains",
            f"domains-without-subdomains-split-{counter}.txt",
        ),
        "w",
    ).write("".join(chunk))

    counter += 1
