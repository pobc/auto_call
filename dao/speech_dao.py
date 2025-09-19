from utils.DBUtils import DBUtils

"""
关键字匹配，播放音频
记录录音、手机号、拨号时间、对话次数、挂断方
关键字，肯定录音  否定录音 挽回录音
"""


def insert_data_speech(data):
    """插入数据"""
    insert_speech_word = """
        INSERT INTO speech_word (txt, txt_no, ok_no, no_no, hesitate_no, community_name, `keys`)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    return DBUtils.execute(insert_speech_word, data)


def update_speech_word(data):
    return DBUtils.execute("""
    UPDATE speech_word
    SET txt = %s
    WHERE id = %s
    """, data)


def delete_speech_word(data):
    return DBUtils.execute("DELETE FROM speech_word WHERE id = %s", data)


def query_speech_word_all_keys():
    return DBUtils.execute("SELECT * FROM speech_word where `keys` is not null order by id asc")


def query_speech_word(data):
    return DBUtils.execute("SELECT * FROM speech_word where txt_no=%s", data)


def insert_data_audio_record(data):
    """插入数据"""
    insert_speech_audio_record = """
       INSERT INTO speech_audio_record (audio_file_name, phone_num, call_datetime, talk_times, duration, off_datetime, 
                                        intention_level, audio_txt, call_status)
       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
       """
    return DBUtils.execute(insert_speech_audio_record, data)


def update_speech_audio_record(data):
    return DBUtils.execute("""
    UPDATE speech_audio_record
    SET audio_file_name = %s
    WHERE id = %s
    """, data)


def delete_speech_audio_record(data):
    return DBUtils.execute("DELETE FROM speech_audio_record WHERE id = %s", data)


def query_speech_audio_record(data):
    return DBUtils.execute("SELECT * FROM speech_audio_record", data)


def insert_data_phone_num(data):
    """插入数据"""
    insert_speech_phone_num = """
      INSERT INTO speech_phone_num (phone_num, insert_datetime, phone_status,house_are)
    VALUES (%s, %s, %s, %s)
       """
    return DBUtils.execute(insert_speech_phone_num, data)


def update_speech_phone_num(data):
    return DBUtils.execute("""
    UPDATE speech_phone_num
    SET  update_datetime = now(), phone_status = %s
    WHERE id = %s
    """, data)


def delete_speech_phone_num(data):
    return DBUtils.execute("DELETE FROM speech_phone_num WHERE id = %s", data)


def query_speech_phone_num(data):
    return DBUtils.execute(
        "SELECT * FROM speech_phone_num where task_code=%s and (phone_status is null or phone_status=%s)", data)


if __name__ == '__main__':
    # print(query_speech_word_all_keys())
    # print(query_speech_word('q1')[0]['txt_no'])
    # print(query_speech_word('feicui_q1'))
    txt = '行情行情'
    all_keywords = query_speech_word_all_keys()
    for keyword_info in all_keywords:
        goon_current_loop = True
        for key in str(keyword_info['keys']).split(','):
            print(key)
            if txt.rfind(str(key)) > -1:
                print(3333)
                is_done = True
                goon_current_loop = False
                break
        if not goon_current_loop:
            break
    pass
