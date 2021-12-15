#!/usr/bin/env python3
# -*- coding: utf-8 -*
import os
import logging
import threading
import configargparse

import numpy as np

from pathlib import Path
from telegram.ext import Updater
from datetime import datetime as dtm
from picamera.array import PiMotionAnalysis
from picamera import PiCamera, Color as PiColor
from logging.handlers import RotatingFileHandler


def get_args():
    """Arguments parser and checker."""
    parser = configargparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', is_config_file=True,
                        help='Path to config file.')

    # telergam arguments
    parser.add_argument('--token', required=True,
                        help='Token for your telegram bot.')
    parser.add_argument('--channel-id', required=True,
                        help='Telegram channel ID. If you don\'t have it '
                             'please, send a message to your channel and '
                             'run /usr/lib/rpi-surveillance/get_channel_id '
                             'with your token.')

    # other arguments
    parser.add_argument('--temp-dir', type=Path,
                        default=Path('/usr/lib/rpi-surveillance/ram-dir'),
                        help='Path to temporary directory for video saving '
                             'before sending to channel. Don\'t change it if '
                             'you don\'t know what you\'re doing.')
    parser.add_argument('--log-file',
                        help='Path to log file for logging.')

    # camera arguments
    parser.add_argument('--resolution', default='640x480',
                        choices=['640x480', '1280x720', '1920x1080'],
                        help='Camera resolution. Default - 640x480.')
    parser.add_argument('--fps', type=int, default=25, choices=[25, 30, 60],
                        help='Frames per second. Default - 25.')
    parser.add_argument('--rotation', type=int, default=0,
                        choices=[0, 90, 180, 270],
                        help='Frame rotation. Default - 0.')
    parser.add_argument('--duration', type=int, default=10,
                        help='Duration of videos in seconds. Default - 10.')

    # detection arguments
    parser.add_argument('--magnitude-th', type=int,
                        help='Magnitude threshold for motion detection '
                             '(lower - more sensitive). '
                             'Defaults: for 640x480 - 15,'
                             '          for 1280x720 - 40,'
                             '          for 1920x1080 - 65.')
    parser.add_argument('--vectors-quorum', type=int,
                        help='Vectors quorum for motion detection '
                             '(lower - more sensitive). '
                             'Defaults: for 640x480 - 10,'
                             '          for 1280x720 - 20,'
                             '          for 1920x1080 - 40.')
    parser.add_argument('--detection-frames', type=int, default=4,
                        help='The number of consecutive frames with detected '
                             'motion to send an alert.')

    # check args
    args = parser.parse_args()
    assert args.duration > 2, 'duration is too low.'

    if args.magnitude_th is None:
        default_magnitudes = {'640x480': 15, '1280x720': 40, '1920x1080': 65}
        args.magnitude_th = default_magnitudes[args.resolution]

    if args.vectors_quorum is None:
        default_vectors = {'640x480': 10, '1280x720': 20, '1920x1080': 40}
        args.vectors_quorum = default_vectors[args.resolution]

    return args


class DetectMotion(PiMotionAnalysis):
    def __init__(self,
                 camera,
                 vectors_quorum=10,
                 magnitude_th=60,
                 motion_frames=4):
        super().__init__(camera)
        self._magnitude_th = magnitude_th
        self._vectors_quorum = vectors_quorum
        self._motion_frames = motion_frames
        self._motions_history = 0
        self._motion = False

    def analyze(self, motions):
        motions = np.sqrt(
            np.square(motions['x'].astype(np.float)) +
            np.square(motions['y'].astype(np.float))
        ).clip(0, 255).astype(np.uint8)

        # check motion on the current frame
        if (motions > self._magnitude_th).sum() > self._vectors_quorum:
            self._motions_history += 1
        else:
            self._motions_history = 0

        # check last N frames motion trigger
        if self._motions_history >= self._motion_frames:
            self._motion = True

    def reset_detection(self):
        """Clean detected motion."""
        self._motion = False

    def detect_motion(self):
        """Return True if motion was presented."""
        return self._motion


def send_record(bot, channel_id, h264_path, fps):
    """Convert a record to from h264 to mp4 and send it to a telegram channel.

    Parameters
    ----------
    bot : telegram.ext.Updater.bot
        Telegram bot instance.
    channel_id : str
        Telegram channel_id of your channel.
    h264_path : pathlib.Path
        Path to h264 record.
    fps : int
        Frames per seconds for h264 record.

    """
    # convert h264 to mp4
    mp4_path = h264_path.parent.joinpath(h264_path.stem + '.mp4')
    cmd = f'MP4Box -add {h264_path} -fps {fps} {mp4_path} >> /dev/null 2>&1'
    os.system(cmd)

    # send to telegram channel
    bot.send_video(chat_id=channel_id,
                   video=open(mp4_path, 'rb'),
                   supports_streaming=True)

    # clean up
    os.remove(mp4_path)
    os.remove(h264_path)


def main():
    """Application entry point."""
    args = get_args()

    # clean temp dir
    [os.remove(x) for x in args.temp_dir.glob('*.*')]

    # setup logging
    date_format = '%Y-%m-%d_%H-%M-%S'
    logging.basicConfig(level=logging.INFO,
                        format='[%(levelname)s] %(asctime)s - %(message)s',
                        datefmt=date_format)

    logger = logging.getLogger('rpi_logger')
    logger.info('Initializing')

    if args.log_file is not None:
        handler = RotatingFileHandler(args.log_file, 'w', 1024 * 1024 * 50, 5)
        logger.addHandler(handler)

    # connect to telegram bot
    updater = Updater(token=args.token)

    # setup camera
    camera = PiCamera(resolution=args.resolution, framerate=args.fps)
    camera.rotation = args.rotation
    camera.annotate_text_size = 14
    camera.annotate_background = PiColor('black')

    # setup move detection
    output = DetectMotion(camera,
                          args.vectors_quorum,
                          args.magnitude_th,
                          args.detection_frames)
    
    # send notification
    updater.bot.send_message(chat_id=args.channel_id,
                             text='Surveillance has been started.')
    
    logger.info('Initialization completed')
    logger.info('Start recording')
    try:
        while True:
            start = dtm.now()
            h264_path = args.temp_dir.joinpath(
                start.strftime(date_format) + '.h264')

            output.reset_detection()
            camera.annotate_text = dtm.now().strftime(date_format)
            camera.start_recording(str(h264_path),
                                format='h264',
                                motion_output=output)

            # make a record
            while (dtm.now() - start).seconds < args.duration:
                camera.annotate_text = dtm.now().strftime(date_format)
                camera.wait_recording(0.2)

            # save file
            camera.stop_recording()

            # if there was a motion - convert and send video asynchronously
            if output.detect_motion():
                logger.warning('Motion detected, sending a record')
                threading.Thread(
                    daemon=True,
                    target=send_record,
                    args=[updater.bot, args.channel_id, h264_path, args.fps]
                ).start()
            else:
                os.remove(h264_path)
    finally:
        camera.stop_recording()


if __name__ == '__main__':
    main()
