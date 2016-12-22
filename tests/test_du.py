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
        obj = Du('/root/', method=Du.RECURSION_METHOD)
        self.assertEqual(obj.path, '/root/')
        self.assertEqual(obj.method, Du.RECURSION_METHOD)
           
        obj = Du('/root/')
        self.assertEqual(obj.path, '/root/')
        self.assertEqual(obj.method, Du.WALK_METHOD)

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
        with self.assertRaises(ValueError):
            obj.path = None
        with self.assertRaises(TypeError):
            obj.path = 4

    def test_call(self):
        for key, value in methods_dict.items():
            with  patch.object(Du, value) as mock_method:
              obj = Du('.')
              obj(method=key)
              mock_method.assert_called()

    def test_methods(self):
        pass


    def test_str(self):
        for key, value in methods_dict.items():
            obj = Du('./test_folder', method=key)
            self.assertEqual(str(obj), 'Total number of files is 6 and their size is 6178 bytes')


if __name__ == '__main__':
    unittest.main()
   