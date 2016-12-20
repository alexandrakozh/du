from os import walk, listdir
from os.path import getsize, join, isfile, isdir
from collections import namedtuple
from subprocess import Popen, PIPE
import re

class InvalidDuMethodError(Exception):
    pass

class Du(object):
    """Class which implement calculations of the number of files in `path` and
    the amount of space on the disc, which is occupied by the files

       :param str path: path to directory
       :param int method: a number that match to the method which execute
         calculations. See `Du` constants `WALK_METHOD`,
        'RECURSION_METHOD', 'QUEUE_METHOD', 'SUBPROCESSES_METHOD'
       :rtype: string
    :return: Message with the number of files and the number of files which is
    occupied
    """

    WALK_METHOD = 1
    RECURSION_METHOD = 2
    QUEUE_METHOD = 3
    SUBPROCESSES_METHOD = 4
    Result = namedtuple('Result',
                        ['total_number_of_files', 'total_size_of_files'])

    def __init__(self, path, method=WALK_METHOD):
        self.path = path
        self.method = method

    @property
    def path(self):
        return self._path

    @property
    def method(self):
        return self._method

    @path.setter
    def path(self, path):
        if path[-1] != "/":
            self._path = path + "/"
        else:
            self._path = path

    @method.setter
    def method(self, method):
        if method in (Du.WALK_METHOD, Du.RECURSION_METHOD, Du.QUEUE_METHOD,
                        Du.SUBPROCESSES_METHOD):
            self._method = method
        else:
            raise InvalidDuMethodError(
                'InvalidDuMethodError: This method doesn\'t exist!'
            )

    # TODO: create argument `method` that will be used before self.method if specified
    def __call__(self, method=None):
        """Perform calculation of files count and capacity

        :param method: Method choose the appropriate method
            to perform calculations
        :rtype: NamedTuple
        :return: Result(files, capacity)
        """

        if method is None:
            action = self.method
        else:
            action = method

        if action == Du.WALK_METHOD:
            return self._du_using_walk()
        elif action == Du.RECURSION_METHOD:
            return self._du_using_recursion()
        elif action == Du.QUEUE_METHOD:
            return self._du_using_list()
        elif action == Du.SUBPROCESSES_METHOD:
            return self._du_using_subprocesses()

        raise InvalidDuMethodError(
            'InvalidDuMethodError: This method doesn\'t exist!'
        )


    def _du_using_walk(self):
        """Method calculates the number of files in `path` and the amount of
        space on the disc, which is occupied by the files using method walk
         from standard library os

        :rtype: NamedTuple
        :return: Result(files, capacity)
        """

        num = 0
        size = 0

        for dirpath, dirnames, files in walk(self.path):
            for f in files:
                size += getsize(join(dirpath, f))
            num += len(files)
        return Du.Result(num, size)

    def _du_using_recursion(self, directory_path=None):
        """Method calculates the number of files in `path` and the amount of
        space on the disc, which is occupied by the files using recursion

           :param str directory_path: for internal use only
        :rtype: NamedTuple
        :return: Result(files, capacity)
        """
        num = 0
        size = 0
        if directory_path is None:
            current_path = self.path
        else:
            current_path = directory_path
        list_of_files = listdir(current_path)
        for f in list_of_files:
            f_path = join(current_path, f)
            if isdir(f_path):
                rec_num, rec_size = self._du_using_recursion(f_path)
                num += rec_num
                size += rec_size
            else:
                num += 1
                size += getsize(f_path)
        return Du.Result(num, size)

    def _du_using_list(self):
        """Method calculates the number of files in `path` and the amount of
        space on the disc, which is occupied by the files using queue method

        :rtype: NamedTuple
        :return:s Result(files, capacity)
        """

        num = 0
        size = 0
        dirs = [self.path]
        for d in dirs:
            list_of_files = listdir(d)
            for name in list_of_files:
                f_path = join(d, name)
                if isfile(f_path):
                    num += 1
                    size += getsize(f_path)
                else:
                    dirs.append(f_path)
        return Du.Result(num, size)

    def _du_using_subprocesses(self):
        """Method calculates the number of files in `path` and the amount of space on the disc,
        which is occupied by the files using subprocess and PIPE

        :rtype: NamedTuple
        :return:s Result(files, capacity)
        """
        size = 0
        size_process = Popen(['find', self.path, '-type', 'f', '-ls'], stdout=PIPE)
        size_result, _  = size_process.communicate()
        lines = size_result.split("\n")
        separator = re.compile("\s+")
        for line in lines:
        	if len(line.strip()) == 0:
        		continue
        	file_info = separator.split(line)
        	file_size = int(file_info[6])
        	size += file_size

        list_of_files_process = Popen(['find', self.path, '-type', 'f'], stdout=PIPE)
        list_of_files, _ = list_of_files_process.communicate()
        num = len(list_of_files.split("\n")) - 1

        return Du.Result(num, size)

    def __str__(self):
        """Method implement string presentation of the result of perfoming the
         class

        :rtype: str
        :return:s Message with the number of files and capacity of directory
        """

        obj = self()
        return "Total number of files is {} " \
               "and their size is {} bytes".format(*obj)



if __name__ == "__main__":
    # TODO: refactor to use comand line arguments using `argparse` module
    # TODO: example
    # TODO: $ ./du.py /tmp/ --method queue
    # TODO: Total a.number of files is 123 and their size is 12345 bytes
    # TODO: $ ./du.py -h
    path = raw_input("Please enter the path of directory: ")
    method = int(raw_input("Please enter the number for appropriate method: \
             1 - for walk method, 2 - for recursion method, 3 - for queue method, \
             4 - for subprocess method:"))
    print Du(path, method)
