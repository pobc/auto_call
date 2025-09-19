import time
from datetime import datetime

from app.main import main
from flask import render_template, Blueprint, redirect, jsonify, flash, request, send_from_directory
from service.audio import speech_phone_num_service, speech_audio_record_service, call_task_service, speech_service
from service import xianyu_service, config_dict_dao
import pandas as pd
from utils import time_tools, win_api_tools
import threading

data_blue = Blueprint('data', __name__, url_prefix='/data')


@main.route('/data/get_speech_phone_num', methods=['GET'])
def get_speech_phone_num():
    phone_num = request.args.get('phone_num')
    phone_status = request.args.get('phone_status')
    start_datetime = request.args.get('start_date')
    end_datetime = request.args.get('end_date')
    task_code = request.args.get('task_code')
    sort_field = request.args.get('sort_field', type=str, default='id')
    sort_order = request.args.get('sort_order', type=str, default='desc')

    start = int(request.args.get('start', 0))  # 起始记录数
    length = int(request.args.get('length', 10))  # 每页显示的记录数
    draw = int(request.args.get('draw', 1))  # 请求计数器
    result = speech_phone_num_service.query_with_conditions(phone_num, phone_status, start_datetime, end_datetime,
                                                            task_code,
                                                            sort_field,
                                                            sort_order,
                                                            start, length)
    result['draw'] = draw
    return result


@main.route('/data/update_speech_phone_num', methods=['POST'])
def update_speech_phone_num():
    task_code = request.form['task_code']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    # 回收未接的
    update_count_missed = speech_phone_num_service.update_status(task_code=task_code, phone_status_param='missed',
                                                                 phone_status='wait', start_date=start_date,
                                                                 end_date=end_date)

    # 回收，对话次数为0的
    update_count_0_talk = speech_phone_num_service.update_status_with_join(task_code=task_code,
                                                                           start_date=start_date,
                                                                           end_date=end_date)
    return {'code': 1, 'count': update_count_missed + update_count_0_talk, 'update_count_0_talk': update_count_0_talk}


@main.route('/data/save_speech_phone_num', methods=['POST'])
def save_speech_phone_num():
    file = request.files['file']
    task_code = request.form['task_code']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and file.filename.endswith('.xlsx'):
        dtype_dict = {
            '电话号码1': str,
            '电话号码2': str,
        }

        # 直接从文件对象中读取Excel数据
        df = pd.read_excel(file, dtype=dtype_dict)
        df = df[df['电话号码1'].notna()]
        dataset = []
        save_count = 0
        update_phone_1_2_same = 0
        # 遍历Excel内容并保存到数据库
        for index, row in df.iterrows():
            phone_num = row['电话号码1']
            phone_num2 = row['电话号码2']
            house_area = row['小区名字']
            house_num = row['门牌号']
            dataset.append({"phone_num": phone_num, "phone_num2": phone_num2, "phone_status": 'wait',
                            "house_area": house_area, "house_num": house_num, 'task_code': task_code})
        # 手动过滤掉为 None 的字段
        del_count = 0
        filtered_data = []
        for item in dataset:
            if item['phone_num'] is None:
                continue
            filtered_item = {k: v for k, v in item.items() if v is not None}  # 过滤掉值为 None 的字段
            filtered_data.append(filtered_item)
        if len(filtered_data) > 0:
            last_day = time_tools.get_previous_date(10).strftime('%Y-%m-%d 00:00:00')
            save_count = speech_phone_num_service.save_batch(filtered_data)
            del_count = speech_phone_num_service.delete_duplicate(last_day)
            update_phone_1_2_same = speech_phone_num_service.update_phone_num_1_2_same(task_code=task_code)
        return {'code': 1, 'save_count': save_count, 'del_count': del_count,
                'update_phone_1_2_same': update_phone_1_2_same}


@main.route('/data/delete_speech_phone_num', methods=['POST'])
def del_speech_phone_num():
    ids = request.get_json().get('ids', None)
    count = speech_phone_num_service.del_with_conditions(ids=ids)
    return {'code': 1, 'count': count}


@main.route('/data/get_speech_audio_record', methods=['GET'])
def get_speech_audio_record():
    phone_num = request.args.get('phone_num')
    start_datetime = request.args.get('start_date')
    end_datetime = request.args.get('end_date')

    intention_level = request.args.get('intention_level')
    talk_count = request.args.get('talk_count')
    task_code = request.args.get('task_code')
    sort_field_index = request.args.get('order[0][column]', 'duration')
    sort_field = request.args.get(f'columns[{sort_field_index}][data]', type=str, default='id')
    sort_order = request.args.get('order[0][dir]', type=str, default='desc')

    start = int(request.args.get('start', 0))  # 起始记录数
    length = int(request.args.get('length', 10))  # 每页显示的记录数
    draw = int(request.args.get('draw', 1))  # 请求计数器
    record_datetime = time.time()
    result = speech_audio_record_service.query_with_conditions(phone_num, start_datetime, end_datetime, intention_level,
                                                               talk_count, task_code, sort_field,
                                                               sort_order, start, length)
    result['draw'] = draw
    return result


@main.route('/data/test_page', methods=['GET'])
def test_page():
    return render_template('test.html')


@main.route('/<task_code>/file/<filename>')
def get_file(task_code, filename):
    return send_from_directory(f'audio_record_files/{task_code}', filename)


@main.route('/file/<filename>')
def get_file2(filename):
    return send_from_directory(f'audio_record_files', filename)


"""
对任务的增 删 改 查
"""


@main.route('/data/get_call_task', methods=['GET'])
def get_call_task():
    page_index = int(request.args.get('page_index', 0))  # 起始记录数
    length = int(request.args.get('length', 10))  # 每页显示的记录数
    draw = int(request.args.get('draw', 1))  # 请求计数器
    local_call_task_service = call_task_service.CallTaskService()
    result = local_call_task_service.list_tasks(page_index, length)
    return {'code': 1, 'data': result, 'page_index': page_index, 'length': length, 'draw': draw}


# 创建新任务
@main.route('/data/add_call_task', methods=['POST'])
def add_task():
    # if request.is_json:
    # data = request.json
    task_code = request.form.get('task_code')
    area_name = request.form.get('area_name')
    task_status = request.form.get('task_status')
    default_choose = request.form.get('default_choose')
    local_call_task_service = call_task_service.CallTaskService()
    result = local_call_task_service.create_task(task_code=task_code, area_name=area_name, task_status=task_status,
                                                 default_choose=default_choose)
    return {'code': 1, 'message': 'ok', 'id': result.id}


# 更新任务
@main.route('/data/update_call_task', methods=['POST'])
def update_task():
    local_call_task_service = call_task_service.CallTaskService()
    task_code = request.form.get('task_code', None)
    area_name = request.form.get('area_name', None)
    default_choose = request.form.get('default_choose', None)
    task_status = request.form.get('task_status', None)

    update_datetime = datetime.now()
    # stop 已经处理
    result = local_call_task_service.update_task(task_code, area_name=area_name,
                                                 task_status=task_status,
                                                 update_datetime=update_datetime, default_choose=default_choose)
    win_api_tools.set_system_volume(volume_level=70)
    print(f"Active threads: {threading.active_count()}")
    if task_status == 'processing':
        thread = threading.Thread(target=speech_service.start_task_tmp, args=(task_code,))
        thread.daemon = True  # 将线程设为守护线程
        thread.start()

    return {'code': 1, 'count': result}


# 删除任务
@main.route('/data/delete_call_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    local_call_task_service = call_task_service.CallTaskService()
    count = local_call_task_service.delete_task(task_id)
    return {'code': 1, 'count': count}


@main.route('/data/update_speech_audio_record', methods=['POST'])
def update_phone_num_status():
    record_id = request.form['record_id']
    audio_txt = request.form.get('audio_txt', None)
    is_checked = request.form.get('is_checked', None)
    intention_level = request.form.get('intention_level', None)
    update_record_count = speech_audio_record_service.update_record(record_id, audio_txt, is_checked, intention_level)
    return {'code': 1, 'count': update_record_count}


@main.route('/data/get_xianyu_item', methods=['GET'])
def get_xianyu_item():
    config_result = config_dict_dao.query_last_config_info('xianyu_web')
    status = 'stop'
    if len(config_result) > 0 and config_result[0]['val'] == 'start':
        status = 'start'
        result = xianyu_service.query_new_house_no_detail()
        if len(result) > 0:
            print(f"没有详情的数据有{len(result)}条")
            return {"status": status, "data": result}
    return {"status": status}
