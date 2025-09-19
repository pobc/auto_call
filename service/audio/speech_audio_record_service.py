from dao import speech_audio_record_dao
from app.models import SpeechAudioRecord
from utils import logging_tools

logger = logging_tools.get_logger()


def query_with_conditions(phone_num=None, start_datetime=None, end_datetime=None, intention_level=None, talk_count=None,
                          task_code=None,
                          sort_field='id', sort_order='asc',
                          start=1,
                          length=20):
    return speech_audio_record_dao.query_with_task(phone_num, start_datetime, end_datetime, intention_level, talk_count,
                                                   task_code,
                                                   sort_field, sort_order,
                                                   start, length)


def del_with_conditions(record_id):
    return speech_audio_record_dao.delete_record(record_id)


def save(audio_file_name, phone_num, call_datetime, talk_times, duration, off_datetime, intention_level, audio_txt):
    save_record = SpeechAudioRecord.create(audio_file_name=audio_file_name, phone_num=phone_num,
                                           call_datetime=call_datetime,
                                           talk_times=talk_times, duration=duration, off_datetime=off_datetime,
                                           intention_level=intention_level, audio_txt=audio_txt)
    return speech_audio_record_dao.insert_record(save_record)


def update_record(record_id, audio_txt, is_checked, intention_level):
    return speech_audio_record_dao.update_record(record_id, audio_txt, is_checked, intention_level)


def get_record_count(talk_times, insert_datetime):
    return speech_audio_record_dao.get_record_count(talk_times, insert_datetime)


if __name__ == '__main__':
    logger.info('fdsafwe')
    pass
