# -*- coding: utf-8 -*-
import subprocess
from service.audio.enum_const import PhoneState
import os
import re

# SWJB8DGMPJO7MBBY
# 9889d548433144334f  三星s8
device_id = 'x8helvhifmizqwj7'


def off_call():
    adb_command = f"adb -s {device_id} shell input keyevent KEYCODE_ENDCALL"

    # 执行 ADB 命令
    result = subprocess.run(adb_command, shell=True, capture_output=True, text=True)

    # 打印执行结果
    if result.returncode == 0:
        print("手机执行电话挂断指令成功")
    else:
        print(f"执行off_call()命令时出错: {result.stderr}")


def call_num(phone_num):
    adb_command = f"adb -s {device_id} shell am start -a android.intent.action.CALL -d tel:{phone_num}"
    os.system(adb_command)


def get_call_state():
    if device_id == 'SWJB8DGMPJO7MBBY':
        return get_lian_call_status()
    # Run the adb shell dumpsys telecom command
    result = subprocess.run(['adb', '-s', device_id, 'shell', 'dumpsys', 'telecom'], stdout=subprocess.PIPE, text=True, encoding='utf-8')
    # Get the output as a string
    output = result.stdout
    # Process each line of the output
    for line in output.splitlines():
        if 'com.android.services.telephony.TelephonyConnectionService' in line:
            # Check the state of the call in the mCalls section
            if 'DIALING' in line:
                return PhoneState.CALLING.value
            elif 'ACTIVE' in line:
                return PhoneState.CHATTING.value
            elif 'RINGING' in line:
                return PhoneState.RINGING.value
        elif 'mCallAudioManager:' in line:
            # If mCalls is empty, the phone is free
            return PhoneState.FREE.value
    return PhoneState.UNKNOWN.value


def get_lian_call_status():
    try:
        # 执行 adb 命令获取 telecom 服务日志
        output = subprocess.check_output(
            ["adb", '-s', device_id, "shell", "dumpsys", "telecom"],
            text=True,
            stderr=subprocess.STDOUT, encoding='utf-8'
        )

        # 正则匹配 CallsManager 的 mCalls 字段
        call_match = re.search(r'CallsManager:.*?mCalls:.*?,\s*([A-Z]+)\b', output, re.DOTALL)

        if call_match:
            call_state = call_match.group(1)
            if 'ACTIVE' in call_state:
                return PhoneState.CHATTING.value
            elif 'DIALING' in call_state:
                return PhoneState.CALLING.value
            elif 'RINGING' in call_state:
                return PhoneState.RINGING.value
        return PhoneState.FREE.value

    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e.output}")
        return PhoneState.UNKNOWN.value
    except Exception as e:
        print(f"未知错误: {str(e)}")
        return PhoneState.UNKNOWN.value


def close_wifi(my_device_id):
    adb_command = f"adb -s {my_device_id} shell svc wifi disable"
    os.system(adb_command)


def open_wifi(my_device_id):
    adb_command = f"adb -s {my_device_id} shell svc wifi enable"
    os.system(adb_command)


def get_battery_level(my_device_id=device_id):
    try:
        # 执行 ADB 命令
        result = subprocess.run(['adb', '-s', my_device_id, 'shell', 'dumpsys', 'battery'], capture_output=True,
                                text=True, check=True, encoding='utf-8')
        output = result.stdout

        # 查找电量信息
        for line in output.splitlines():
            if 'level' in line:
                level = line.split(':')[-1].strip()
                return int(level)
        return -1
    except subprocess.CalledProcessError as e:
        print(f"执行 ADB 命令时出错: {e}")
    except ValueError:
        print("无法解析电量信息")
    except Exception as e:
        print(f"发生未知错误: {e}")
    return -2


if __name__ == '__main__':

    # print(call_num(18807101234))
    # print(get_call_state())
    # print(get_lian_call_status())
    print(get_battery_level(device_id))
    pass
