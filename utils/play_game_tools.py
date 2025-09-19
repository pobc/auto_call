import time, os

import pygame
from utils import cache_tools
from service.audio.enum_const import PhoneState

from pydub import AudioSegment
import simpleaudio as sa
import sounddevice as sd


def init():
    # 初始化 pygame
    pygame.mixer.init()


def get_audio_device_index(device_name):
    devices = sd.query_devices()
    for idx, device in enumerate(devices):
        print(devices)
        if device_name in device['name']:
            return idx
    return None


def play_sound(file_path):
    # 加载 MP3 文件
    pygame.mixer.music.load(file_path)
    # 播放 MP3 文件
    pygame.mixer.music.play()

    # 保持程序运行直到音乐播放完毕
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    audio = None
    if file_path.endswith('.mp3'):
        audio = AudioSegment.from_mp3(file_path)
    elif file_path.endswith('.wav'):
        audio = AudioSegment.from_wav(file_path)
    duration_ms = len(audio)
    duration_seconds = duration_ms / 1000.0
    return duration_seconds


def play_mp3(file_path, device_name):
    # 加载 MP3 文件
    audio = AudioSegment.from_mp3(file_path)
    # 获取音频设备索引
    device_index = get_audio_device_index(device_name)
    if device_index is None:
        print(f"Device '{device_name}' not found.")
        return

    # 播放音频
    playback = sa.play_buffer(
        audio.raw_data,
        num_channels=audio.channels,
        bytes_per_sample=audio.sample_width,
        sample_rate=audio.frame_rate,
        device=device_index
    )
    playback.wait_done()


def convert_mp3_to_wav(mp3_path, wav_path):
    try:
        audio = AudioSegment.from_mp3(mp3_path)
        audio.export(wav_path, format="wav")
        print(f"Converted {mp3_path} to {wav_path}")
    except Exception as e:
        print(f"Failed to convert {mp3_path}: {e}")


def convert_directory_mp3_to_wav(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):
            mp3_path = os.path.join(directory, filename)
            wav_filename = os.path.splitext(filename)[0] + ".wav"
            wav_path = os.path.join(directory, wav_filename)
            convert_mp3_to_wav(mp3_path, wav_path)


if __name__ == '__main__':
    init()
    cache_tools.init()
    # print(get_audio_device_index('外部麦克风 (Realtek(R) Audio), MME (2 in, 0 out)'))
    # print(play_sound(r'C:\Users\jiang\PycharmProjects\xianyu_spider\audios\q2.mp3'))
    convert_directory_mp3_to_wav(r'C:\Users\jiang\PycharmProjects\xianyu_spider\audios')

    # 示例用法
    # file_path = "path_to_your_mp3_file.mp3"
    # device_name = "耳机设备名称"  # 根据实际情况填写耳机设备名称
    # play_mp3(file_path, device_name)
    pass
