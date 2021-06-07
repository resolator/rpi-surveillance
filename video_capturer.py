#!/usr/bin/env python3
# -*- coding: utf-8 -*
import os
import argparse
import picamera

from pathlib import Path
from telegram.ext import Updater
from datetime import datetime as dtm


def get_args():
    """Arguments parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--token', required=True,
                        help='Token for your telegram bot.')
    parser.add_argument('--chat-id', required=True,
                        help='Telegram chat ID.')
    parser.add_argument('--temp-dir', type=Path,
                        default=Path('/tmp/rpi-surveillance'),
                        help='Path to temporary directory for video saving '
                             'before sending to chat.')
    parser.add_argument('--resolution', default='640x480',
                        choices=['640x480', '1280x720', '1920x1080'],
                        help='Camera resolution.')
    parser.add_argument('--fps', type=int, default=30, choices=[30, 60],
                        help='Frames per second.')
    parser.add_argument('--rotation', type=int, default=0,
                        choices=[0, 90, 180, 270],
                        help='Frame rotation.')
    parser.add_argument('--duration', type=int, default=5,
                        help='Duration of videos in seconds.')
    parser.add_argument('--save-to', type=Path,
                        help='Path to save dir.')

    return parser.parse_args()


def main():
    """Application entry point."""
    args = get_args()

    print('Initializing...')
    updater = Updater(token=args.token)
    updater.start_polling()

    time_format = '%Y-%m-%d-%H-%M-%S'
    with picamera.PiCamera(resolution=args.resolution,
                           framerate=args.fps) as camera:
        camera.rotation = args.rotation
        camera.start_preview()
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text = dtm.now().strftime(time_format)

        for _ in range(5):
            print('Processing')
            start = dtm.now()
            file_path = str(args.temp_dir.joinpath(
                start.strftime(time_format)))
            camera.start_recording(file_path + '.h264')

            # record 10 seconds
            while (dtm.now() - start).seconds < args.duration:
                camera.annotate_text = dtm.now().strftime(time_format)
                camera.wait_recording(0.2)

            # save file
            camera.stop_recording()

            # convert to mp4
            os.system(f'MP4Box -add {file_path}.h264 '
                      f'-fps {args.fps} {file_path}.mp4')

            # send to telegram
            updater.bot.send_video(
                chat_id=args.chat_id,
                video=open(f'{file_path}.mp4', 'rb'),
                supports_streaming=True)

            # clean up
            os.remove(file_path + '.mp4')


if __name__ == '__main__':
    main()
