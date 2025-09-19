import pyaudio
import wave
import ffmpeg
import time
import numpy as np
from pydub import AudioSegment
from utils import cache_tools, time_tools

# 配置音频
FORMAT = pyaudio.paInt16  # 音频格式
CHANNELS = 1  # 立体声
RATE = 16000  # 采样率
CHUNK = 1024 * 2  # 缓冲区大小
RECORD_SECONDS = 10  # 录音时长
WAVE_OUTPUT_FILENAME = "../service/audio/output.wav"
MP3_OUTPUT_FILENAME = "output.mp3"

wav_file_path = r'C:\Users\jiang\PycharmProjects\xianyu_spider\audios\yuanyang_q1.mp3'


def record_audio():
    audio = pyaudio.PyAudio()

    # 打开音频流
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Recording...")

    chunk_ms = 160 /1000  # 每帧间隔
    task_start_time = time.time()
    audio_stream_data = []

    wav_audio = AudioSegment.from_mp3(wav_file_path)
    duration_ms = len(wav_audio)
    print('本地音频长度 {} 秒'.format(duration_ms))
    wav_audio = wav_audio.set_frame_rate(RATE).set_channels(CHANNELS)
    # 将MP3音频转换为字节数据
    wav_bytes = wav_audio.raw_data
    start_time = time.time()
    while time.time() - task_start_time < RECORD_SECONDS:
        loop_start_time = time.time()  # 记录每次循环的开始时间
        # 读取录音数据
        pcm = stream.read(CHUNK)
        print(f'spend time:{time.time() - loop_start_time}')
        # 发送录音
        data = pcm
        # ------------------ ##
        # 计算自录音开始以来经过的时间。
        elapsed_time = time.time() - start_time

        wav_start_frame = int(elapsed_time * RATE / CHUNK)
        # 计算应从MP3文件中读取的字节的起始位置。mp3_start_frame * CHUNK * wav_audio.frame_width 计算对应的字节数。
        wav_start_byte = wav_start_frame * CHUNK * wav_audio.frame_width
        # 计算应从MP3文件中读取的字节的起始位置。mp3_start_frame * CHUNK * wav_audio.frame_width 计算对应的字节数。
        mp3_chunk = wav_bytes[wav_start_byte:wav_start_byte + CHUNK * wav_audio.frame_width]
        print(f'{wav_start_byte}-{wav_start_byte + CHUNK * wav_audio.frame_width}')
        # 检查从MP3数据流中提取的数据块大小是否与当前录音数据块大小一致。如果一致，则进行数据混合。
        if len(mp3_chunk) == len(data):
            # print('组合音频数据')
            # 将录音数据块和MP3数据块转换为NumPy数组，并将它们相加进行混合
            combined_data = np.frombuffer(data, dtype=np.int16) + np.frombuffer(mp3_chunk, dtype=np.int16)
            data = combined_data.tobytes()
        audio_stream_data.append(data)
        # 计算循环执行时间
        # loop_duration = time.time() - loop_start_time
        # sleep_time = max(0, chunk_ms - loop_duration)  # 计算需要等待的时间
        # print(f'sleep time: {sleep_time}')
        #time.sleep(sleep_time)

    save_audio(audio_stream_data, audio)


def save_audio(audio_byte_data, audio):
    file_name = f'test_{time_tools.now_str("%Y%m%d%H%M%S")}.wav'
    file_path = fr'C:\Users\jiang\PycharmProjects\xianyu_spider\utest\{file_name}'
    if len(audio_byte_data) > 0:
        wave_file = wave.open(file_path, 'wb')
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(audio.get_sample_size(FORMAT))
        wave_file.setframerate(RATE)
        wave_file.writeframes(b''.join(audio_byte_data))
        wave_file.close()
        time.sleep(1)
        audio_byte_data = []
        print(f"录音已保存为 {file_path}")
    else:
        print('audio 录音数据长度为0')


if __name__ == "__main__":
    record_audio()
    # convert_wav_to_mp3()
    pass
