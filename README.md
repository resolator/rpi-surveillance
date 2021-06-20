# rpi-surveillance
Make a surveillance camera from your Raspberry Pi 4!

## Installation

### Create telegram bot and chat

1. Write to `@BotFather` in telegram and create a bot:
```
/start
/newbot
<name of your bot>
<username of your bot>_bot
```
You will get the TOKEN. Save it for future use.

2. Create a private channel where you will receive video sequences with motion.
3. Add created bot to the channel (rerquires only "post messages" permission).
4. Send message `test` to the channel.
5. Run `get_chat_id.sh` to get the CHANNEL_ID. Save it for future use.

### Install package

Run `install.sh` and it will install all required packages (sudo required):
```shell
usage: install.sh [--help] TOKEN CHANNEL_ID

positional arguments:
  TOKEN    Telegram token of your bot.
  CHANNEL_ID  Channel ID where your bot is added and can send messages.

optional arguments:
  --help            Show this help message and exit.
```

Note: the installation supposes that you already enabled camera module on your Raspberry Pi.


## Usage

After installation done the `default.cfg` will be created. You can modify it to
controll the surveillance settings. The following arguments are available:
```
  --token TOKEN         Token for your telegram bot.
  --channel-id CHANNEL_ID
                        Telegram channel ID.
  --temp-dir TEMP_DIR   Path to temporary directory for video saving before
                        sending to channel.
  --resolution {640x480,1280x720,1920x1080}
                        Camera resolution.
  --fps {25,30,60}      Frames per second.
  --rotation {0,90,180,270}
                        Frame rotation.
  --duration DURATION   Duration of videos in seconds.
  --log-file LOG_FILE   Path to log file for logging.
```

To launch surveillance just run `start.sh`.

Note: `sudo` required here to create a temporary filesystem mapped on the RAM 
memory  to store a single video before sending it to the channel.

## TODO
- [ ] create deb package
- [ ] move `tmpfs` creation to `fstab` on installation stage
