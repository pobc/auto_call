from app import get_logger, get_config
import math
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import utils
from app.models import CfgNotify
from app.main.forms import CfgNotifyForm
from . import main
from app.views import data_views

from service import haiju_house_service
from utils import time_tools

logger = get_logger(__name__)
cfg = get_config()


# 通用列表查询
def common_list(DynamicModel, view):
    # 接收参数
    action = request.args.get('action')
    id = request.args.get('id')
    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length')) if request.args.get('length') else cfg.ITEMS_PER_PAGE

    # 删除操作
    if action == 'del' and id:
        try:
            DynamicModel.get(DynamicModel.id == id).delete_instance()
            flash('删除成功')
        except:
            flash('删除失败')

    # 查询列表
    query = DynamicModel.select()
    total_count = query.count()

    # 处理分页
    if page: query = query.paginate(page, length)

    dict_data = {'content': utils.query_to_list(query), 'total_count': total_count,
                 'total_page': math.ceil(total_count / length), 'page': page, 'length': length}
    return render_template(view, form=dict_data, current_user=current_user)


# 通用单模型查询&新增&修改
def common_edit(DynamicModel, form, view):
    id = request.args.get('id', '')
    if id:
        # 查询
        model = DynamicModel.get(DynamicModel.id == id)
        if request.method == 'GET':
            utils.model_to_form(model, form)
        # 修改
        if request.method == 'POST':
            if form.validate_on_submit():
                utils.form_to_model(form, model)
                model.save()
                flash('修改成功')
            else:
                utils.flash_errors(form)
    else:
        # 新增
        if form.validate_on_submit():
            model = DynamicModel()
            utils.form_to_model(form, model)
            model.save()
            flash('保存成功')
        else:
            utils.flash_errors(form)
    return render_template(view, form=form, current_user=current_user)


# 根目录跳转
@main.route('/', methods=['GET'])
@login_required
def root():
    return redirect(url_for('main.index'))


# 首页
@main.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('index.html', current_user=current_user)


# 通知方式查询
@main.route('/phone_num_list', methods=['GET', 'POST'])
def notifylist():
    return common_list(CfgNotify, 'phone_num_list.html')


@main.route('/task_list', methods=['GET', 'POST'])
def task_list():
    return common_list(CfgNotify, 'phone_task_list.html')


# 通知方式配置
@main.route('/task_list', methods=['GET', 'POST'])
def notifyedit():
    return common_edit(CfgNotify, CfgNotifyForm(), 'phone_task_list.html')


@main.route('/test', methods=['GET', 'POST'])
def test():
    return "fafdsf"


@main.route('/house/<house_code>')
def house_detail(house_code):
    house_detail_info = haiju_house_service.get_info_detail(house_code)
    context = {}
    if house_detail_info['code'] == 0:
        data = house_detail_info['data']
        # 处理时间戳
        warrant_end_time = '0'
        if data['warrant_end_time'] != '0':
            warrant_end_time = time_tools.timestamp_to_date_str(data['warrant_end_time'])

        rent_time_end = time_tools.timestamp_to_date_str(data['rent_time_end'])
        # 整理数据传递给模板
        context = {
            'community_title': data['community_title'],
            'rent_amount': data['rent_amount'] / 10000,
            'real_build_area': data['real_build_area'],
            'real_house_type_title': data['real_house_type_title'],
            'locker_type_title': data['locker_type_title'],
            'has_key': '有钥匙' if data['has_key'] == 1 else '没有钥匙',
            'rent_container': data['house_rent_container_val']['title'],
            'min_lease_title': data['min_lease_title'],
            'warrant_end_time': warrant_end_time,
            'rent_time_end': rent_time_end,
            'warrant_status': data['warrant_status'],
            'landlord_phone': data['landlord_phone'],
            'house_code': data['house_code'],
            'door_number': data['door_number']
        }

    return render_template('haiju_house_info.html', **context)
