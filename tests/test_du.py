import unittest

import sys
sys.path.append('..')
from du import Du, InvalidDuMethodError


class TestDu(unittest.TestCase):

    def test_init(self):
        obj = Du('/root/', method=Du.QUEUE_METHOD)
        self.assertEqual(obj.path, '/root/')
        self.assertEqual(obj.method, Du.QUEUE_METHOD)

    def test_method(self):
        allowed_methods = (
            Du.WALK_METHOD, Du.RECURSION_METHOD, 
            Du.QUEUE_METHOD, Du.SUBPROCESSES_METHOD
        )

        obj = Du('.')
        # test of allowed method
        for m in allowed_methods:
            obj.method = m
            self.assertEqual(obj.method, m)

        # test of all other
        with self.assertRaises(InvalidDuMethodError):
            obj.method = 0


if __name__ == '__main__':
    unittest.main()