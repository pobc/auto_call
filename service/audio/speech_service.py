from dao import speech_dao
from utils import adb_tools, cache_tools, play_game_tools, logging_tools, time_tools
from service.audio.audio_local_service import AudioLocalService
from service.audio.enum_const import CustomLevel

import time
import datetime
import threading
from service.audio.enum_const import PhoneState
from service.audio.call_task_service import CallTaskService
from service.audio import speech_audio_record_service
from main import config

audio_file_path = r'C:\Users\jiang\PycharmProjects\xianyu_spider\audios'
logger = logging_tools.get_logger()
audio_service: AudioLocalService


def init():
    cache_tools.init(100)
    cache_tools.cache['task_startup'] = True
    cache_tools.cache['test'] = config.speech_test_phone_num
    cache_tools.cache['rest_time'] = False
    cache_tools.cache["last_call_phone_num"] = config.speech_test_phone_num

    cache_tools.cache[f"chat_all_txt_{config.speech_test_phone_num}"] = ''

    play_game_tools.init()
    global audio_service
    print("AudioWsService init success")
    audio_service = AudioLocalService()
    audio_service.init()
    # audio_service.test_speech_ws_status()
    # 单独一个线程 监控电话状态
    threading.Thread(target=monitor_phone_state).start()


def receive_positive_keywords():
    return ['出租', '好的', '租啊', '去租', '租不租', '能不能租', '可以', '有的', '搜猪']


def receive_negative_keywords():
    return ['不出租', '自住', '自己住', '自己句', '没有', '卖掉', '卖了', '自己做', '自己', '啊没', '字句', '不用',
            '挂了', '记住', '不错', '冒的', '冇得', '冒得',
            '自助', '语音助手', '智能助理', '不需要', '录音超时']


def check_busy(phone_num):
    chat_txt = cache_tools.cache[f'chat_last_txt_{phone_num}']
    if '正在通话' in chat_txt and get_talk_duration_seconds(phone_num) < 3:
        logger.info('检测到通话中')
        return True
    return False


def check_person_keywords(phone_num):
    chat_txt = cache_tools.cache[f'chat_all_txt_{phone_num}']
    for keyword in ['暂时无人接听', '录音超时', '无法接通', '号码是空号', '用户正忙', 'busy', '用户已关机',
                    '电话已停机', '已开通来电应急防护', '正在忙线中', '用户已暂停服务']:
        if keyword in chat_txt:
            return True
    return False


def file_path_concat(num_str):
    num = str(num_str).lower()
    return fr'{audio_file_path}\{num}.mp3'


def monitor_phone_state():
    while cache_tools.cache['task_startup']:
        cache_tools.cache['phone_state'] = adb_tools.get_call_state()
        time.sleep(1)


def my_play_sound(voice_num):
    if adb_tools.get_call_state() != PhoneState.CHATTING.value:
        return 0
    file_path = file_path_concat(voice_num)
    audio_service.load_mp3_file(file_path)
    sound_second = play_game_tools.play_sound(file_path)
    time.sleep(1.2)
    return sound_second


def reset_chat_cache_json(phone_num):
    cache_tools.cache[f'chat_last_timestamp_{phone_num}'] = time.time()
    cache_tools.cache[f'chat_last_txt_{phone_num}'] = ''


def get_talk_duration_seconds(phone_num):
    return time_tools.time_diff_now(cache_tools.cache[f'chat_last_timestamp_{phone_num}'], precision=3)


def check_speech_num_finish(txt_no):
    if txt_no in ['w1', 'w29', 'q5', 'q7', 'q9', 'q12', 'missed'] \
            or ('phone_state' in cache_tools.cache and cache_tools.cache['phone_state'] == PhoneState.RINGING.value):
        logger.info('结束，挂机')
        return True


def wait_charge():
    power_level = adb_tools.get_battery_level()
    while power_level <= 5:
        logger.info('电量低于5%，休息')
        time.sleep(60 * 1)
        if power_level > 20:
            logger.info('电量低于大于20，开始任务')
            break


def process_audio_and_txt(phone_num, phone_info_id, task_code):
    chat_times = 0
    txt_no = task_code + '_q1'
    logger.info('开始执行 play_audio_by_keys()')
    my_voice_duration_seconds = 0
    reset_chat_cache_json(phone_num)
    # 呼叫等待
    time.sleep(1)
    logger.info(f'手机状态：{adb_tools.get_call_state()}')
    logger.info(f'等待接听')
    call_start_time = time.time()
    cache_tools.cache[f'{phone_num}_intention_level'] = CustomLevel.MISSED.value
    call_time = 0
    # and f'{phone_num}_intention_level' not in cache_tools.cache
    while adb_tools.get_call_state() == PhoneState.CALLING.value:
        wait_period = 0.5
        time.sleep(wait_period)
        if check_busy(phone_num):
            adb_tools.off_call()
            if call_time == 0:
                call_time += 1
                time.sleep(2)
                logger.info('通话中，再次拨打')
                adb_tools.call_num(phone_num)
                time.sleep(2)
            else:
                logger.info('第二次通话中')
                return {'num': 'w1', 'status': 'busy', 'chat_times': chat_times, 'call_duration': 0}
        elif time.time() - call_start_time > 60 or check_person_keywords(phone_num):
            adb_tools.off_call()
            logger.info('无人接听或者等待超过1分钟，挂机')
            speech_dao.update_speech_phone_num(['missed', phone_info_id])
            return {'num': 'w1', 'status': 'missed', 'chat_times': chat_times, 'call_duration': 0}
    talk_start_time = time.time()
    cache_tools.cache[f'word_matching_count_{phone_num}'] = 0
    cache_tools.cache[f'txt_num_use_record_{phone_num}'] = []
    cache_tools.cache[f'{phone_num}_intention_level'] = CustomLevel.MAYBE.value
    reset_chat_cache_json(phone_num)
    while adb_tools.get_call_state() == PhoneState.CHATTING.value:
        chat_times += 1
        cache_tools.cache[f'txt_num_use_record_{phone_num}'].append(txt_no)
        is_done = False
        if chat_times == 1:
            logger.info('接听4')
            logger.info('接通了，开始播放收条语言')
            my_voice_duration_seconds = my_play_sound(task_code + '_q1')

        if check_speech_num_finish(txt_no) \
                or ('phone_state' in cache_tools.cache and cache_tools.cache['phone_state'] == PhoneState.RINGING.value) \
                or (time.time() - talk_start_time > 60 * 2):
            logger.info('结束，挂机')
            return {'num': txt_no, 'status': '', 'chat_times': chat_times,
                    'call_duration': time.time() - talk_start_time}
        logger.info(f'这是第{chat_times}次对话循环，使用的语音编号{txt_no}, 播放的语音时长{my_voice_duration_seconds}')
        # 播放语音后，等待回复
        logger.info(f'与最近的回复 相差：{get_talk_duration_seconds(phone_num)} 秒')
        while get_talk_duration_seconds(phone_num) < 1.5 and time.time() - talk_start_time < 60:
            time.sleep(0.1)
            continue
        duration_seconds = get_talk_duration_seconds(phone_num)
        logger.info(f'上次回复到现在，等待了{duration_seconds}秒')
        call_wait_seconds = round(duration_seconds - my_voice_duration_seconds, 3)
        # 当有回复内容之后，如果等待超过1秒，没有回复，则继续循环
        if 5 < call_wait_seconds < 15:
            logger.info(f'播放等待录音 已经等待{call_wait_seconds}秒')
            my_voice_duration_seconds = my_play_sound('w46')
            continue
        elif call_wait_seconds - my_voice_duration_seconds > 15:
            adb_tools.off_call()
            logger.info('一直没有回复，挂断')
            return {'num': 'w1', 'status': 'silence', 'chat_times': chat_times,
                    'call_duration': time.time() - talk_start_time}
        time.sleep(0.1)
        txt = cache_tools.cache[f'chat_last_txt_{phone_num}']
        speech_word = speech_dao.query_speech_word(txt_no)[0]
        logger.info(f'当前编号 {txt_no}')
        logger.info(f'收到的回复：{txt}')
        # 否定
        for keyword in receive_negative_keywords():
            if str(txt).rfind(keyword) > -1:
                txt_no = speech_word['no_no']
                is_done = True
                logger.info(f'{txt_no} 否定回答 is_done={is_done}')
                if speech_word['no_no'] is not None:
                    my_voice_duration_seconds = my_play_sound(speech_word['no_no'])
                # 保存意向等级
                if task_code + '_q1' == txt_no:
                    cache_tools.cache[f'{phone_num}_intention_level'] = CustomLevel.REJECT.value
                break
        if is_done:
            continue
        # 肯定
        for keyword in receive_positive_keywords():
            if str(txt).rfind(keyword) > -1:
                logger.info(f'{txt_no} 肯定回复')
                my_voice_duration_seconds = my_play_sound(speech_word['ok_no'])
                if task_code + '_q1' == txt_no:
                    cache_tools.cache[f'{phone_num}_intention_level'] = CustomLevel.OK.value
                txt_no = speech_word['ok_no']
                is_done = True
                break
        if is_done:
            continue
        all_keywords = speech_dao.query_speech_word_all_keys()
        for keyword_info in all_keywords:
            goon_current_loop = True
            for key in str(keyword_info['keys']).split(','):
                library_txt_no = keyword_info['txt_no']
                talk_num_key = f'{phone_num}_talk_num_{library_txt_no}'
                key = key.replace(' ', '')
                if str(txt).rfind(key) > -1 and talk_num_key not in cache_tools.cache:
                    cache_tools.cache[talk_num_key] = 1
                    txt_no = library_txt_no
                    logger.info(f'{library_txt_no} 的关键字被触发')
                    my_voice_duration_seconds = my_play_sound(library_txt_no)
                    is_done = True
                    goon_current_loop = False
                    break
            if not goon_current_loop:
                break
        if is_done:
            continue
        # 所有关键字都没匹配到
        logger.info(f'等待{call_wait_seconds}秒后，没有匹配到')
        if len(txt) > 0 and cache_tools.cache[f'word_matching_count_{phone_num}'] >= 1:
            logger.info(f'{phone_num}两次没有匹配到词库,结束')
            my_play_sound('w1')
            return {'num': 'w1', 'status': 'no_word', 'chat_times': chat_times,
                    'call_duration': time.time() - talk_start_time}
        elif len(txt) > 0:
            cache_tools.cache[f'word_matching_count_{phone_num}'] += 1
            txt_no = 'q2'
            my_voice_duration_seconds = my_play_sound(txt_no)
        else:
            time.sleep(0.2)
    return {'num': 'w1', 'status': '', 'chat_times': chat_times, 'call_duration': time.time() - talk_start_time}


def start_task_tmp(task_code):
    try:
        start_task(task_code)
    except Exception as e:
        logger.info('start_task任务执行，发生异常')
        logger.error(e)


def start_task(task_code, is_test=False):
    wait_charge()
    call_task_service = CallTaskService()
    call_task_service.update_task(task_code, task_status='processing')
    phone_list = speech_dao.query_speech_phone_num([task_code, 'wait'])

    test_phone_list = [
        {'house_are': 'test', 'id': 1, 'insert_datetime': None, 'phone_num': config.speech_test_phone_num, 'phone_num2': config.speech_test_phone_num,
         'phone_status': 'wait',
         'update_datetime': '2024-07-29 14:26:00'},
        # {'house_are': '远洋', 'id': 1, 'insert_datetime': None, 'phone_num': '', 'phone_num': '',
        # 'phone_status': 'wait',
        #  'update_datetime': '2024-07-29 14:26:00'}
    ]

    if phone_list and len(phone_list) > 0 or is_test is True:
        init()
        if is_test:
            phone_list = test_phone_list
        else:
            phone_list = test_phone_list + phone_list

        logger.info(f'电话数据条数{len(phone_list)}')
        for idx, phone_info in enumerate(phone_list):
            # 超过晚上9点，或者超过指定点记录数，则停止呼叫
            valid_call_count = speech_audio_record_service.get_record_count(talk_times=1,
                                                                            insert_datetime=time_tools.now_str(
                                                                                '%Y-%m-%d'))
            if datetime.datetime.now().hour >= 21 or valid_call_count > 1000:
                logger.info('到达指定任务')
                break
            if idx >= 50 and idx % 50 == 0:
                rest_seconds = 1 * 60
                cache_tools.cache['rest_time'] = True
                time.sleep(2)
                logger.info(f'循环至第{idx}个电话，休息{rest_seconds / 60}分钟')
                audio_service.stop_recording()
                time.sleep(rest_seconds)
                cache_tools.cache['rest_time'] = False
                logger.info('休息结束')
                init()
            task_info = call_task_service.get_task_by_id(task_code)
            if task_info.task_status == 'stop':
                break
            cache_tools.cache['task_startup'] = True
            # 更新手机号状态
            speech_dao.update_speech_phone_num(['used', phone_info['id']])
            multi_phone_num = [phone_info['phone_num'], phone_info['phone_num2']]
            for nextIdx, current_phone_num in enumerate(multi_phone_num):
                phone_num = current_phone_num
                if phone_num is None or len(phone_num) != 11:
                    if nextIdx == 0:
                        speech_dao.update_speech_phone_num(['error', phone_info['id']])
                    logger.info('手机号格式不对')
                    continue
                call_datetime = time_tools.now_str()
                # 只有电话在空闲状态，才拨打电话
                if adb_tools.get_call_state() != PhoneState.FREE.value:
                    adb_tools.off_call()
                logger.info(f'开始第{idx + 1}个中的第{nextIdx + 1}个，拨打电话:{phone_num}，共{len(phone_list)}个电话')
                # 初始化，开始拨打电话的时间戳
                cache_tools.cache[f'chat_last_txt_{phone_num}'] = ''
                cache_tools.cache[f'chat_last_timestamp_{phone_num}'] = time.time()
                cache_tools.cache['last_call_phone_num'] = phone_num
                cache_tools.cache[f'chat_all_txt_{phone_num}'] = ''
                adb_tools.call_num(phone_num)
                # 根据内容，匹配话术，播放录音
                # ####### 开始任务 #############
                result = process_audio_and_txt(phone_num=phone_num,
                                               phone_info_id=phone_info['id'], task_code=task_code)
                logger.info(f'循环结束 返回结果{result}')
                # 如果到了 Q12，挂断电话
                # if check_speech_num_finish(result['num']):
                adb_tools.off_call()
                # 保存录音、识别记录
                audio_file_save_path = audio_service.save_audio(phone_num, task_code)
                speech_dao.insert_data_audio_record(
                    [f'/{task_code}/file/' + audio_file_save_path, phone_num, call_datetime, result['chat_times'],
                     result['call_duration'],
                     time_tools.now_str(), cache_tools.cache[f'{phone_num}_intention_level'],
                     cache_tools.cache[f'chat_all_txt_{phone_num}'], result['status']])
                if result['status'] != 'missed':
                    # 如果第一个号码 接通了，则不再拨打第一个电话
                    break

        # 有任务的情况下，才需要更新
        call_task_service.update_task(task_code, task_status='stop')
        logger.info('电话任务循环结束')
        cache_tools.cache['task_startup'] = False
        time.sleep(2)
        audio_service.stop_recording()
    else:
        logger.info("没有发现电话任务")


if __name__ == '__main__':
    # start_task('jindigelindongjun', is_test=True)
    # txt = '行情行情'
    # all_keywords = speech_dao.query_speech_word_all_keys()
    # for keyword_info in all_keywords:
    #     goon_current_loop = True
    #     for key in str(keyword_info['keys']).split(','):
    #         library_txt_no = keyword_info['txt_no']
    #         talk_num_key = f'{188}_talk_num_{library_txt_no}'
    #         if str(txt).rfind(key) > -1:
    #             print('11111111111')
    # logger.info(__name__)
    pass
