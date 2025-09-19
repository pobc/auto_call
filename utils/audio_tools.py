import pyaudio
import numpy as np

# 设置参数
CHUNK = 1024  # 每个数据块的帧数
FORMAT = pyaudio.paInt16  # 采样深度
CHANNELS = 1  # 单声道
RATE = 44100  # 采样率

# 初始化PyAudio
p = pyaudio.PyAudio()

# 打开麦克风流
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("开始录制...")

try:
    while True:
        # 读取音频数据
        data = stream.read(CHUNK)

        # 将音频数据转换为numpy数组
        audio_data = np.frombuffer(data, dtype=np.int16)

        # 计算音频数据的均方根（RMS）值
        rms = np.sqrt(np.mean(audio_data ** 2))

        # 设置一个阈值，判断是否有人在说话
        threshold = 500  # 可以根据实际情况调整阈值

        if rms > threshold:
            print("检测到有人在说话")
        else:
            print("静音")
except KeyboardInterrupt:
    print("录制结束")

# 关闭流
stream.stop_stream()
stream.close()
p.terminate()
