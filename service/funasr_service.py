# -*- coding: utf-8 -*-

import colorlog
import wave
from utils import cache_tools, time_tools, logging_tools
from pydub import AudioSegment
from funasr import AutoModel

import datetime
import os
import logging
import threading
import time
import pyaudio

from main import config
import numpy as np
from service.audio.enum_const import PhoneState

logger2 = logging_tools.get_logger()

# 配置音频
FORMAT = pyaudio.paInt16  # 音频格式
CHANNELS = 1  # 1单声道， 2 立体声
# Stream parameters
sample_rate = 16000  # Sample rate for the audio stream
chunk_size = [0, 10, 5]  # [0, 10, 5] 600ms, [0, 8, 4] 480ms
chunk_stride = chunk_size[1] * 960  # 600ms
buffer_size = int(chunk_stride)  # Size of the buffer for one chunk
# CHUNK = 2048  # 缓冲区大小

encoder_chunk_look_back = 4  # number of chunks to lookback for encoder self-attention
decoder_chunk_look_back = 1  # number of encoder chunks to lookback for decoder cross-attention
# Cache for the model
cache = {}


def list_audio_devices():
    """列出所有可用的音频输入设备"""
    p = pyaudio.PyAudio()
    print("可用音频设备：")
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if dev['maxInputChannels'] > 0:  # 只显示输入设备
            print(f"设备ID {i}: {dev['name']}, 输入声道: {dev['maxInputChannels']}")


class AudioLocalService(object):
    # 打开音频流
    stream: pyaudio.Stream = None
    audio_stream_data = []
    audio_stream_data_single = []
    audio_buffer_index = 0
    audio_buffer_index_single = 0
    audio_buffer_end_index = 0
    audio_buffer_end_index_single = 0
    audio: pyaudio.PyAudio
    start_time = time.time()
    mp3_file_path = None
    is_loaded_mp3 = False
    is_recoding = False
    model = None
    sample_count = 0
    encoder_chunk_look_back = 4  # number of chunks to lookback for encoder self-attention
    decoder_chunk_look_back = 1  # number of encoder chunks to lookback for decoder cross-attention
    last_phone_status = None

    def __init__(self):
        pass

    def init(self):
        print('init AudioWsService2')
        device_index = 11
        logger2.info(f'AudioWsService 初始化')
        self.audio = pyaudio.PyAudio()
        self.is_recoding = True
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                                      rate=sample_rate, input=True,
                                      frames_per_buffer=buffer_size)
        model_path = r"C:\Users\jiang\.cache\modelscope\hub\iic\speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-online"
        if self.model is None:
            self.model = AutoModel(model=model_path, disable_update=True)
        logger2.info(f'AudioWsService 初始化2')
        threading.Thread(target=self.send_and_append_mp3_data, daemon=True).start()


    def send_data_async(self, data_byte):
        audio_chunk = np.frombuffer(data_byte, dtype=np.int16)

        # Convert to float and normalize the audio chunk
        # disable_pbar 关闭语音文字识别时候的 日志输出
        audio_chunk = audio_chunk.astype(np.float32) / 32768.0  # Normalize to [-1, 1]
        res = self.model.generate(input=audio_chunk, cache=cache, is_final=False,
                                  chunk_size=chunk_size, disable_pbar=True,
                                  encoder_chunk_look_back=encoder_chunk_look_back,
                                  decoder_chunk_look_back=decoder_chunk_look_back)
        self.on_message(res)

    def send_and_append_mp3_data(self):
        if self.model is None:
            return
        print("Recording...")
        logger2.info("send_audio total={}")
        mp3_audio = None
        mp3_bytes = None
        while True:
            time.sleep(0.5)
            # 读取录音数据
            record_audio_data = self.stream.read(buffer_size)
            threading.Thread(target=self.send_data_async, args=(record_audio_data,)).start()
            record_audio_data_tmp = record_audio_data
            if self.mp3_file_path is not None:
                if self.is_loaded_mp3 is False:
                    logger2.info(f'读取mp3文件：{self.mp3_file_path[-6:]}')
                    mp3_audio = AudioSegment.from_mp3(self.mp3_file_path)
                    # duration_ms = len(wav_audio)
                    mp3_audio = mp3_audio.set_frame_rate(sample_rate).set_channels(CHANNELS)
                    # 将MP3音频转换为字节数据
                    mp3_bytes = mp3_audio.raw_data
                    self.sample_count = 0
                    self.is_loaded_mp3 = True

                self.sample_count += buffer_size  # 更新采样总数
                # ------------------ ##
                # 计算自录音开始以来经过的时间。
                mp3_start_frame = self.sample_count  # 当前采样点数就是音频的起始位置
                mp3_start_byte = mp3_start_frame * mp3_audio.frame_width

                # 计算应从MP3文件中读取的字节的起始位置。mp3_start_frame * CHUNK * wav_audio.frame_width 计算对应的字节数。
                end_byte = mp3_start_byte + buffer_size * mp3_audio.frame_width

                if end_byte <= len(mp3_bytes):
                    mp3_chunk = mp3_bytes[mp3_start_byte:end_byte]
                else:
                    mp3_chunk = mp3_bytes[mp3_start_byte:]  # 处理越界情况





    def on_message(self, message_json):
        """
            接收服务端返回的消息
            :param ws:
            :param message: json格式，自行解析
            :return:
            """
        if len(message_json) > 0:
            # 成功收到反馈，输出内容
            receive_txt = message_json[0]["text"]
            print(receive_txt)

        else:
            logger2.info("Response: " + message_json)

    log_colors_config = {
        'DEBUG': 'white',
        'INFO': 'white',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }

    def stop_recording(self):
        self.is_recoding = False
        time.sleep(1.1)
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()


class NoColorFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)
        return message  # 去掉任何颜色控制字符


if __name__ == "__main__":
    logger2.info('fsfsd')
    # list_audio_devices()
    aud = AudioLocalService()
    aud.init()

    while True:
        time.sleep(10)
    #     handler = logging.StreamHandler()
    #     formatter = colorlog.ColoredFormatter(
    #         '%(log_color)s[%(asctime)-15s] [%(funcName)s()][%(levelname)s] %(message)s'
    #     )
    #     handler.setFormatter(formatter)
    #     logger = logging.getLogger(__name__)
    #     logger.addHandler(handler)
    #
    #     logger.setLevel(logging.DEBUG)  # 调整为logging.INFO，日志会少一点
    #     logger.info("begin")
    #     # websocket.enableTrace(True)
    #     uri = const.URI + "?sn=" + str(uuid.uuid1())
    #     logger.info("uri is " + uri)
    #     # init()
    #     # ws_app = websocket.WebSocketApp(uri,
    #     #                                 on_open=on_open,  # 连接建立后的回调
    #     #                                 on_message=on_message,  # 接收消息的回调
    #     #                                 on_error=on_error,  # 库遇见错误的回调
    #     #                                 on_close=on_close)  # 关闭后的回调
    #     # ws_app.run_forever()
    pass
