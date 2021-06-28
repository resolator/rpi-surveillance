# -*- coding: utf-8 -*-

# This file is part of rpi-surveillance project.
# Copyright (C) 2021 Vladyslav Dusiak

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='rpi-surveillance',
    use_scm_version=True,
    install_requires=required,
    setup_requires=[
        'setuptools_scm'
    ],
    python_requires='>=3',
    description='Make a surveillance camera from your Raspberry Pi 4! The '
                'surveillance is built as following: the camera records 10 '
                'seconds video and if a motion was detected - sends the video '
                'to telegram channel. Tested on Raspberry Pi 4 (4 RAM) + NoIR '
                'Camera V2.',
    author='Vladyslav Dusiak',
    author_email='v.dusiak@gmail.com',
    url='https://github.com/resolator/rpi-surveillance',
    license='MIT',
    packages=find_packages(exclude=['tests.*']),
    package_data={'rpi_surveillance': ['sbin/get_channel_id']},
    entry_points={
        'console_scripts': ['rpi-surveillance=rpi_surveillance.app:main']
    },
    data_files=[
        ('/usr/lib/rpi-surveillance', [
            'rpi_surveillance/sbin/get_channel_id'
        ]),
        ('/usr/lib/rpi-surveillance/ram-dir', [
            'rpi_surveillance/sbin/.placeholder'
        ])
    ],
    zip_safe=False
)
