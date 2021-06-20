#!/usr/bin/env bash

HELP_MESSAGE=$(cat <<-END
usage: install.sh [--help] TOKEN CHAT_ID

positional arguments:
  TOKEN    Telegram token of your bot.
  CHAT_ID  Chat/channel ID where your bot is added and can send messages.

optional arguments:
  --help            Show this help message and exit.
END
)

# check arguments
TOKEN=$1
if [ "${TOKEN}" == "" ]; then
    echo "[ERROR] Please enter the Telegram token for your bot."
    exit 1
elif [ "${TOKEN}" == "--help" ]; then
    echo "${HELP_MESSAGE}"
    exit 0
fi

CHAT_ID=$2
if [ "${CHAT_ID}" == "" ]; then
    echo "[ERROR] Please enter the Telegram chat where your bot is."
    exit 2
fi

# create default config file
REPO_DIR=$(dirname "$0")
CONFIG_FILE="${REPO_DIR}/default.cfg"

if [ -f "${CONFIG_FILE}" ]; then
    echo "[ERROR] ${CONFIG_FILE} exists. Please, remove it before continuing."
    exit 3
fi

# install requirements
sudo apt update
sudo apt install python3-pip python3-venv libatlas-base-dev

# create and setup venv
VENV_DIR="${REPO_DIR}/.venv"
python3 -m venv "${VENV_DIR}"
source "${VENV_DIR}/bin/activate"
pip3 install --upgrade pip
pip3 install -r "${REPO_DIR}/requirements.txt"
deactivate

# create default config file
touch "${CONFIG_FILE}"
echo "token=${TOKEN}" >> "${CONFIG_FILE}"
echo "chat-id=${CHAT_ID}" >> "${CONFIG_FILE}"
echo "temp-dir=/tmp/rpi-surveillance" >> "${CONFIG_FILE}"
echo "resolution=640x480" >> "${CONFIG_FILE}"
echo "fps=25" >> "${CONFIG_FILE}"
echo "rotation=0" >> "${CONFIG_FILE}"
echo "duration=10" >> "${CONFIG_FILE}"

echo -e "\nDone! We created ${CONFIG_FILE} with default configuration that you can change."
echo "Now you can run it using start.sh"
