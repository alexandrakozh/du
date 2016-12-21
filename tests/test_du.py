import unittest
from mock import MagicMock, patch

import sys
sys.path.append('..')
from du import Du, InvalidDuMethodError

allowed_methods = (Du.WALK_METHOD, Du.RECURSION_METHOD, 
        Du.QUEUE_METHOD, Du.SUBPROCESSES_METHOD
        )

class TestDu(unittest.TestCase):

    def test_init(self):
        obj = Du('/root/', method=Du.QUEUE_METHOD)
        self.assertEqual(obj.path, '/root/')
        self.assertEqual(obj.method, Du.QUEUE_METHOD)
        obj2 = Du('/root/')
        self.assertEqual(obj2.path, '/root/')
        self.assertEqual(obj2.method, Du.WALK_METHOD)

    def test_method(self):
        obj = Du('.')
        # test of allowed method
        for m in allowed_methods:
            obj.method = m
            self.assertEqual(obj.method, m)

        # test of all other
        with self.assertRaises(InvalidDuMethodError):
            obj.method = 0

    def test_path(self):
        obj = Du('/root')
        self.assertEqual(obj.path, '/root/')
        obj2 = Du('/root/')
        self.assertEqual(obj2.path, '/root/')

    def test_call(self):
        # TODO: test all methods
        # TODO: create loop over all methods using dictionary with getattr builtin operator
        with patch.object(Du, '_du_using_walk') as mock_method:
            obj = Du('.')
            obj(method=Du.WALK_METHOD)
            mock_method.assert_called()

        # TODO: test that default method will be called

        with self.assertRaises(InvalidDuMethodError):
            obj(method=0)

    def test_du_using_walk(self):
        obj = Du('./tests/test_folder', method=Du.WALK_METHOD)
        self.assertTrue(Du.Result(total_number_of_files=6, total_size_of_files=6178))
        obj2 = Du('./tests/test_folder', method=1)
        self.assertTrue(Du.Result(total_number_of_files=6, total_size_of_files=6178))
        obj3 = Du('./tests/test_folder')
        self.assertTrue(Du.Result(total_number_of_files=6, total_size_of_files=6178))

    def test_du_using_recursion(self):
        obj = Du('./tests/test_folder', method=Du.RECURSION_METHOD)
        self.assertTrue(Du.Result(total_number_of_files=6, total_size_of_files=6178))
        obj2 = Du('./tests/test_folder', method=2)
        self.assertTrue(Du.Result(total_number_of_files=6, total_size_of_files=6178))

    def test_du_using_list(self):
        obj = Du('./tests/test_folder', method=Du.QUEUE_METHOD)
        self.assertTrue(Du.Result(total_number_of_files=6, total_size_of_files=6178))
        obj2 = Du('./tests/test_folder', method=3)
        self.assertTrue(Du.Result(total_number_of_files=6, total_size_of_files=6178))

    def test_du_using_subprocesses(self):
        obj = Du('./tests/test_folder', method=Du.SUBPROCESSES_METHOD)
        self.assertTrue(Du.Result(total_number_of_files=6, total_size_of_files=6178))
        obj2 = Du('./tests/test_folder', method=4)
        self.assertTrue(Du.Result(total_number_of_files=6, total_size_of_files=6178))

    def test_str(self):
        obj = Du('./tests/test_folder', method=Du.RECURSION_METHOD)
        self.assertTrue('Total number of files is 6 and their size is 6178 bytes')
        obj2 = Du('./tests/test_folder', method=1)
        self.assertTrue('Total number of files is 6 and their size is 6178 bytes')
        obj3 = Du('./tests/test_folder')
        self.assertTrue('Total number of files is 6 and their size is 6178 bytes')

if __name__ == '__main__':
    unittest.main()
