import unittest
from mock import MagicMock, patch
import os
import tempfile
import os.path 
import subprocess

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
    path_to_temp_folder = None

    @classmethod  
    def setUpClass(cls):
        cls.path_to_temp_folder = tempfile.mkdtemp()

        path_of_folder = os.path.join(cls.path_to_temp_folder, 'folder1')
        os.mkdir(path_of_folder)
        with open(os.path.join(path_of_folder, 'file1'), 'w') as f:
            f.write('test')

        path_of_folder2  = os.path.join(cls.path_to_temp_folder, 'folder2')
        os.mkdir(path_of_folder2)
        
        path_of_folder3 = os.path.join(path_of_folder2, 'folder3')
        os.mkdir(path_of_folder3)

        with open(os.path.join(path_of_folder3, 'file2'), 'w') as f:
            f.write('test')

        path_of_folder4 = os.path.join(path_of_folder3,'folder4')
        os.mkdir(path_of_folder4)

        with open(os.path.join(path_of_folder4, 'file3'), 'w') as f:
            f.write('test')
        with open(os.path.join(path_of_folder4, 'file4'), 'w') as f:
            f.write('test')

    @classmethod  
    def tearDownClass(cls):
        if cls.path_to_temp_folder is not None:
            subprocess.call(['rm', '-rf', cls.path_to_temp_folder])
       
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
        for key, value in methods_dict.items():
            obj = Du(self.path_to_temp_folder)
            method = getattr(obj,value)
            res = method()
            
        self.assertEqual(
            res,
            Du.Result(total_number_of_files=4, total_size_of_files=16)
        )
        self.assertIsInstance(res, Du.Result)

    def test_str(self):
        for key, value in methods_dict.items():
            obj = Du(self.path_to_temp_folder, method=key)
            self.assertEqual(str(obj), 
                    'Total number of files is 4 and their size is 16 bytes')

    def test_context_manager(self):
        obj = Du('/root/', method=Du.WALK_METHOD)
        with obj.use_method(Du.RECURSION_METHOD) as d:
            self.assertEqual(d.path, '/root/')
            self.assertEqual(d.method, Du.RECURSION_METHOD)
            self.assertIsNot(obj, d)



if __name__ == '__main__':
    unittest.main()
   