# 推荐放在一个新的 service 文件中，例如 speech_word_service.py
from peewee import *
import datetime
from app.models import SpeechWord  # 导入更新后的 SpeechWord 模型
from playhouse.shortcuts import model_to_dict

class SpeechWordService:
    def __init__(self):
        """初始化时，指定要操作的模型"""
        self.model = SpeechWord

    def create_speech_word(self, txt, txt_no, ok_no, no_no, hesitate_no, community_name, keys):
        """
        创建一个新的话术记录。
        """
        try:
            speech_word = self.model.create(
                txt=txt,
                txt_no=txt_no,
                ok_no=ok_no,
                no_no=no_no,
                hesitate_no=hesitate_no,
                community_name=community_name,
                keys=keys,
                insert_datetime=datetime.datetime.now(),
                update_datetime=datetime.datetime.now()
            )
            return speech_word
        except Exception as e:
            print(f"Error creating speech word: {e}")
            return None

    def get_speech_word_by_id(self, speech_word_id):
        """
        根据 ID 获取单个话术记录。
        """
        try:
            speech_word = self.model.get_by_id(speech_word_id)
            return speech_word
        except self.model.DoesNotExist:
            return None
        except Exception as e:
            print(f"Error retrieving speech word: {e}")
            return None

    def update_speech_word(self, speech_word_id, **kwargs):
        """
        根据 ID 更新话术记录。
        """
        try:
            kwargs['update_datetime'] = datetime.datetime.now()
            query = self.model.update(**kwargs).where(self.model.id == speech_word_id)
            rows_updated = query.execute()
            return rows_updated > 0
        except Exception as e:
            print(f"Error updating speech word: {e}")
            return False

    def delete_speech_word(self, speech_word_id):
        """
        根据 ID 删除话术记录。
        """
        try:
            query = self.model.delete().where(self.model.id == speech_word_id)
            rows_deleted = query.execute()
            return rows_deleted > 0
        except Exception as e:
            print(f"Error deleting speech word: {e}")
            return False

    def list_speech_words(self, page, page_size):
        """
        分页列出所有话术记录。
        """
        try:
            speech_words = self.model.select().order_by(self.model.id.desc()).paginate(page, page_size)
            all_data = []
            for speech_word in speech_words:
                record_dict = model_to_dict(speech_word)
                if speech_word.insert_datetime:
                    record_dict['insert_datetime'] = speech_word.insert_datetime.strftime('%Y-%m-%d %H:%M:%S')
                if speech_word.update_datetime:
                    record_dict['update_datetime'] = speech_word.update_datetime.strftime('%Y-%m-%d %H:%M:%S')
                all_data.append(record_dict)
            return all_data
        except Exception as e:
            print(f"Error listing speech words: {e}")
            return []