# -*- coding: UTF-8 -*-
import os,shutil
import threading
import time,datetime,subprocess

from MyConfig import MyConfig
from lib.AdbLibCom import AdbLibCom
from lib.AppDeviceInfo import DeviceMessage
from lib.AppCalculator import CalculateData
from lib.AppOperateFile import OperateFileNew
from lib.AppPickle import OperatePickle
from lib.AppReport import Report

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(os.path.realpath('__file__')), p)) #os.path.realpath(path)  返回path的真实路径

ad = AdbLibCom()
apm = CalculateData()
devMs = DeviceMessage()
pick = OperatePickle()
config = MyConfig()

#全局变量
MemTestFlag = 0
monkey_log=''
path_log=''



# 手机信息
# def get_phone():
#     phone_info = devMs.GetDevMsg()
# #    print phone_info
#     app = {}
#     app["phone_name"] = phone_info[0]["phone_name"] + "_" + phone_info[0]["phone_model"] + "_" + phone_info[0]["release"]
#     app["rom"] = phone_info[1]
#     app["kel"] = phone_info[2]
#     app["pix"] = phone_info[3]
#     return app

def Create_pickle(data):
    print("创建持久性文件...")

    # devIP = dev.split(':')[0].replace(".","")
    freemen = config.info_dir + "_" + config.package_name + "_" + "Free_mem.pickle"#空闲状态
    medimen = config.info_dir + "_" + config.package_name + "_" + "Medium_mem.pickle"#中等压力
    fullmen = config.info_dir + "_" + config.package_name + "_" + "Full_mem.pickle"#满压力
    freecpu = config.info_dir + "_" + config.package_name + "_" + "Free_cpu.pickle"#空闲状态
    medicpu = config.info_dir + "_" + config.package_name + "_" + "Medium_cpu.pickle"#中等压力
    fullcpu = config.info_dir + "_" + config.package_name + "_" + "Full_cpu.pickle"#满压力
    # freejiff = config.info_dir + "_" + config.package_name + "_" + "Free_jiff.pickle"#空闲状态
    # medijiff = config.info_dir + "_" + config.package_name + "_" + "Medium_jiff.pickle"#中等压力
    # fulljiff = config.info_dir + "_" + config.package_name + "_" + "Full_jiff.pickle"#满压力
    # medifps = config.info_dir + "_" + config.package_name + "_" + "Medium_fps.pickle"#中等压力
    # fullfps = config.info_dir + "_" + config.package_name + "_" + "Full_fps.pickle"#满压力

   # time.sleep(2)
    OperateFileNew(freemen).mkdir_file_new()
    OperateFileNew(medimen).mkdir_file_new()
    OperateFileNew(fullmen).mkdir_file_new()
    OperateFileNew(freecpu).mkdir_file_new()
    OperateFileNew(medicpu).mkdir_file_new()
    OperateFileNew(fullcpu).mkdir_file_new()
    # OperateFileNew(freejiff).mkdir_file_new()
    # OperateFileNew(medijiff).mkdir_file_new()
    # OperateFileNew(fulljiff).mkdir_file_new()
    # OperateFileNew(medifps).mkdir_file_new()
    # OperateFileNew(fullfps).mkdir_file_new()
    '''
    OperateFile(freemenTime).mkdir_file()
    OperateFile(medimenTime).mkdir_file()
    OperateFile(fullmenTime).mkdir_file()
    OperateFile(freecpuTime).mkdir_file()
    OperateFile(medicpuTime).mkdir_file()
    OperateFile(fullcpuTime).mkdir_file()
    OperateFile(freejiffTime).mkdir_file()
    OperateFile(medijiffTime).mkdir_file()
    OperateFile(fulljiffTime).mkdir_file()
    OperateFile(medifpsTime).mkdir_file()
    OperateFile(fullfpsTime).mkdir_file()
    '''
    OperateFileNew(config.info_dir + "sumInfo.pickle").mkdir_file_new() # 用于记录是否已经测试完毕，里面存的是一个整数
    OperateFileNew(config.info_dir + "info.pickle").mkdir_file_new() # 用于记录统计结果的信息，是[{}]的形式
    pick.write_sum(0, data, config.info_dir + "sumInfo.pickle") # 初始化记录当前真实连接的设备数
    pick.write_info(devMs.get_device_message(), config.info_dir + "info.pickle") # 初始化记录设备信息

def unlockScreen():
    cmd_openScreen = "shell input keyevent 224"
    cmd_slide = "shell input swipe 300 500 1000 500"
    ad.adb_command(cmd_openScreen)  # 点亮屏幕
    time.sleep(0.5)
    ad.adb_command(cmd_slide)  # 滑动解锁
    ad.adb_command(cmd_slide)

#log生成函数
def logProcess(runtime):
    # logcat日志
    logcat_log = path_log + "\\" + runtime + "logcat.log"
    cmd_logcat = "logcat -d > %s" % (logcat_log)
    ad.adb_command(cmd_logcat)
    print('logcat 完成')

    # "导出traces文件"
    traces_log = path_log + "\\" + runtime + "traces.log"
    cmd_traces = "shell cat /data/anr/traces.txt > %s" % (traces_log)
    ad.adb_command(cmd_traces)
    print('traces_log 完成')


# monkey启动函数
def monkeyStart(runtime, flag):
    global path_log
    path_log = config.log_dir
    device_dir = os.path.exists(path_log)
    if device_dir:
        print("log已存在，继续执行测试!")
    else:
        os.mkdir(path_log)
    if flag == 2:
        adb_monkey = "shell monkey -p %s -s %s %s" % (config.package_name, config.monkey_seed, config.monkey_parameters_full)
    elif flag == 1:
        adb_monkey = "shell monkey -p %s -s %s %s" % (config.package_name, config.monkey_seed, config.monkey_parameters_medi)
    global monkey_log
    monkey_log = path_log + "\\" + runtime + "monkey.log"
    cmd_monkey = "adb %s > %s" % (adb_monkey, monkey_log)
    subprocess.Popen(cmd_monkey, shell=True)


def mediMemTest():
    print("--------------开始执行测试----------------")
    print("--------------设备：场景2：中等压力下APP性能指标----------------")
    ad.adb_stop_activity(config.package_name)
    run_time = time.strftime("%Y-%m-%d_%H%M%S", time.localtime(time.time()))
    monkeyStart(run_time, 1)
    time.sleep(5)
    logProcess(run_time)#放在monkeystart之后作为缓冲，否则程序运行失败
    while ad.checkDevices():
        # try:
        #     with open(monkey_log, 'rb') as monkeylog:
        time.sleep(1)  # 每1秒采集一次
        apm.pid_mem(config.package_name, 1)
        apm.pid_cpuRate(config.package_name, 1)
        continue
                # time.sleep(config.get_time1(1)) #采样时间
                # apm.pid_fps(Config.package_name, 1)
                # if monkeylog.read().count('Monkey finished') > 0:
                #     # app[] = {"header": get_phone()}
                #     # app[]["header"]["net"] = Config.net
                #     # pick.writeInfo(app, Config.info_dir + "info.pickle")
                #     print("--------------设备：场景2：中等压力下测试完成----------------")
                #     break
        # except:
        #     break

def fullMemTest():
    print("--------------开始执行测试----------------")
    print("--------------设备：场景3：满压力下APP性能指标----------------")
    ad.adb_stop_activity(config.package_name)
    run_time = time.strftime("%Y-%m-%d_%H%M%S", time.localtime(time.time()))
    monkeyStart(run_time, 2)
    logProcess(run_time)
    while ad.checkDevices():
        # try:
        #     with open(monkey_log, 'rb') as monkeylog:
        time.sleep(1)  # 每1秒采集一次
        apm.pid_mem(config.package_name, 2)
        apm.pid_cpuRate(config.package_name, 2)
        continue
                # time.sleep(config.get_time1(2)) #采样时间
                #fps测试需要事先开启手机开发者模式里的GPU显示，否则运行出错
                # apm.pid_fps(dev, Config.package_name, 2)
                # if monkeylog.read().count('Monkey finished') > 0:
                #     print("--------------设备： 场景3：满压力下测试完成----------------")
                #     break
        # except:
        #     break

def start():
    rt = os.popen('adb devices').readlines()  # os.popen()执行系统命令并返回执行后的结果
    num = len(rt) - 2
    app = {}
    Create_pickle(num)
    unlockScreen()
    # 中等压力下测试
    mediMemTest()
    print('生成测试报告......')
    rep = Report("乐学高考 V3.1.3 性能测试报告", "Medium")
    rep.createReport()
    print('测试报告生成完毕')

#启动MONKEY多线程
class MonkeyTestThread(threading.Thread):
    def __init__(self,dev):
        threading.Thread.__init__(self)
        self.thread_stop = False
        self.dev = dev

    def run(self):
        time.sleep(2)
        start()



def create_threads_monkey(device):
    Thread_instances = ""
    if device != "":
        MontestInstance = MonkeyTestThread(device)
        Thread_instances = MontestInstance
        Thread_instances.start()
    else:
        pass    



if __name__ == '__main__':
    device_dir = os.path.exists(config.info_dir)
    if device_dir:
        print ("持久性目录info已存在，继续执行测试!")
    else:
        #os.mkdir(AppPerformanceConfig.info_path)  # 创建持久性目录,需要在文件存在的情况下创建二级目录
        os.makedirs(config.info_dir)   # 使用makedirs可以在文件夹不存在的情况下直接创建
    device= apm.get_device()
    if ad.checkDevices():
        print("设备存在")
        create_threads_monkey(device)
    else:
        print("设备不存在")