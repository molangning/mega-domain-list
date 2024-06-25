#!/usr/bin/env python3

from zipfile import ZipFile

import json
import os
import requests
import time


def wrapped_requests(url, headers={}, json=False, head=False, ignore_200=False):
    for i in range(1, 4):
        try:
            if head:
                r = requests.head(url, headers=headers, timeout=60)
            else:
                r = requests.get(url, headers=headers, timeout=60)

            if r.status_code == 200 or ignore_200:
                # print("[+] Got %s successfully!"%(url))
                break

            if i == 3:
                print("[!] Failed to get %s." % (url))
                return None

            print("[!] Getting %s failed(%i/3)" % (url, i))
            time.sleep(0.5)

        except requests.exceptions.Timeout:
            print("[!] Timed out getting %s (%i/3)" % (url, i))

        except requests.exceptions.SSLError:
            return None

        except Exception as e:
            print(f"[!] Got exception {e}")
            return None

    if json is True:
        try:
            return r.json()
        except:
            print("[+] Converting response to dictionary failed")
            return
    else:
        if head == True:
            return r.headers

        return r.text


def download_file(url, fp, headers={}):
    for i in range(1, 4):
        try:
            r = requests.get(url, headers=headers, stream=True, timeout=60)

            if r.status_code != 200:
                print("[!] Getting %s failed(%i/3)" % (url, i))
                time.sleep(0.5)
                continue

            if i == 3:
                print("[!] Failed to get %s." % (url))
                return False

            for chunk in r.iter_content(chunk_size=4096):
                fp.write(chunk)

            return True

        except requests.exceptions.Timeout:
            print("[!] Timed out getting %s (%i/3)" % (url, i))

        except requests.exceptions.SSLError:
            return False

        except Exception as e:
            print(f"[!] Got exception {e}")
            return False


def unzip_file(filepath, base_name):
    base_path, filename = filepath.rsplit("/", 1)

    decompressed_file_name = filename.replace(".zip", "")
    compressed_file_handle = ZipFile(filepath)

    filelist = compressed_file_handle.namelist()

    if decompressed_file_name.count(".") == 0:
        if len(filelist) == 1:
            decompressed_file_name = filelist[0]
        else:
            print(f"[!] Not unzipping file {filepath} as it does not contain one file")
            return

    decompressed_file_path = os.path.join(
        base_path, f'{base_name}.{decompressed_file_name.rsplit(".", 1)[1]}'
    )

    with ZipFile(filepath) as compressed_file:
        open(decompressed_file_path, "wb").write(
            compressed_file.open(decompressed_file_name).read()
        )

    print(f"[+] Extracted {decompressed_file_name}")
    os.remove(filepath)


def process_csv_line(tld):
    return tld.split(",", 1)[1].split(".")


def process_dat_line(tld, removed=False):
    if not tld:
        return

    if tld.startswith("!"):
        return

    if tld.startswith("*."):
        tld = tld[2:]

    if tld.startswith("//"):
        if removed is False:
            return

        tld = tld.split(" ")[1]

        if "/" in tld:
            return

        if (
            tld.endswith(":")
            or tld.endswith(".")
            or tld.startswith(".")
            or tld.endswith(",")
            or not tld.islower()
        ):
            return

        if tld.count(".") == 0:
            return

    return tld.strip().encode("idna").decode().split(".")


def process_plain_line(tld):
    return tld.encode("idna").decode().split(".")


def parse_content_deposition(headers):
    if "Content-Disposition" not in headers.keys():
        return False

    for field in headers["Content-Disposition"].split(";"):
        if "=" not in field:
            continue

        field, value = field.split("=")

        if not field.startswith("filename"):
            continue

        return value

    return False


def parse_location(headers, url):
    if "Location" not in headers.keys():
        return False

    url_scheme = "https"

    if "://" in url:
        url_scheme, url = url.split("://")

    return "://".join([url_scheme, url.split("/", 1)[0]]) + headers["Location"]


def download_source(tld_name, download_url, output_root, headers={}):
    compressed_file = False
    file_name = download_url.rsplit("/", 1)[1]

    if file_name.count(".") == 0:
        file_name = parse_content_deposition(
            wrapped_requests(download_url, head=True, headers=headers)
        )

    if file_name.endswith(".zip"):
        compressed_file = True

    temp_file_name = file_name + ".part"
    temp_file_path = os.path.join(output_root, temp_file_name)

    download_status = download_file(download_url, open(temp_file_path, "wb"), headers)
    if not download_status:
        print("[!] Failed to get file")
        os.remove(temp_file_path)
        return False

    print(f"[+] Downloaded {tld_name}")

    if compressed_file:
        output_file_path = os.path.join(output_root, file_name)
        os.rename(temp_file_path, output_file_path)
        unzip_file(output_file_path, tld_name)

    else:
        file_name = f"{tld_name}.{file_name.rsplit('.', 1)[1]}"
        output_file_path = os.path.join(output_root, file_name)
        os.rename(temp_file_path, output_file_path)

    return True


def chunk_list(to_chunk, chunk_size):
    for i in range(0, len(to_chunk), chunk_size):
        yield to_chunk[i : i + chunk_size]


def patch_sources(sources):
    download_url_format = "https://tranco-list.eu/download/{}/full"

    if "tranco-list-full" not in sources:
        return sources

    tranco_urls = json.load(open(os.path.join("sources", "tranco-list-urls.json")))

    for url in tranco_urls:
        new_url = parse_location(wrapped_requests(url, head=True, ignore_200=True), url)
        file_id = new_url.rsplit("/", 2)[1]
        sources["tranco-list-full"] = download_url_format.format(file_id)
        return sources


def find_offset(fields):
    offset = 0

    for field in fields:
        if field.strip('"').count(".") > 0:
            return offset
        offset += 1

    return None
