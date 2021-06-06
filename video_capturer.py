# Web streaming example
# Source code from the official PiCamera package
# http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming
import io
import os
import argparse
import picamera

from datetime import datetime as dtm

from pathlib import Path


def get_args():
    """Arguments parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--resolution', default='640x480',
                        choices=['640x480', '1280x720', '1920x1080'],
                        help='Camera resolution.')
    parser.add_argument('--fps', type=int, default=30, choices=[30, 60],
                        help='Frames per second.')
    parser.add_argument('--rotation', type=int, default=0,
                        choices=[0, 90, 180, 270],
                        help='Frame rotation.')
    parser.add_argument('--duration', type=int, default=10,
                        help='Duration of videos in seconds.')
    parser.add_argument('--save-to', type=Path,
                        help='Path to save dir.')

    return parser.parse_args()


def main():
    """Application entry point."""
    args = get_args()

    time_format = '%Y-%m-%d-%H-%M-%S'
    with picamera.PiCamera(resolution=args.resolution,
                           framerate=args.fps) as camera:
        camera.rotation = args.rotation
        camera.start_preview()
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text = dtm.now().strftime(time_format)

        for _ in range(5):
            start = dtm.now()
            file_name = start.strftime(time_format)
            camera.start_recording(file_name + '.h264')

            # record 10 seconds
            while (dtm.now() - start).seconds < args.duration:
                camera.annotate_text = dtm.now().strftime(time_format)
                camera.wait_recording(0.2)

            # save file
            camera.stop_recording()

            # convert to mp4
            os.system(f'MP4Box -add {file_name}.h264 '
                      f'-fps {args.fps} {file_name}.mp4')

            # send to telegram
            os.system(f'telegram-send --video {file_name}.mp4')

            # clean up
            os.remove(file_name + '.mp4')


if __name__ == '__main__':
    main()
