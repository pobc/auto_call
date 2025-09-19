from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import ctypes
import comtypes


def set_system_volume(volume_level=70):
    # 初始化 COM 库
    comtypes.CoInitialize()

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
    # 设置音量，范围是 0.0（静音）到 1.0（最大音量）
    volume_level = max(0.0, min(1.0, volume_level / 100.0))  # 保证值在0到1之间
    volume.SetMasterVolumeLevelScalar(volume_level, None)

    # 取消静音
    if volume.GetMute():  # 检查当前是否静音
        volume.SetMute(0, None)  # 设置静音为 0（即关闭静音）

if __name__ == '__main__':
    # 设置音量为 70%
    set_system_volume(70)