import unittest
from mock import MagicMock, patch

import sys
sys.path.append('..')
from du import Du, InvalidDuMethodError

methods_dict = {
    Du.WALK_METHOD: '_du_using_walk', 
    Du.RECURSION_METHOD: '_du_using_recursion',
    Du.QUEUE_METHOD: '_du_using_list', 
    Du.SUBPROCESSES_METHOD : '_du_using_subprocesses'
    }


class TestDu(unittest.TestCase):

    def test_init(self):
        for key, value in methods_dict.items():
            obj = Du('/root/', method=key)
            self.assertEqual(obj.path, '/root/')
            self.assertEqual(obj.method, key)
           
        obj2 = Du('/root/')
        self.assertEqual(obj2.path, '/root/')
        self.assertEqual(obj2.method, Du.WALK_METHOD)

    def test_method(self):
        obj = Du('.')
        for key, value in methods_dict.items():
            obj.method = key
            self.assertEqual(obj.method, key)

        with self.assertRaises(InvalidDuMethodError):
            obj.method = 0

    def test_path(self):
        obj = Du('/root')
        self.assertEqual(obj.path, '/root/')
        obj = Du('/root/')
        self.assertEqual(obj.path, '/root/')

    def test_call(self):
    #     # with patch.object(Du, '_du_using_walk') as mock_method:
    #     #     obj = Du('.')
    #     #     obj(method=Du.WALK_METHOD)
    #     #     mock_method.assert_called()

        obj = Du('.')
        a = getattr(obj, methods_dict[Du.WALK_METHOD])
        self.assertEqual(obj(), a())


        for key, value in methods_dict.items():
            obj = Du('.', method=key)
            a = getattr(obj, value)
            self.assertEqual(obj(), a())

        with self.assertRaises(InvalidDuMethodError):
            obj(method=0)

    def test_methods(self):
        for key, value in methods_dict.items():
            mock_method = patch.object(Du, value)
            obj = Du('.')
            obj(method=key)
            mock_method.assert_called()

    def test_str(self):
        for key, value in methods_dict.items():
            obj = Du('./test_folder', method=key)
            self.assertEqual(str(obj), 'Total number of files is 6 and their size is 6178 bytes')


if __name__ == '__main__':
    unittest.main()
   