import unittest
from utils.DBUtils import DBUtils


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_executeMany(self):
        sql = "insert into test(id,name, name2) values(%s,%s,%s)"
        data = [(1, '2室1厅1卫', 'faeee'),(2, '2室1厅1卫', 'faeee')]
        DBUtils.executeMany(sql, data)
        self.assertEqual(True, True)

    def test_executeMany(self):
        """
        sql = "insert into house_list(itemId,desc,imageUrls,lastVisitTimeDesc,price,locationDetails) values(%s,%s,%s,%s,%s,%s)"
        data = [('754501293859', '323', '2', '30分钟前', '850', '位于洪山区')]
        """
        sql = "insert into house_list(`desc`) values ( %s) "
        data = [( 'few')]
        DBUtils.executeMany(sql, data)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
