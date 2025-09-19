from dao import speech_phone_num_dao


def query_with_conditions(phone_num, phone_status, start_datetime, end_datetime, task_code, sort_field='id',
                          sort_order='asc',
                          page_index=1,
                          page_size=20):
    return speech_phone_num_dao.query(phone_num, phone_status, start_datetime, end_datetime, task_code, sort_field,
                                      sort_order,
                                      page_index, page_size)


def update_status(task_code, phone_status_param, **kwargs):
    return speech_phone_num_dao.update_status(task_code=task_code, phone_status_param=phone_status_param, **kwargs)


def del_with_conditions(ids=None, phone_num=None, phone_status=None, start_datetime=None, end_datetime=None):
    return speech_phone_num_dao.delete_speech_phone_num(ids, phone_num, phone_status, start_datetime, end_datetime)


def save_batch(data):
    return speech_phone_num_dao.save_batch(data)


def delete_duplicate(start_datetime):
    return speech_phone_num_dao.delete_duplicate(start_datetime)


def update_phone_num_1_2_same(task_code):
    return speech_phone_num_dao.update_phone_num_1_2_same(task_code)


def update_status_with_join(task_code, start_date, end_date):
    return speech_phone_num_dao.update_status_with_join(task_code, start_date, end_date)
