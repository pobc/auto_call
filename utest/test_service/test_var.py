import time
import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        print(2 in [1, 3])

        for i in range(10):
            for j in range(10):
                print(f"{i}   {j}")
                if i > 3 and j > 3:
                    break
                    break
        self.assertEqual(True, True)  # add assertion here

    def test_json(self):
        a = {'a': {'b': {'c': 3}}}
        a['a']['b']['e'] = 4
        # print(['a']['b'] in a)
        print(a)
        abc = 'fasdfsa'
        abc = abc.replace('a', '1')
        print(abc)
        self.assertEqual(True, True)

    def test_encode(self):
        err = KeyError('error_no')
        aa = {'timestamp': 0, 'chat_txt': 1}
        bb = aa['timestamp']
        for i in range(20):
            time.sleep(1)
            bb = '99'
            print(aa)
        print(err.args[0])
        pass

    def test_arr(self):
        print(160 / 1000)
        print(160 / 1000.0)
        txt_no = 'w1'
        print('=====')
        print('q2' in 'q1.mp3')
        print(txt_no in ['q12', 'w12', 'q7'])
        print(';'.join(["fafdsa", "32432", "阀打开方式"]))
        self.assertEqual(True, True)

    def test_num(self):
        kwargs = {'a': 1, 'b': 2, 'c': 3}
        print({key: value for key, value in kwargs.items() if value is not None})
        print(round(2.3658, 3))
        print(round(9898.523 / 10, 2))
        print(9.98 - -7)
        print('1234567899876543b2a1'[-3:])



if __name__ == '__main__':
    unittest.main()
