#!/bin/bash

set -euxo pipefail
export PYTHONUNBUFFERED=1

./scripts/download-tlds.py
./scripts/download-sources.py
./scripts/process-tlds.py
./scripts/process-sources.py
./scripts/merge-domains.py
./scripts/split-domains.py
