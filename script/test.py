# -*- coding: UTF-8 -*-
import os, sys
from lib.AppCalculator import CalculateData
from lib.AdbLibCom import AdbLibCom
from MyConfig import MyConfig
from lib.AppDeviceInfo import DeviceMessage

a = CalculateData()
dm = DeviceMessage()
b = AdbLibCom()
mc = MyConfig()


# mc.get_time1(1)

# class test:
#     def adb_get_pid(self):
#         result = self.adb_command("shell ps |findstr %s" % (mc.package_name)).split()[1]
#         print("1:", result)
#
#     def adb_command1(command):
#         result = ''
#         result_line = ''
#         command_input = "adb %s" % (command)
#         result = os.popen(command_input, "r")
#         while True:
#             line = result.readline()
#             if not line:
#                 break
#             result_line += line
#         result.close()
#         return result_line
#
#     def adb_command(self, command):
#         result = ''
#         result_line = ''
#         command_input = "adb %s" % (command)
#         result = os.popen(command_input, "r")
#         while True:
#             line = result.readline()
#             if not line:
#                 break
#             result_line += line
#         result.close()
#         return result_line
def getflow():
    # flow_info = open("e://1121.txt", "r").readlines()
    flow = [0, 0]

    info = " wlan0: 500101674  480193    0    0    0     0          0         0 28876223  211664    0    0    0     0       0          0"
    flow[0] = info.split(":")[1].strip().split(" 0    0    0     0          0         0")[0].strip().split(" ")[0] # 下载
    flow[1] = info.split(":")[1].strip().split(" 0    0    0     0          0         0")[1].strip().split(" ")[0]  # 发送
    print(flow[0])


if __name__ == '__main__':
    # result = test().adb_get_pid()
    # print(a.get_cpu_core_number())
    # a.getliuliang()
    # curPath = os.path.abspath(os.path.dirname(__file__))
    # print(curPath)
    # rootPath = os.path.split(curPath)[0]
    # sys.path.append(os.path.split(rootPath)[0])
    # print(rootPath)
    getflow()
