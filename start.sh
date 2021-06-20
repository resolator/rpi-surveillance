#!/usr/bin/env bash

# mount tmpfs
REPODIR=$(dirname "$0")
TEMP_DIR="/tmp/rpi-surveillance"
if [ ! -d "${TEMP_DIR}" ]; then
    mkdir "${TEMP_DIR}"
fi
sudo mount -t tmpfs -o size=256m tmpfs "${TEMP_DIR}"

# activate venv
source "${REPODIR}/.venv/bin/activate"

# launch surveillance
python3 surveillance.py --config "${REPODIR}/default.cfg"
