# -*- coding: UTF-8 -*-

import os, pickle


# 持久化
class OperatePickle(object):

    # read pickle info
    def read_info(self, path):
        data = []
        with open(path, "rb") as f:
            try:
                data = pickle.load(f)
            # print("data:",data)
            except EOFError:
                data = []
                print("read file error for the file is empty!")
        print("read file success %s" %path)
        # print(data)
        return data

    # write pickle info
    def write_info(self, data, path):
        _read = self.read_info(path)
        result = []
        if _read:
            _read.append(data)
            result = _read
        else:
            result.append(data)
        with open(path, "wb") as f:
            print("write info success %s" %path)
            # print(result)
            pickle.dump(result, f)

    # write sum
    # possible no use
    def write_sum(self, init, data=None, path="data.pickle"):
        if init == 0:
            result = data
        else:
            _read = self.read_info(path)

        with open(path, "wb") as f:
            print("write sum")
            # print("sum:", sum)
            pickle.dump(result, f)

    # read sum
    # possible no use
    def read_sum(self, path):
        data = {}
        with open(path, "rb") as f:
            try:
                data = pickle.load(f)
            except EOFError:
                data = {}
                print("read file error for the file is empty!")
        print("read file sum success")
        # print(data)
        return data
