from datetime import datetime

from peewee import fn

from app.models import SpeechPhoneNum, SpeechAudioRecord
from playhouse.shortcuts import model_to_dict
import math


def query(phone_num, phone_status, start_datetime, end_datetime, task_code, sort_field='id', sort_order='asc',
          page_index=1,
          page_size=20):
    query_result = SpeechPhoneNum.select()
    if phone_status and len(phone_status) > 1:
        query_result = query_result.where(SpeechPhoneNum.phone_status == phone_status)

    if start_datetime:
        query_result = query_result.where(
            (SpeechPhoneNum.update_datetime >= start_datetime))
    if end_datetime:
        query_result = query_result.where(SpeechPhoneNum.update_datetime <= end_datetime)
    if phone_num:
        query_result = query_result.where(
            (SpeechPhoneNum.phone_num == phone_num) | (SpeechPhoneNum.phone_num2 == phone_num))

    query_result = query_result.where(SpeechPhoneNum.task_code == task_code)
    if not sort_field:
        sort_field = 'id'

    if sort_order == 'asc':
        query_result = query_result.order_by(getattr(SpeechPhoneNum, sort_field).asc())
    else:
        query_result = query_result.order_by(getattr(SpeechPhoneNum, sort_field).desc())

    total_count = query_result.count()
    total_pages = math.ceil(total_count / page_size)

    paginated_results = query_result.offset(page_index).limit(page_size)
    all_data = []
    for record in paginated_results:
        record_dict = model_to_dict(record)
        if record.insert_datetime:
            record_dict['insert_datetime'] = record.insert_datetime.strftime('%Y-%m-%d %H:%M:%S')
        if record.update_datetime:
            record_dict['update_datetime'] = record.update_datetime.strftime('%Y-%m-%d %H:%M:%S')
        all_data.append(record_dict)
    return {
        'data': all_data,
        'recordsFiltered': total_count,
        'recordsTotal': total_count,
        'total_pages': total_pages,
        'current_page': page_index / page_size
    }


def save(phone_num, phone_status, house_are):
    return SpeechPhoneNum.create(
        phone_num=phone_num,
        phone_status=phone_status,
        house_are=house_are,
        insert_datetime=datetime.now(),
        update_datetime=datetime.now()
    )


def save_batch(data_list):
    prepare_insert = SpeechPhoneNum.insert_many(data_list)
    return prepare_insert.execute()


def update_status(task_code, phone_status_param, **kwargs):
    kwargs['update_datetime'] = datetime.now()  # 更新修改时间
    fields = [field.name for field in SpeechPhoneNum._meta.sorted_fields]
    fields_to_update = {key: value for key, value in kwargs.items() if value is not None and key in fields}
    update_prepare = SpeechPhoneNum.update(**fields_to_update).where(
        (SpeechPhoneNum.task_code == task_code) & (SpeechPhoneNum.phone_status == phone_status_param) & (
                SpeechPhoneNum.update_datetime >= kwargs['start_date']) & (
                SpeechPhoneNum.update_datetime <= kwargs['end_date']))
    rows_updated = update_prepare.execute()

    return rows_updated


def update_status_with_join(task_code, start_date, end_date):
    # 开始事务
    with SpeechPhoneNum._meta.database.atomic():
        # 执行更新
        with SpeechPhoneNum._meta.database.atomic():
            # 子查询：找到有 talk_times != 0 的 phone_num
            exclude_phone_nums = (
                SpeechAudioRecord
                .select(SpeechAudioRecord.phone_num)
                .where(
                    (SpeechAudioRecord.talk_times != 0) &
                    (SpeechAudioRecord.insert_datetime >= start_date) &
                    (SpeechAudioRecord.insert_datetime <= end_date)
                )
            )

            # 主查询：更新 phone_status
            prepare_update = (
                SpeechPhoneNum
                .update(phone_status='wait')
                .where(
                    (SpeechPhoneNum.phone_status == 'used') &
                    (SpeechPhoneNum.task_code == task_code) &
                    (SpeechPhoneNum.phone_num.in_(
                        SpeechAudioRecord
                        .select(SpeechAudioRecord.phone_num)
                        .where(
                            ((SpeechAudioRecord.talk_times == 0) |
                             (SpeechAudioRecord.audio_txt.contains("语音留言")) |
                             (SpeechAudioRecord.audio_txt.contains("通话中")) |
                             (SpeechAudioRecord.audio_txt.contains("助理"))) &
                            (SpeechAudioRecord.insert_datetime >= start_date) &
                            (SpeechAudioRecord.insert_datetime <= end_date) &
                            (~SpeechAudioRecord.phone_num.in_(exclude_phone_nums))  # 排除有 talk_times != 0 的 phone_num
                        )
                    ))
                )
            )
        # 执行更新并获取影响的记录数
        updated_count = prepare_update.execute()
    return updated_count


def delete_speech_phone_num(ids, phone_num, phone_status, start_datetime, end_datetime):
    query_result = SpeechPhoneNum.delete()
    if not ids and not phone_num and not start_datetime:
        return 0

    if ids and len(ids) > 0:
        query_result = query_result.where(SpeechPhoneNum.id.in_(ids))
    if phone_status:
        query_result = query_result.where(SpeechPhoneNum.phone_status == phone_status)
    if end_datetime:
        query_result = query_result.where(
            (SpeechPhoneNum.insert_datetime >= start_datetime) & (SpeechPhoneNum.insert_datetime <= end_datetime))
    if phone_num:
        query_result = query_result.where(SpeechPhoneNum.phone_num == phone_num)

    return query_result.execute()


def delete_duplicate(start_datetime):
    # 删除重复记录中 id比较大的
    sql = """
    DELETE s.*
    FROM speech_phone_num s
    INNER JOIN (
        SELECT phone_num, MIN(id) AS min_id
        FROM speech_phone_num
        WHERE insert_datetime > %s
        GROUP BY phone_num
        HAVING COUNT(*) > 1
    ) t ON s.phone_num = t.phone_num AND s.id != t.min_id
    WHERE s.insert_datetime > %s;
    """
    with SpeechPhoneNum._meta.database.atomic():
        deleted_count = SpeechPhoneNum._meta.database.execute_sql(sql, (start_datetime, start_datetime)).rowcount
        print(f'已删除 {deleted_count} 条记录')

    return deleted_count


def update_phone_num_1_2_same(task_code):
    return (SpeechPhoneNum
            .update(phone_num2='nan')
            .where((SpeechPhoneNum.phone_num == SpeechPhoneNum.phone_num2) &
                   (SpeechPhoneNum.task_code == task_code))
            .execute())
