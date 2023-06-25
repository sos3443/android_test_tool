# -*- coding: UTF-8 -*-

import os, re
from lib.AdbLibCom import AdbLibCom

alc = AdbLibCom()


class DeviceMessage(object):

    # get device 型号
    # def get_device_model(self):
    # 	result = {}
    # 	result["release"] = alc.adb_get_android_version()
    # 	result["phone_name"] = alc.adb_get_device_name()
    # 	result["phone_model"] = alc.adb_get_device_brand()
    # 	return result

    # get mem total
    def get_mem_total(self):
        result = alc.adb_get_device_mem()
        return result.rstrip().lstrip()

    # get cpu core number
    def get_cpu_number(self):
        result = alc.adb_get_device_cpu_info()
        return str(len(re.findall("processor", result)))

    # get screen size
    def get_screen_size(self):
        result = alc.adb_get_screen_size().split(":")[1]
        return result.rstrip().lstrip()

    # get all
    def get_device_message(self):
        result = {}
        result["release"] = alc.adb_get_android_version()
        result["phone_name"] = alc.adb_get_device_name()
        result["phone_model"] = alc.adb_get_device_brand()
        result["screen_size"] = self.get_screen_size()
        result["mem_total"] = self.get_mem_total()
        # phone_msg = self.get_device_model()
        result["cpu_sum"] = self.get_cpu_number()
        # print(dev + ":"+ pix,men_total,phone_msg,cpu_sum)
        return result


if __name__ == "__main__":
    pass
