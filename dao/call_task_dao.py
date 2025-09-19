import datetime
from app.models import CallTask


def create_call_task(task_code, area_name):
    record = CallTask.create(
        task_code=task_code,
        area_name=area_name,
        insert_datetime=datetime.datetime.now(),
        update_datetime=datetime.datetime.now()
    )
    return record


def get_call_task_by_id(task_id):
    try:
        record = CallTask.get(CallTask.id == task_id)
        return record
    except CallTask.DoesNotExist:
        return None


def update_call_task_choose():
    return CallTask.update({'default_choose': 'no'}).where(CallTask.default_choose == 'ok').execute()


def update_call_task(task_code, **kwargs):
    kwargs['update_datetime'] = datetime.datetime.now()  # 更新修改时间
    fields_to_update = {key: value for key, value in kwargs.items() if value is not None}
    query = CallTask.update(**fields_to_update).where(CallTask.task_code == task_code)
    rows_updated = query.execute()
    return rows_updated


def delete_call_task(task_code):
    query = CallTask.delete().where(CallTask.task_code == task_code)
    rows_deleted = query.execute()
    return rows_deleted
