from peewee import *
import datetime
from app.models import CallTask  # 假设 CallTask 模型已经定义在 models.py 中
from playhouse.shortcuts import model_to_dict
from dao import call_task_dao


class CallTaskService:
    def __init__(self):
        self.model = CallTask

    def create_task(self, task_code, area_name, task_status, default_choose):
        try:
            if default_choose == 'ok':
                call_task_dao.update_call_task_choose()
            task = self.model.create(
                task_code=task_code,
                area_name=area_name,
                task_status=task_status,
                default_choose=default_choose,
                insert_datetime=datetime.datetime.now(),
                update_datetime=datetime.datetime.now()
            )

            return task
        except Exception as e:
            print(f"Error creating task: {e}")
            return None

    def get_task_by_id(self, task_code):
        try:
            task = self.model.get(self.model.task_code == task_code)
            return task
        except self.model.DoesNotExist:
            return None
        except Exception as e:
            print(f"Error retrieving task: {e}")
            return None

    def update_task(self, task_code, **kwargs):
        try:
            if 'default_choose' in kwargs and kwargs['default_choose'] == 'ok':
                call_task_dao.update_call_task_choose()
            kwargs['update_datetime'] = datetime.datetime.now()  # 更新修改时间
            return call_task_dao.update_call_task(task_code, **kwargs)  # 返回 True 如果有记录被更新
        except Exception as e:
            print(f"Error updating task: {e}")
            return False

    def delete_task(self, task_id):
        try:
            query = self.model.delete().where(self.model.id == task_id)
            rows_deleted = query.execute()
            return rows_deleted > 0  # 返回 True 如果有记录被删除
        except Exception as e:
            print(f"Error deleting task: {e}")
            return False

    def list_tasks(self, page, page_size):
        try:
            tasks = self.model.select().order_by(self.model.id.desc()).paginate(page, page_size)
            all_data = []
            for page_call_task in tasks:
                record_dict = model_to_dict(page_call_task)
                if page_call_task.insert_datetime:
                    record_dict['insert_datetime'] = page_call_task.insert_datetime.strftime('%Y-%m-%d %H:%M:%S')
                if page_call_task.update_datetime:
                    record_dict['update_datetime'] = page_call_task.update_datetime.strftime('%Y-%m-%d %H:%M:%S')
                all_data.append(record_dict)
            return all_data
        except Exception as e:
            print(f"Error listing tasks: {e}")
            return []
