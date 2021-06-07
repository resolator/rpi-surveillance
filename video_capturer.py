#!/usr/bin/env python3
# -*- coding: utf-8 -*
import os
import logging
import argparse
import picamera
import picamera.array

import numpy as np

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


class DetectMotion(picamera.array.PiMotionAnalysis):
    def __init__(self, camera, vectors_quorum=10, magnitude_th=60):
        super().__init__(camera)
        self.magnitude_th = magnitude_th
        self.vectors_quorum = vectors_quorum
        self.motion = False

    def analyze(self, motions):
        motions = np.sqrt(
            np.square(motions['x'].astype(np.float)) +
            np.square(motions['y'].astype(np.float))
        ).clip(0, 255).astype(np.uint8)

        if (motions > self.magnitude_th).sum() > self.vectors_quorum:
            self.motion = True


def main():
    """Application entry point."""
    args = get_args()
    logging.basicConfig(level=logging.INFO)
    logging.info('Initializing.')

    # connect to telegram bot
    updater = Updater(token=args.token)
    updater.start_polling()

    # setup camera
    camera = picamera.PiCamera(resolution=args.resolution, framerate=args.fps)
    camera.rotation = args.rotation
    camera.annotate_background = picamera.Color('black')
    time_format = '%Y-%m-%d-%H-%M-%S'
    camera.annotate_text = dtm.now().strftime(time_format)

    # setup move detection
    detection_data = {'640x480': (8, 20),
                      '1280x720': (10, 40),
                      '1920x1080': (12, 60)}
    vectors_quorum, magnitude_th = detection_data[args.resolution]
    output = DetectMotion(camera, vectors_quorum, magnitude_th)

    logging.info('Initialization complete.')
    logging.info('Start recording.')
    while True:
        start = dtm.now()
        file_path = str(args.temp_dir.joinpath(start.strftime(time_format)))

        output.motion = False
        camera.start_recording(file_path + '.h264', format='h264',
                               motion_output=output)

        # make a record
        while (dtm.now() - start).seconds < args.duration:
            camera.annotate_text = dtm.now().strftime(time_format)
            camera.wait_recording(0.2)

        # save file
        camera.stop_recording()

        if output.motion:
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
        os.remove(file_path + '.h264')


if __name__ == '__main__':
    main()
