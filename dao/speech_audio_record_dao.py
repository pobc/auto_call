import datetime
import math
import time
from peewee import JOIN

# SpeechCallRecord 模型
from app.models import SpeechAudioRecord, SpeechPhoneNum
from playhouse.shortcuts import model_to_dict
from utils import time_tools


# 插入数据
def insert_record(speech_audio_record: SpeechAudioRecord):
    return speech_audio_record.save()


# 查询所有记录
def get_all_records():
    all_records = SpeechAudioRecord.select()
    return list(all_records)


def query_with_task(phone_num, start_datetime, end_datetime, intention_level, talk_count, task_code, sort_field='id',
                    sort_order='desc',
                    start=1,
                    length=10):
    record_datetime = time.time()
    query1 = (SpeechAudioRecord
              .select(SpeechAudioRecord, SpeechPhoneNum.id.alias('phone_num_id'), SpeechPhoneNum.task_code,
                      SpeechPhoneNum.phone_status, SpeechPhoneNum.house_num, SpeechPhoneNum.house_area)
              .join(SpeechPhoneNum, JOIN.INNER, on=(SpeechPhoneNum.phone_num == SpeechAudioRecord.phone_num))
              .where(SpeechPhoneNum.task_code == task_code))

    query2 = (SpeechAudioRecord
              .select(SpeechAudioRecord, SpeechPhoneNum.id.alias('phone_num_id'), SpeechPhoneNum.task_code,
                      SpeechPhoneNum.phone_status, SpeechPhoneNum.house_num, SpeechPhoneNum.house_area)
              .join(SpeechPhoneNum, JOIN.INNER, on=(SpeechPhoneNum.phone_num2 == SpeechAudioRecord.phone_num))
              .where(SpeechPhoneNum.task_code == task_code))

    # Add filters to both queries
    if start_datetime:
        query1 = query1.where(SpeechAudioRecord.insert_datetime >= start_datetime)
        query2 = query2.where(SpeechAudioRecord.insert_datetime >= start_datetime)

    if end_datetime:
        query1 = query1.where(SpeechAudioRecord.insert_datetime <= end_datetime)
        query2 = query2.where(SpeechAudioRecord.insert_datetime <= end_datetime)

    if phone_num:
        query1 = query1.where(SpeechAudioRecord.phone_num == phone_num)
        query2 = query2.where(SpeechAudioRecord.phone_num == phone_num)

    if intention_level:
        query1 = query1.where(SpeechAudioRecord.intention_level == int(intention_level))
        query2 = query2.where(SpeechAudioRecord.intention_level == int(intention_level))

    if talk_count:
        talk_count = int(talk_count)
        query1 = query1.where(SpeechAudioRecord.talk_times >= talk_count)
        query2 = query2.where(SpeechAudioRecord.talk_times >= talk_count)

    # Combine queries using UNION
    query_result = query1.union_all(query2)
    if sort_order == 'asc':
        query_result = query_result.order_by(getattr(SpeechAudioRecord, sort_field).asc())
    else:
        query_result = query_result.order_by(getattr(SpeechAudioRecord, sort_field).desc())

    #  paginated_results = query_result.paginate(page=start, paginate_by=length)
    total_count = query_result.count()
    # 获取分页后的数据
    paginated_results = query_result.offset(start).limit(length)

    total_pages = math.ceil(total_count / length)

    all_data = []
    for page_record in paginated_results:
        record_dict = model_to_dict(page_record)
        record_dict['house_area'] = page_record.speechphonenum.house_area
        record_dict['house_num'] = page_record.speechphonenum.house_num
        if page_record.insert_datetime:
            record_dict['insert_datetime'] = page_record.insert_datetime.strftime('%Y-%m-%d %H:%M:%S')
        if page_record.call_datetime:
            record_dict['call_datetime'] = page_record.call_datetime.strftime('%Y-%m-%d %H:%M:%S')

        all_data.append(record_dict)
    return {
        'data': all_data,
        'recordsFiltered': total_count,
        'recordsTotal': total_pages,
        'total_pages': total_pages,
        'current_page': start / length
    }


def query(phone_num, start_datetime, end_datetime, intention_level, talk_count, sort_field='id', sort_order='desc',
          start=1,
          length=10):
    query_result = SpeechAudioRecord.select()

    if start_datetime:
        query_result = query_result.where(
            (SpeechAudioRecord.insert_datetime >= start_datetime))
    if end_datetime:
        query_result = query_result.where(SpeechAudioRecord.insert_datetime <= end_datetime)
    if phone_num:
        query_result = query_result.where(SpeechAudioRecord.phone_num == phone_num)

    if intention_level:
        query_result = query_result.where(SpeechAudioRecord.intention_level == int(intention_level))

    if talk_count:
        talk_count = int(talk_count)
        if talk_count >= 6:
            query_result = query_result.where(SpeechAudioRecord.talk_times >= talk_count)
        else:
            query_result = query_result.where(SpeechAudioRecord.talk_times == talk_count)

    if sort_order == 'asc':
        query_result = query_result.order_by(getattr(SpeechAudioRecord, sort_field).asc())
    else:
        query_result = query_result.order_by(getattr(SpeechAudioRecord, sort_field).desc())

    total_count = query_result.count()
    total_pages = math.ceil(total_count / length)

    paginated_results = query_result.offset(start).limit(length)
    all_data = []
    for page_record in paginated_results:
        record_dict = model_to_dict(page_record)
        if page_record.insert_datetime:
            record_dict['insert_datetime'] = page_record.insert_datetime.strftime('%Y-%m-%d %H:%M:%S')
        if page_record.call_datetime:
            record_dict['call_datetime'] = page_record.call_datetime.strftime('%Y-%m-%d %H:%M:%S')
        all_data.append(record_dict)

    return {
        'data': all_data,
        'recordsFiltered': total_count,
        'recordsTotal': total_pages,
        'total_pages': total_pages,
        'current_page': start / length
    }


# 查询单条记录
def get_record_by_id(record_id):
    try:
        record_info = SpeechAudioRecord.get(SpeechAudioRecord.id == record_id)
        return record_info
    except SpeechAudioRecord.DoesNotExist:
        print("Record not found.")
        return None


# 条件查询
def get_records_by_phone(phone_num):
    records_info = SpeechAudioRecord.select().where(SpeechAudioRecord.phone_num == phone_num)
    return list(records_info)


# 更新数据
def update_record(record_id, audio_txt, is_checked, intention_level):
    # 动态构建更新字段
    update_data = {}
    if audio_txt is not None:
        update_data[SpeechAudioRecord.audio_txt] = audio_txt
    if is_checked is not None:
        update_data[SpeechAudioRecord.is_checked] = is_checked
    if intention_level is not None:
        update_data[SpeechAudioRecord.intention_level] = intention_level
    # 检查是否有字段需要更新
    if update_data:
        update_prepare = SpeechAudioRecord.update(update_data).where(SpeechAudioRecord.id == record_id)
        rows_updated = update_prepare.execute()
        return rows_updated
    else:
        return 0


# 删除数据
def delete_record(record_id):
    query_result = SpeechAudioRecord.delete().where(SpeechAudioRecord.id == record_id)
    deleted_rows = query_result.execute()
    if deleted_rows > 0:
        print(f"Record ID {record_id} deleted.")
    else:
        print(f"No record found with ID {record_id}.")
    return deleted_rows


# 获取数据的总数量
def get_record_count(talk_times, insert_datetime):
    query_result = SpeechAudioRecord.select()
    query_result = query_result.where(
        (SpeechAudioRecord.insert_datetime >= insert_datetime) & (SpeechAudioRecord.talk_times >= talk_times))
    count = query_result.count()
    print(f'Total records: {count}')
    return count


# 主程序
if __name__ == "__main__":
    # 示例操作
    # insert_record(123456789, '/path/to/audio.mp3', 120, 'Transcribed text of the audio')
    #
    # records = get_all_records()
    # for record in records:
    #     print(record.phone_num, record.audio_path)
    #
    # record = get_record_by_id(1)
    # if record:
    #     print(record.audio_txt)

    print(update_record(1, 'Updated transcribed text', 1))

    # delete_record(1)
    #
    # total_records = get_record_count()
