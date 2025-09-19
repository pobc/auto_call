import unittest

from dao import call_task_dao


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_update_call_task_choose(self):
        print(call_task_dao.update_call_task_choose())
        self.assertEqual(True, True)

    def test_update_task(self):

        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
