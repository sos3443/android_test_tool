# -*- coding: UTF-8 -*-

import os


class OperateFileNew(object):

    def __init__(self, file, method='w+'):
        self.file = file
        self.method = method
        self.file_handle = None

    def mkdir_file_new(self):
        if os.path.isfile(self.file):
            f = open(self.file, self.method)
            f.close()
            print("file created success %s" %self.file)
        else:
            print("file already existed")

    def remove_file_new(self):
        if os.path.isfile(self.file):
            os.remove(self.file)
        else:
            print("file not existed")

    def prepare_pickle(self):
        if os.path.exists(self.file):
            os.remove(self.file)
            f = open(self.file, self.method)
            print("file recreate succeess %s" %self.file)
            f.close()
        else:
            f = open(self.file, self.method)
            print("file create succeess %s" % self.file)
            f.close()
