#!/usr/bin/env python3

from zipfile import ZipFile

import os
import requests
import time

def wrapped_requests(url, headers={}, json=False):
    for i in range(1,4):
        try:
            r = requests.get(url,headers=headers, timeout=60)
    
            if r.status_code==200:
                # print("[+] Got %s successfully!"%(url))
                break
    
            if i==3:
                print("[!] Failed to get %s."%(url))
                return None
    
            print("[!] Getting %s failed(%i/3)"%(url,i))
            time.sleep(0.5)

        except requests.exceptions.Timeout:
            print("[!] Timed out getting %s (%i/3)"%(url,i))

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
        return r.text
    
def download_file(url, fp, headers={}):
    for i in range(1,4):
        try:
            r = requests.get(url, headers=headers, stream=True, timeout=60)
    
            if r.status_code!=200:
                print("[!] Getting %s failed(%i/3)"%(url,i))
                continue
    
            if i==3:
                print("[!] Failed to get %s."%(url))
                exit(2)

            for chunk in r.iter_content(chunk_size=4096):
                fp.write(chunk)

            return True

        except requests.exceptions.Timeout:
            print("[!] Timed out getting %s (%i/3)"%(url,i))

        except requests.exceptions.SSLError:
            return False
        
        except Exception as e:
            print(f"[!] Got exception {e}")
            return False
            
def unzip_file(filepath, base_name):
    base_path, filename = filepath.rsplit("/", 1)
    decompressed_file_name = filename.replace(".zip", "")

    if decompressed_file_name.count(".") < 1:
        print(f"[!] Not unzipping file {filepath} as it does not have a file extension")
        return

    decompressed_file_path = os.path.join(base_path, f'{base_name}.{decompressed_file_name.rsplit(".", 1)[1]}')

    with ZipFile(filepath) as compressed_file:
        open(decompressed_file_path, "wb").write(compressed_file.open(decompressed_file_name).read())

    print(f"[+] Extracted {decompressed_file_name}")
    os.remove(filepath)