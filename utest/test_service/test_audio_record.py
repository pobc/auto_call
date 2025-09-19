# -*- coding: utf-8 -*-

import websocket
import colorlog
import wave
from pydub import AudioSegment

import threading
import time
import uuid
import json
import logging
import pyaudio
from utils import cache_tools, time_tools
from main import config
import numpy as np
import sounddevice

logger = logging.getLogger('audio_ws_service')

# 配置音频
FORMAT = pyaudio.paInt16  # 音频格式
CHANNELS = 1  # 立体声
RATE = 16000  # 采样率
CHUNK = 2048  # 缓冲区大小

class AudioWsService(object):
    # 打开音频流
    stream: pyaudio.Stream
    audio_stream_data = []
    audio: pyaudio.PyAudio
    start_time = time.time()
    mp3_file_path = None
    mp3_audio = None
    mp3_bytes = None
    is_load_mp3 = False

    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                                      rate=RATE, input=True,
                                      frames_per_buffer=CHUNK)

    def start(self):
        while True:
            time.sleep(0.1)
            pcm = self.stream.read(CHUNK)

if __name__ == '__main__':
    tt = AudioWsService()
    tt.start()