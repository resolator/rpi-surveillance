# rpi-surveillance
Make a surveillance camera from your Raspberry Pi 4!

The surveillance is built as following: the camera records 10 seconds video 
and if a motion was detected - sends the video to telegram channel.

Tested on Raspberry Pi 4 (4 RAM) + NoIR Camera V2.

## Installation

### Install package

Install Python 3 requirements:
```shell
pip3 install --user -r requirements.txt
```

Install provided `.deb` package:
```shell
sudo dpkg -i <path/to/downloaded/rpi-surveillance.deb>
sudo apt install -f
```

Note: the installation supposes that you already enabled camera module on your Raspberry Pi.

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
5. Run `/usr/lib/rpi-surveillance/get_channel_id` to get the CHANNEL_ID. 
   Save it for future use.


## Usage

To launch surveillance just run `rpi-surveillance` with your TOKEN and 
CHANNEL_ID, for example:
```shell
rpi-surveillance --token 1259140266:WAaqkMycra87ECzRZwa6Z_8T9KB4N-8OPI --channel-id -1003209177928
```

You can set various parameters of the surveillance:
```
usage: rpi-surveillance [-h] [--config CONFIG] --token TOKEN --channel-id
                        CHANNEL_ID [--temp-dir TEMP_DIR]
                        [--resolution {640x480,1280x720,1920x1080}]
                        [--fps {25,30,60}] [--rotation {0,90,180,270}]
                        [--duration DURATION] [--magnitude-th MAGNITUDE_TH]
                        [--vectors-quorum VECTORS_QUORUM]
                        [--log-file LOG_FILE]

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Path to config file.
  --token TOKEN         Token for your telegram bot.
  --channel-id CHANNEL_ID
                        Telegram channel ID. If you don't have it please, send
                        a message to your channel and run /usr/lib/rpi-
                        surveillance/get_channel_id with your token.
  --temp-dir TEMP_DIR   Path to temporary directory for video saving before
                        sending to channel. Don't change it if you don't know
                        what you're doing.
  --resolution {640x480,1280x720,1920x1080}
                        Camera resolution. Default - 640x480.
  --fps {25,30,60}      Frames per second. Default - 25.
  --rotation {0,90,180,270}
                        Frame rotation. Default - 0.
  --duration DURATION   Duration of videos in seconds. Default - 10.
  --magnitude-th MAGNITUDE_TH
                        Magnitude threshold for motion detection (lower - more
                        sensitive). Defaults: for 640x480 - 15, for 1280x720 -
                        40, for 1920x1080 - 65.
  --vectors-quorum VECTORS_QUORUM
                        Vectors quorum for motion detection (lower - more
                        sensitive). Defaults: for 640x480 - 10, for 1280x720 -
                        20, for 1920x1080 - 40.
  --log-file LOG_FILE   Path to log file for logging.
```

## Build
Build was done using `dpkg-buildpackage`.
