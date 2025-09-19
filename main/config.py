import platform
import os

dev_local_path = r'C:\Users\jiang\PycharmProjects\auto_call'
log_path = dev_local_path + r"\\logs\\readEmail.log"
local_mode = platform.node() == 'Jiang'

audio_file_save_path = r"C:\Users\jiang\PycharmProjects\xianyu_spider\app\audio_record_files"

speech_test_phone_num = 18807101234

if not local_mode:
    speech_test_phone_num = 18807102447

db_config ={
    'host': '127.0.0.1',
    'user': 'root',
    'pwd': 'jiang',
    'database': 'xianyu',
    'port': '3306',
}