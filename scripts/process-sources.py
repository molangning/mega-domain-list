#!/usr/bin/env python3

from multiprocessing import Pool
from shared_lib import chunk_list

import json
import os
import time

SOURCES_PATH = os.path.join("sources", "sources.json")
SOURCES = json.load(open(SOURCES_PATH))

TLDS_PATH = os.path.join("lists", "tlds", "tld-all-levels.json")
TLDS = json.load(open(TLDS_PATH))
TLDS_SEARCH_ORDER = sorted(TLDS.keys())[1:][::-1]

OUTPUT_ROOT = os.path.join("lists", "domains")
CHUNK_SIZE = 100000

subdomains = set()
root_domains = set()

def find_offset(fields):
    offset = 0

    for field in fields:
        if field.strip('"').count(".") > 0:
            return offset 
        offset += 1

    return None

def process_domain(domain_list):
    t1 = time.time()
    results = [set(), set()]

    for domain in domain_list:
        if domain.count(".") == 1:
            results[0].add(domain)
            continue

        split_domain = domain.split(".")

        for i in TLDS_SEARCH_ORDER:
            i = int(i)
            partial_tld = ".".join(split_domain[-i:])
            if partial_tld in TLDS[str(i)]:
                results[0].add(partial_tld)
                results[1].update(split_domain[:-i])
                break
        else:
            results[0].add(".".join(split_domain[-2:]))
            results[1].update(split_domain[:-2])
    
    results.append(round(time.time() - t1, 3))
    return results

tasks_start_time = time.time()

for dir_file in os.listdir(OUTPUT_ROOT):
    filename, ext = dir_file.rsplit(".", 1)

    if filename not in SOURCES.keys():
        continue

    filepath = os.path.join(OUTPUT_ROOT, dir_file)

    try:
        f = open(filepath)

    except FileNotFoundError:
        print(f"[!] Can't open {filepath}")
        continue

    print(f"[+] Starting task {filename}")
    start_time = time.time()

    offset = 0
    tasks = []

    for line in f:
        fields = line.split(",")

        if not fields[0].strip('"\n').isnumeric():
            continue

        offset = find_offset(fields)

        if not offset:
            continue

        tasks.append(fields[offset].strip('"\n'))
        break

    for line in f:
        fields = line.split(",")
        tasks.append(fields[offset].strip('"\n'))

    print(f"[+] Extracted {len(tasks)} domains in {round(time.time() - start_time, 3)} seconds")

    pool = Pool()
    batch_counter = 1
    total_batches = 0

    total_batches = len(tasks) / CHUNK_SIZE

    if not total_batches.is_integer():
        total_batches = int(total_batches) + 1
    else:
        total_batches = int(total_batches)

    print(f"[+] Starting batch processing with batch size {CHUNK_SIZE}")
    start_time = time.time()
    
    for result in pool.imap(process_domain, chunk_list(tasks, CHUNK_SIZE)):
        if root_domains:
            root_domains.update(result[0])
        if subdomains:
            subdomains.update(result[1])

        print(f"[+] Processed batch {batch_counter}/{total_batches} in {result[2]} seconds")
        batch_counter+=1
    
    pool.close()
    pool.join()

    print(f"[+] Finished processing task {filename} in {round(time.time() - start_time, 3)} seconds")
    open("domains.txt", "w").write("\n".join(sorted(root_domains)))
    open("subdomains.txt", "w").write("\n".join(sorted(subdomains)))

print(f"[+] Finished all tasks in {round(time.time() - tasks_start_time, 3)} seconds")


