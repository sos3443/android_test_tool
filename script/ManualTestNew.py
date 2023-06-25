# -*- coding: UTF-8 -*-
import os, sys
import threading
import time
from MyConfig import MyConfig
from lib.AdbLibCom import AdbLibCom
from lib.AppDeviceInfo import DeviceMessage
from lib.AppCalculator import CalculateData
from lib.AppOperateFile import OperateFileNew
from lib.AppPickle import OperatePickle
from lib.AppReport import Report

# from lib.AppOperateFile import OperateFile

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(os.path.realpath('__file__')), p))  # os.path.realpath(path)  返回path的真实路径

ad = AdbLibCom()
apm = CalculateData()
devMs = DeviceMessage()
pick = OperatePickle()
config = MyConfig()
# rep = Report()

# 全局变量
MemTestFlag = 0
monkey_log = ''
path_log = ''


def create_pickle(app_num):
    print("创建持久性文件...")
    manualMem = config.info_dir + "_" + config.package_name + "_" + "Manual_mem.pickle"
    manualCpu = config.info_dir + "_" + config.package_name + "_" + "Manual_cpu.pickle"
    manualBattery = config.info_dir + "_" + config.package_name + "_" + "Manual_battery.pickle"
    manualLiuliang = config.info_dir + "_" + config.package_name + "_" + "Manual_liuliang.pickle"
    manualAppRunTime = config.info_dir + "_" + config.package_name + "_" + "Manual_appruntime.pickle"
    # Manualjiff = Config.info_dir + "_" + Config.package_name + "_" + "Manual_jiff.pickle"
    # Manualfps = Config.info_dir + "_" + Config.package_name + "_" + "Manual_fps.pickle"
    # time.sleep(2)
    #  app[dev] = {"freemen": freemen, "medimen": medimen, "fullmen": fullmen,
    #              "freecpu": freecpu, "medicpu": medicpu, "fullcpu": fullcpu,
    #              "header": get_phone(dev)}
    time.sleep(1)
    OperateFileNew(manualMem, 'w+').prepare_pickle()
    time.sleep(1)
    OperateFileNew(manualCpu, 'w+').prepare_pickle()
    time.sleep(1)
    OperateFileNew(manualBattery, 'w+').prepare_pickle()
    time.sleep(1)
    OperateFileNew(manualLiuliang, 'w+').prepare_pickle()
    # time.sleep(1)
    # OperateFileNew(manualAppRunTime, 'w+').prepare_pickle()
    # OperateFileNew(Manualjiff,'w+').mkdir_file_new()
    # OperateFileNew(Manualfps,'w+').mkdir_file_new()
    OperateFileNew(config.info_dir + "sumInfo.pickle", 'w+').prepare_pickle()  # 用于记录是否已经测试完毕，里面存的是一个整数
    OperateFileNew(config.info_dir + "info.pickle", 'w+').prepare_pickle()  # 用于记录统计结果的信息，是[{}]的形式
    pick.write_sum(0, app_num, config.info_dir + "sumInfo.pickle")  # 初始化记录当前真实连接的设备数
    pick.write_info(devMs.get_device_message(), config.info_dir + "info.pickle")  # 初始化记录设备信息


# log生成函数
def logProcess(runtime):
    # logcat日志
    logcat_log = path_log + "\\" + runtime + "logcat.log"
    cmd_logcat = " logcat -d > %s" % (logcat_log)
    ad.adb_command(cmd_logcat)
    print('logcat 完成')

    # "导出traces文件"
    traces_log = path_log + "\\" + runtime + "traces.log"
    cmd_traces = " shell cat /data/anr/traces.txt > %s" % (traces_log)
    ad.adb_command(cmd_traces)
    print('traces_log 完成')


def start():
    rt = os.popen('adb devices').readlines()  # os.popen()执行系统命令并返回执行后的结果
    num = len(rt) - 2
    print(num)
    # app = {}
    create_pickle(num)
    signal = input("现在是手动测试部分，是否要开始你的测试，请输入(y or n): ")
    if signal == 'y' or 'Y':
        print("测试即将开始，请打开需要测试的app并准备执行您的操作....")
        time.sleep(5)
        # run_time = time.strftime("%Y-%m-%d_%H%M%S", time.localtime(time.time()))
        # logProcess(run_time)
        while ad.checkDevices():
            if not ad.checkDevices():
                break
            time.sleep(1)  # 每1秒采集一次
            print("----------------数据采集-----------------")
            apm.pid_mem(3)
            apm.getCpu()
            apm.get_battery_info()
            # apm.getRunAppTime()
            apm.getliuliang()
            continue
        # fps 测试需要打开开发者模式GPU模式
        # apm.pid_fps(Config.package_name, 3)
        # run_time = time.strftime("%Y-%m-%d_%H%M%S", time.localtime(time.time()))
        # logProcess(run_time)
        print('生成测试报告......')
        rep = Report(config.report_name, "Manual")
        rep.createReport()
        print('测试报告生成完毕')
    elif signal == 'n' or 'N':
        print('用户主动放弃测试，测试结束！')
    else:
        print("测试结束，输入非法，请重新输入y or n！")


# 启动多线程
class MonkeyTestThread(threading.Thread):
    def __init__(self, dev):
        threading.Thread.__init__(self)
        self.thread_stop = False
        self.dev = dev

    def run(self):
        time.sleep(2)
        start()


def create_threads_monkey(device):
    Thread_instances = ""
    # id_instance = ""
    # if device_list != [] and len(device_list) > 1:
    #  for id_instance in device_list:
    #   # dev = id_instance
    #   testInstance = MonkeyTestThread(id_instance)
    #   Thread_instances.append(testInstance)
    #  for instance in Thread_instances:
    #   instance.start()
    # elif device_list != [] and len(device_list) == 1:
    # dev = id_instance
    if device != "":
        testInstance = MonkeyTestThread(device)

        testInstance.start()
    else:
        pass


if __name__ == '__main__':
    # curPath = os.path.abspath(os.path.dirname(__file__))
    # rootPath = os.path.split(curPath)[0]
    # sys.path.append(os.path.split(rootPath)[0])
    device_dir = os.path.exists(config.info_dir)
    if device_dir:
        print("持久性目录info已存在，继续执行测试!")
    else:
        # os.mkdir(AppPerformanceConfig.info_path)  # 创建持久性目录,需要在文件存在的情况下创建二级目录
        os.makedirs(config.info_dir)  # 使用makedirs可以在文件夹不存在的情况下直接创建
    device = apm.get_device()
    # print(len(device))
    if ad.checkDevices():
        print("设备存在")
        create_threads_monkey(device)
    else:
        print("设备不存在")
