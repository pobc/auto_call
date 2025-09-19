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

    def load_mp3_file(self, file_path):
        logger2.info(f'加载{file_path}')
        self.is_loaded_mp3 = False
        self.mp3_file_path = file_path

    def send_data_async(self, data_byte):
        if 'task_startup' in cache_tools.cache and cache_tools.cache['task_startup'] is True and self.model is not None:
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
        logger2.info(f"task_startup:{'task_startup' in cache_tools.cache}")
        while ('task_startup' in cache_tools.cache and cache_tools.cache['task_startup'] is True
               and self.is_recoding is True):
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

                # 检查从MP3数据流中提取的数据块大小是否与当前录音数据块大小一致。如果一致，则进行数据混合。
                if len(mp3_chunk) == len(record_audio_data_tmp):
                    # print(f'{wav_start_byte}-{wav_start_byte + CHUNK * wav_audio.frame_width}')
                    # 将录音数据块和MP3数据块转换为NumPy数组，并将它们相加进行混合
                    combined_data = np.frombuffer(record_audio_data_tmp, dtype=np.int16) + np.frombuffer(mp3_chunk,
                                                                                                         dtype=np.int16)
                    record_audio_data_tmp = combined_data.tobytes()

            self.audio_stream_data.append(record_audio_data_tmp)
            self.audio_stream_data_single.append(record_audio_data)
            if ('phone_state' in cache_tools.cache and
                    cache_tools.cache['phone_state'] == PhoneState.CHATTING.value):

                if self.audio_buffer_index == 0:
                    self.audio_buffer_index = len(self.audio_stream_data) - 1

                if self.audio_buffer_index_single == 0:
                    self.audio_buffer_index_single = len(self.audio_stream_data_single) - 1

                if self.audio_buffer_index >= 0:
                    self.audio_buffer_end_index = len(self.audio_stream_data) - 1

                if self.audio_buffer_index_single >= 0:
                    self.audio_buffer_end_index_single = len(self.audio_stream_data_single) - 1

    def save_speech_file(self, file_path, speech_data):
        directory = os.path.dirname(file_path)

        # Create directory if it doesn't exist
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        wave_file = wave.open(file_path, 'wb')
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(self.audio.get_sample_size(FORMAT))
        wave_file.setframerate(sample_rate)
        wave_file.writeframes(b''.join(speech_data))
        wave_file.close()
        time.sleep(1)
        logger2.info(f"录音已保存为 {file_path}")

    def save_audio(self, phone_num, task_code) -> str:
        if self.audio is None:
            logger2.info('audio 未初始化')
        file_name = f'{phone_num}_{time_tools.now_str("%Y%m%d%H%M%S")}.wav'
        file_name_single = f'{phone_num}_{time_tools.now_str("%Y%m%d%H%M%S")}_single.wav'

        file_path = fr'{config.audio_file_save_path}\{task_code}\{file_name}'
        file_path_single = fr'{config.audio_file_save_path}\{task_code}\{file_name_single}'
        if len(self.audio_stream_data) > 0 and self.audio_buffer_index > 0:
            self.audio_stream_data = self.audio_stream_data[self.audio_buffer_index:self.audio_buffer_end_index]
            self.audio_stream_data_single = self.audio_stream_data_single[
                                            self.audio_buffer_index_single:self.audio_buffer_end_index_single]
            self.save_speech_file(file_path, self.audio_stream_data)
            self.save_speech_file(file_path_single, self.audio_stream_data_single)
        else:
            logger2.info('audio 录音数据长度为0')
        self.audio_stream_data.clear()
        self.audio_buffer_index = 0
        self.audio_buffer_end_index = 0
        self.audio_buffer_index_single = 0
        self.audio_buffer_end_index_single = 0
        return file_name

    def on_message(self, message_json):
        """
            接收服务端返回的消息
            :param ws:
            :param message: json格式，自行解析
            :return:
            """
        # [{'key': 'rand_key_dtl2HUetz1vtA', 'text': '我要'}]
        phone_num = cache_tools.cache["last_call_phone_num"]
        if (self.last_phone_status != PhoneState.CHATTING.value and
                cache_tools.cache[f'phone_state'] == PhoneState.CHATTING.value):
            cache_tools.cache[f'chat_all_txt_{phone_num}'] += '###'
        self.last_phone_status = cache_tools.cache[f'phone_state']
        if len(message_json) > 0:
            # 成功收到反馈，输出内容
            receive_txt = message_json[0]["text"]
            if 'last_call_phone_num' in cache_tools.cache and len(receive_txt) > 0:
                timestamp = time.time()
                cache_tools.cache[f'chat_all_txt_{phone_num}'] += receive_txt
                if timestamp - cache_tools.cache[f'chat_last_timestamp_{phone_num}'] < 3:
                    cache_tools.cache[f'chat_last_txt_{phone_num}'] += receive_txt
                else:
                    cache_tools.cache[f'chat_last_txt_{phone_num}'] = receive_txt
                cache_tools.cache[f'chat_last_timestamp_{phone_num}'] = timestamp

            if message_json[0]["text"] == '':
                chat_all_txt = cache_tools.cache[f'chat_all_txt_{phone_num}']
                if len(chat_all_txt) > 0 and chat_all_txt[-1] != ';':
                    cache_tools.cache[f'chat_all_txt_{phone_num}'] += ';'

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
    cache_tools.init()
    cache_tools.cache['task_startup'] = True
    cache_tools.cache["last_call_phone_num"] = '999'
    cache_tools.cache["chat_last_txt_999"] = ''
    cache_tools.cache["chat_all_txt_999"] = ''
    cache_tools.cache["chat_last_timestamp_999"] = time.time()
    cache_tools.cache[f'phone_state'] = PhoneState.CHATTING.value
    cache_tools.cache[f'phone_state'] = PhoneState.CHATTING.value
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
