# -*- coding: utf-8 -*-

import websocket
import colorlog
import wave
from pydub import AudioSegment
import os
import threading
import time
import uuid
import json
import logging
import pyaudio
from service.audio import const
from utils import cache_tools, time_tools, logging_tools
from main import config
import numpy as np
from service.audio.enum_const import PhoneState

logger = logging_tools.get_logger()

# 配置音频
FORMAT = pyaudio.paInt16  # 音频格式
CHANNELS = 1  # 1单声道， 2 立体声
RATE = 16000  # 采样率
CHUNK = 2048  # 缓冲区大小


class AudioWsService(object):
    # 打开音频流
    stream: pyaudio.Stream = None
    audio_stream_data = []
    audio_buffer_index = 0
    audio_buffer_end_index = 0
    audio: pyaudio.PyAudio
    start_time = time.time()
    wav_file_path = None
    wav_audio = None
    wav_bytes = None
    is_loaded_wav = False
    is_recoding = False
    ws = None
    sample_count = 0

    def __init__(self):
        pass

    def init(self):
        print('init AudioWsService2')
        logger.info(f'AudioWsService 初始化')
        self.audio = pyaudio.PyAudio()
        self.is_recoding = True
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                                      rate=RATE, input=True,
                                      frames_per_buffer=CHUNK)
        baidu_uri = const.URI + "?sn=" + str(uuid.uuid1())
        ws_app2 = websocket.WebSocketApp(baidu_uri,
                                         on_open=self.on_open,  # 连接建立后的回调
                                         on_message=self.on_message,  # 接收消息的回调
                                         on_error=self.on_error,  # 库遇见错误的回调
                                         on_close=self.on_close)  # 关闭后的回调
        logger.info(f'AudioWsService 初始化2')
        threading.Thread(target=ws_app2.run_forever, daemon=True).start()

    def load_mp3_file(self, file_path):
        logger.info(f'加载{file_path}')
        self.is_loaded_wav = False
        self.wav_file_path = file_path

    def send_data_async(self, data_byte):
        if 'task_startup' in cache_tools.cache and cache_tools.cache['task_startup'] is True and self.ws is not None:
            self.ws.send(data_byte, websocket.ABNF.OPCODE_BINARY)

    def send_and_append_mp3_data(self, ws):
        if self.stream is None:
            return
        print("Recording...")
        logger.info("send_audio total={}")
        wav_audio = None
        wav_bytes = None
        logger.info(f"task_startup:{'task_startup' in cache_tools.cache}")
        while ('task_startup' in cache_tools.cache and cache_tools.cache['task_startup'] is True
               and self.is_recoding is True):
            # 读取录音数据
            record_audio_data = self.stream.read(CHUNK)
            threading.Thread(target=self.send_data_async, args=(record_audio_data,)).start()
            record_audio_data_tmp = record_audio_data
            if self.wav_file_path is not None:
                if not self.is_loaded_wav:
                    logger.info(f'读取wav文件：{self.wav_file_path[-6:]}')
                    wav_audio = AudioSegment.from_mp3(self.wav_file_path)
                    # duration_ms = len(wav_audio)
                    wav_audio = wav_audio.set_frame_rate(RATE).set_channels(CHANNELS)
                    # 将MP3音频转换为字节数据
                    wav_bytes = wav_audio.raw_data
                    start_time = time.time()
                    self.sample_count = 0
                    self.is_loaded_wav = True

                self.sample_count += CHUNK  # 更新采样总数
                # ------------------ ##
                # 计算自录音开始以来经过的时间。
                wav_start_frame = self.sample_count  # 当前采样点数就是音频的起始位置
                wav_start_byte = wav_start_frame * wav_audio.frame_width

                # 计算应从MP3文件中读取的字节的起始位置。mp3_start_frame * CHUNK * wav_audio.frame_width 计算对应的字节数。
                end_byte = wav_start_byte + CHUNK * wav_audio.frame_width

                if end_byte <= len(wav_bytes):
                    mp3_chunk = wav_bytes[wav_start_byte:end_byte]
                else:
                    mp3_chunk = wav_bytes[wav_start_byte:]  # 处理越界情况

                # 检查从MP3数据流中提取的数据块大小是否与当前录音数据块大小一致。如果一致，则进行数据混合。
                if len(mp3_chunk) == len(record_audio_data_tmp):
                    # print(f'{wav_start_byte}-{wav_start_byte + CHUNK * wav_audio.frame_width}')
                    # 将录音数据块和MP3数据块转换为NumPy数组，并将它们相加进行混合
                    combined_data = np.frombuffer(record_audio_data_tmp, dtype=np.int16) + np.frombuffer(mp3_chunk,
                                                                                                         dtype=np.int16)
                    record_audio_data_tmp = combined_data.tobytes()
            self.audio_stream_data.append(record_audio_data_tmp)
            if (self.audio_buffer_index == 0 and 'phone_state' in cache_tools.cache
                    and cache_tools.cache['phone_state'] == PhoneState.CHATTING.value):
                self.audio_buffer_index = len(self.audio_stream_data) - 1

            if (self.audio_buffer_index >= 0 and 'phone_state' in cache_tools.cache
                    and cache_tools.cache['phone_state'] == PhoneState.CHATTING.value):
                self.audio_buffer_end_index = len(self.audio_stream_data) - 1

    def send_start_params(self, ws):
        """
        开始参数帧
        :param websocket.WebSocket ws:
        :return:
        """
        req = {
            "type": "START",
            "data": {
                "appid": const.APPID,  # 网页上的appid
                "appkey": const.APPKEY,  # 网页上的appid对应的appkey
                "dev_pid": const.DEV_PID,  # 识别模型
                "cuid": "yourself_defined_user_id",  # 随便填不影响使用。机器的mac或者其它唯一id，百度计算UV用。
                "sample": 16000,  # 固定参数
                "format": "pcm"  # 固定参数
            }
        }
        body = json.dumps(req)
        ws.send(body, websocket.ABNF.OPCODE_TEXT)
        logger.info("send START frame with params:" + body)

    def send_audio(self, ws):
        """
        发送二进制音频数据，注意每个帧之间需要有间隔时间
        :param  websocket.WebSocket ws:
        :return:
        """
        if self.stream is None:
            return
        logger.info("send_audio data")
        self.send_and_append_mp3_data(ws)

    def save_audio(self, phone_num) -> str:
        if self.audio is None:
            logger.info('audio 未初始化')
        file_name = f'{phone_num}_{time_tools.now_str("%Y%m%d%H%M%S")}.wav'
        file_path = fr'{config.audio_file_save_path}\{file_name}'
        if len(self.audio_stream_data) > 0 and self.audio_buffer_index > 0:
            self.audio_stream_data = self.audio_stream_data[self.audio_buffer_index:self.audio_buffer_end_index]
            wave_file = wave.open(file_path, 'wb')
            wave_file.setnchannels(CHANNELS)
            wave_file.setsampwidth(self.audio.get_sample_size(FORMAT))
            wave_file.setframerate(RATE)
            wave_file.writeframes(b''.join(self.audio_stream_data))
            wave_file.close()
            time.sleep(1)
            logger.info(f"录音已保存为 {file_path}")
        else:
            logger.info('audio 录音数据长度为0')
        self.audio_stream_data.clear()
        self.audio_buffer_index = 0
        self.audio_buffer_end_index = 0
        return file_name

    def send_finish(self, ws):
        """
        发送结束帧
        :param websocket.WebSocket ws:
        :return:
        """
        req = {
            "type": "FINISH"
        }
        body = json.dumps(req)
        self.is_recoding = False
        ws.send(body, websocket.ABNF.OPCODE_TEXT)
        logger.info("send FINISH frame")

    def send_cancel(self, ws):
        """
        发送取消帧
        :param websocket.WebSocket ws:
        :return:
        """
        req = {
            "type": "CANCEL"
        }
        body = json.dumps(req)
        ws.send(body, websocket.ABNF.OPCODE_TEXT)
        logger.info("send Cancel frame")

    def on_open(self, ws):
        self.ws = ws
        """
            连接后发送数据帧
            :param  websocket.WebSocket ws:
            :return:
            """

        def run(*args):
            self.send_start_params(ws)
            self.send_audio(ws)
            self.send_finish(ws)
            logger.info("thread terminating")

        threading.Thread(target=run).start()

    def on_message(self, ws, message):
        """
            接收服务端返回的消息
            :param ws:
            :param message: json格式，自行解析
            :return:
            """
        # {"err_no":0,"err_msg":"OK","log_id":1163673784,
        # "sn":"7d188ebf-4707-11ef-84fd-e4c7671e02e8_ws_0","type":"MID_TEXT","result":"北京科技","start_time":640,"end_time":2700}
        message_json = json.loads(message)
        if message_json["err_no"] == 0:
            # 成功收到反馈，输出内容
            receive_txt = message_json["result"]
            logger.info(receive_txt)
            if 'last_call_phone_num' in cache_tools.cache:
                timestamp = time.time()
                phone_num = cache_tools.cache["last_call_phone_num"]
                if len(cache_tools.cache[f'chat_all_txt_{phone_num}']) > 0 and \
                        cache_tools.cache[f'chat_all_txt_{phone_num}'][-1] in receive_txt:
                    cache_tools.cache[f'chat_all_txt_{phone_num}'][-1] = receive_txt
                else:
                    cache_tools.cache[f'chat_all_txt_{phone_num}'].append(receive_txt)
                cache_tools.cache[f'chat_json_{phone_num}'] = {'timestamp': timestamp,
                                                               'chat_txt': receive_txt}
        elif message_json["err_no"] == -3005:
            logger.info('no word send or receive')
        else:
            logger.info("Response: " + message)

    def on_error(self, ws, error):
        """
            库的报错，比如连接超时
            :param ws:
            :param error: json格式，自行解析
            :return:
                """
        if error.args[0] != 'err_no':
            logger.error(f"error2: {error}")

    def on_close(self, ws, a, b):
        """
            Websocket关闭
            :param websocket.WebSocket ws:
            :return:
            """
        logger.info(f"ws close ...{a}###{b},rest_time={cache_tools.cache['rest_time']}")
        ws.close()
        # 非休息时间，如果ws被关了，则任务结束
        if cache_tools.cache['rest_time'] is False:
            logger.info('非休息时间，暂停任务')
            cache_tools.cache['task_startup'] = False

    log_colors_config = {
        'DEBUG': 'white',
        'INFO': 'white',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }

    def stop_recording(self):
        logger.info('stop_recording')
        self.is_recoding = False
        logger.info('stop_recording2')
        self.stream.stop_stream()
        logger.info('stop_recording3')
        self.stream.close()
        logger.info('stop_recording4')
        self.audio.terminate()
        logger.info('stop_recording5')


    def test_speech_ws_status(self):
        cache_tools.cache['task_startup'] = False
        cache_tools.cache["last_call_phone_num"] = '999'
        cache_tools.cache[f'chat_json_999'] = ''
        cache_tools.cache["chat_all_txt_999"] = []
        test_mp3_file = r'C:\Users\jiang\PycharmProjects\xianyu_spider\audios\test_speech_to_word.mp3'
        # 读取 MP3 文件并转换成字节数据
        mp3_audio = AudioSegment.from_mp3(test_mp3_file)
        mp3_audio = mp3_audio.set_frame_rate(16000).set_channels(1)
        chunk_size = 1024  # 每次发送的字节大小
        start_byte = 0

        while start_byte < len(mp3_audio.raw_data):
            chunk = mp3_audio.raw_data[start_byte:start_byte + chunk_size]
            self.send_data_async(chunk)
            start_byte += chunk_size
            time.sleep(0.05)  # 每隔一段时间发送一块数据
        time.sleep(1)
        result = cache_tools.cache[f'chat_json_999']
        logger.info(f'返回结果：{result}')
        if 'chat_txt' in result and result['chat_txt'] != '测试语音识别':
            logger.info(f'测试失败，停止任务，测试结果：{result}')
            cache_tools.cache['task_startup'] = False
        else:
            cache_tools.cache['task_startup'] = True

    # 配置日志格式


class NoColorFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)
        return message  # 去掉任何颜色控制字符


if __name__ == "__main__":
    aud = AudioWsService()
    aud.init()
    cache_tools.init()
    cache_tools.cache['task_startup'] = True
    cache_tools.cache["last_call_phone_num"] = '999'

    aud.test_speech_ws_status()
    time.sleep(5)
    aud.stop_recording()
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
