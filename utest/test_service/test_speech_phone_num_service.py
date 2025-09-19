import unittest
from service.audio import speech_phone_num_service
from utils import time_tools


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_something_else(self):
        datetime_7_ago = time_tools.get_previous_date(7)
        print(speech_phone_num_service.update_status_with_join('yuanyang', datetime_7_ago))
        self.assertEqual(True, True)

    def test_delete_duplicate(self):
        datetime_7_ago = time_tools.get_previous_date(3)
        speech_phone_num_service.delete_duplicate(datetime_7_ago)
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
