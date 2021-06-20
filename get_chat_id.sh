#!/usr/bin/env bash

HELP_MESSAGE=$(cat <<-END
usage: install.sh [--help] TOKEN

positional arguments:
  TOKEN    Telegram token of your bot.

optional arguments:
  --help            Show this help message and exit.
END
)

# check argument
TOKEN=$1
if [ "${TOKEN}" == "" ]; then
    echo "[ERROR] Please enter the Telegram token for your bot."
    exit 1
elif [ "${TOKEN}" == "--help" ]; then
    echo "${HELP_MESSAGE}"
    exit 0
fi

# extract chat/channel ID
CHAT_ID=$(curl -s "https://api.telegram.org/bot${TOKEN}/getUpdates" | grep -oPm 1 "\"sender_chat\":{\"id\":\K[^<]+?(?=,)")
if [ "${CHAT_ID}" == "" ]; then
    echo -e "\n[WARNING] Could not parse chat ID. Please, check that:"
    echo "- you send a message \"test\" to the chat with bot"
    echo "- bot has access to messages in this chat"
    echo "- bot TOKEN is correct"
    exit 2
else
    echo -e "\nChat/channel ID: ${CHAT_ID}"
fi
