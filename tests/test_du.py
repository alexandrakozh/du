import unittest

import sys
sys.path.append('..')
from du import Du


class TestDu(unittest.TestCase):

    def test_init(self):
        obj = Du('/root/', method=Du.QUEUE_METHOD)
        self.assertEqual(obj.path, '/root/')
        self.assertEqual(obj.method, Du.QUEUE_METHOD)

    def test_method(self):
        obj = Du('/root/', method=Du.RECURSION_METHOD)
        self.assertEqual(obj.method, Du.RECURSION_METHOD)
        obj = Du('/root/', method=4)
        self.assertRaises(InvalidDuMethodError, Du.method)

if __name__ == '__main__':
    unittest.main()