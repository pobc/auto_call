import pyaudio
import wave
import ffmpeg
import numpy as np

# 配置音频
FORMAT = pyaudio.paInt16  # 音频格式
CHANNELS = 2  # 立体声
RATE = 16000  # 采样率
CHUNK = 1024  # 缓冲区大小
RECORD_SECONDS = 3  # 录音时长
WAVE_OUTPUT_FILENAME = "../service/audio/output.wav"
MP3_OUTPUT_FILENAME = "output.mp3"


def record_audio():
    audio = pyaudio.PyAudio()

    # 打开音频流
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Recording...")
    print(f'stream.is_active():{stream.is_active()}')
    print(f'stream.is_stopped()：{stream.is_stopped()}')
    frames = []

    # 录音
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    # 停止和关闭音频流
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # print(stream.is_active())
    # print(stream.)
    # 保存为WAV文件
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def convert_wav_to_mp3():
    input_file = WAVE_OUTPUT_FILENAME
    output_file = MP3_OUTPUT_FILENAME

    # 使用ffmpeg将wav转换为mp3
    ffmpeg.input(input_file).output(output_file).run(overwrite_output=True)
    print(f"File converted and saved as {output_file}")


if __name__ == "__main__":
    record_audio()
    # convert_wav_to_mp3()
    pass
