import unittest

import datetime
from service.audio import speech_audio_record_service


class MyTestCase(unittest.TestCase):
    def test_query_with_conditions(self):
        print(speech_audio_record_service.query_with_conditions(start_datetime='2024-12-17', end_datetime='2024-12-23',
                                                                talk_count=1, start=1, length=10,
                                                                task_code='shilixincheng'))
        self.assertEqual(True, True)

    def test_get_record_count(self):
        talk_times = 1
        insert_datetime = '2024-12-24'
        print(datetime.datetime.now().hour)
        print(speech_audio_record_service.get_record_count(talk_times, insert_datetime))

        self.assertEqual(True, True)
