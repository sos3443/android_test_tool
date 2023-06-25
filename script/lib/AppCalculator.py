# -*- coding: UTF-8 -*-
import math
import os, re, time
from lib.AdbLibCom import AdbLibCom
from lib.AppDeviceInfo import DeviceMessage
from MyConfig import MyConfig
from lib.AppPickle import OperatePickle

alc = AdbLibCom()
dm = DeviceMessage()
mc = MyConfig()
pick = OperatePickle()


class CalculateData(object):

    def get_device(self):
        device = ""
        rt = os.popen('adb devices').readlines()  # os.popen()执行系统命令并返回执行后的结果
        n = len(rt) - 2
        print("当前已连接待测手机数为：" + str(n))
        if n == 1:
            # print(str(rt).split("\n")[0])
            device = (str(rt[1]).split("\t")[0])
        else:
            pass
        print(device)
        return device

    # (B-A)/(TB-TA)*100，其中A为被测应用第一次获取到的cpu情况，B为A间隔500毫秒后再次获取到cpu情况，
    # TA为整个手机的cpu情况，TB为TA间隔500毫秒后再次获取到的cpu情况。当前应用有多个进程时，所得的cpu占用为多个进程的cpu占用和
    # calculate cpu rate
    def cal_cpu(self):
        middle1 = []
        rates = []
        pids = []
        package_names = []
        cpu_rate = {}
        cpu_rate_all = 0.00
        cpu_data_init = alc.adb_get_device_cpu_rate()
        middle1 = cpu_data_init.split("\n")
        if len(middle1) == 1:
            str1 = ''.join(middle1)
            # print("str1:",str1)
            a = str1.split(" ")[0]
            # print("a:",a)
            b = str1.split(" ")[1]
            # print("b:",b)
            d = b.split("/")[0]
            # print("d:",d)
            c = b.split("/")[1][:-1]
            # print("c:",c)
            cpu_rate[c] = a
        # print(c,cpu_rate[c])
        else:
            # print("middle1:",middle1)
            for i in middle1:
                str1 = ''.join(i)
                # print("str1:",str1)
                a = str1.rstrip().lstrip().split(" ")[0]
                rates.append(a)
                # print("a:",a)
                d = str1.rstrip().lstrip().split(" ")[1]
                # print("d:",d)
                b = d.rstrip().lstrip().split("/")[0]
                pids.append(b)
                # print("b:",b)
                c = d.rstrip().lstrip().split("/")[1][:-1]
                package_names.append(c)
                # print("c:",c)
                cpu_rate[c] = a

                for i in cpu_rate.keys():
                    cpu_rate_all += float(cpu_rate[i][:-1]) / 100
            # print(cpu_rate_all)
        return round(cpu_rate_all, 2)

    def cal_mem(self):
        str1 = alc.adb_get_device_mem_all()
        # print("str1:",str1)
        mem_number = str1.split()[0][:-1]
        # print("mem_number:",mem_number)
        return mem_number

    # record mem heap
    def record_mem(self):
        str1 = alc.adb_get_device_pid_mem()
        # print("str1:",str1)
        native_heap = str1.split("\n")[7].rstrip().lstrip().split("    ")[1]
        dalvik_heap = str1.split("\n")[8].rstrip().lstrip().split("     ")[1]
        total = str1.split("\n")[22].rstrip().lstrip().split("    ")[1]
        print("native_heap:", native_heap)
        print("dalvik_heap:", dalvik_heap)
        print("total:", total)
        return native_heap, dalvik_heap, total

    # calculate mem rate
    def cal_mem_rate(self):
        used = self.cal_mem()[:-1]
        s = re.sub(',', '', used)
        print(s)
        total = alc.adb_get_device_mem().split()[0]
        print(total)
        if len(total) > 0:
            used_mem_rate = int(s) / int(total) * 1.0000
        else:
            print("total mem error!")
            used_mem_rate = 0
        return used_mem_rate

    # get battery
    def get_battery(self):
        list = alc.adb_get_battery_info().split
        for k, v in enumerate(list):
            if str(v) == "level:":
                battery = int(list[k + 1])
        print("battery")
        print(type(battery))
        pick.write_info(battery, mc.info_dir + "_Manual_battery.pickle")

    # get total cpu time
    def get_total_cpu_time(self):
        user = nice = system = idle = iowait = irq = softirq = 0

        '''
        user    从系统启动开始累计到当前时刻，用户态的CPU时间（单位：jiffies） ，不包含 nice值为负进程。1jiffies=0.01秒
        nice    从系统启动开始累计到当前时刻，nice值为负的进程所占用的CPU时间（单位：jiffies）
        system  从系统启动开始累计到当前时刻，核心时间（单位：jiffies）
        idle    从系统启动开始累计到当前时刻，除硬盘IO等待时间以外其它等待时间（单位：jiffies）
        iowait  从系统启动开始累计到当前时刻，硬盘IO等待时间（单位：jiffies） ，
        irq     从系统启动开始累计到当前时刻，硬中断时间（单位：jiffies）
        softirq 从系统启动开始累计到当前时刻，软中断时间（单位：jiffies）
        '''
        res = alc.adb_get_cpu_time().split()
        try:
            for info in res:
                if info == "cpu":
                    user = res[1]
                    nice = res[2]
                    system = res[3]
                    idle = res[4]
                    iowait = res[5]
                    irq = res[6]
                    softirq = res[7]
                    result = int(user) + int(nice) + int(system) + int(idle) + int(iowait) + int(irq) + int(softirq)
                    return result
        except:
            return 0

    def pidCpuJiff(self, pid):
        '''
        utime   该任务在用户态运行的时间，单位为jiffies
        stime   该任务在核心态运行的时间，单位为jiffies
        cutime  累计的该任务的所有的waited-for进程曾经在用户态运行的时间，单位为jiffies
        cstime= 累计的该任务的所有的waited-for进程曾经在核心态运行的时间，单位为jiffies
        '''
        utime = stime = cutime = cstime = 0
        try:
            res = alc.adb_get_pid_cpu_time(pid).split()
            utime = res[13]
            stime = res[14]
            cutime = res[15]
            cstime = res[16]
            result = int(utime) + int(stime) + int(cutime) + int(cstime)
        except:
            result = 0
        return result

    def get_pid(self):
        pid = alc.adb_get_pid()
        print(pid)
        return int(pid)

    def get_devSystemison(self):
        return alc.adb_get_android_version()

    # 通过jiff来进行CPU计算

    def cpu_jiffrate(self):
        try:
            pid = self.get_pid()
            processCpuTime1 = self.pidCpuJiff(pid)
            totalCpuTime1 = self.get_total_cpu_time()
            time.sleep(1)
            processCpuTime2 = self.pidCpuJiff(pid)
            totalCpuTime2 = self.get_total_cpu_time()
            processCpuTime3 = processCpuTime2 - processCpuTime1
            totalCpuTime3 = (totalCpuTime2 - totalCpuTime1)
            cpu = 100 * (processCpuTime3) / (totalCpuTime3)
        except Exception as e:
            print("error %s" % (e))
            cpu = 0
        return cpu

    # 计算某进程的cpu使用率 top方式
    # dev     :    设备号
    # packname:    应用包名
    # flag    :    # 0: 空闲状态
    #              # 1：中等压力
    #              # 2：满压力
    #              # 3：手动

    def pid_cpuRate(self, flag):
        try:
            rate = self.cal_cpu()  # 精度不足，先忍了
            print("--------设备：cpurate--------")
            if rate >= 0 and flag == 0:
                pick.write_info(rate, mc.info_dir + "_" + mc.package_name + "_" + "Free_cpu.pickle")
                pick.write_info(time.strftime("%H:%M:%S", time.localtime(time.time())),
                                mc.info_dir + "_" + mc.package_name + "_" + "Free_cpu.pickle")
            elif rate >= 0 and flag == 1:
                pick.write_info(rate, mc.info_dir + "_" + mc.package_name + "_" + "Medium_cpu.pickle")
                pick.write_info(time.strftime("%H:%M:%S", time.localtime(time.time())),
                                mc.info_dir + "_" + mc.package_name + "_" + "Medium_cpu.pickle")
            elif rate >= 0 and flag == 2:
                pick.write_info(rate, mc.info_dir + "_" + mc.package_name + "_" + "Full_cpu.pickle")
                pick.write_info(time.strftime("%H:%M:%S", time.localtime(time.time())),
                                mc.info_dir + "_" + mc.package_name + "_" + "Full_cpu.pickle")
            else:
                pick.write_info(rate, mc.info_dir + "_" + mc.package_name + "_" + "Manual_cpu.pickle")
                pick.write_info(time.strftime("%H:%M:%S", time.localtime(time.time())),
                                mc.info_dir + "_" + mc.package_name + "_" + "Manual_cpu.pickle")
        except Exception as e:
            print("捕捉cpuerror %s" % (e))

    # 获得CPU进程时间片
    def pid_Jiff(self, pid):
        processCpuTime1 = self.pidCpuJiff(pid)
        time.sleep(1)
        processCpuTime2 = self.pidCpuJiff(pid)
        processCpuTime3 = processCpuTime2 - processCpuTime1
        jiff = processCpuTime3
        print("--------jiff--------")
        if jiff >= 0:
            pick.write_info(jiff, mc.info_dir + "_" + mc.package_name + "_" + "_jiff.pickle")
        return jiff

    # 获得指定应用内存信息
    # 0: 空闲状态
    # 1：中等压力
    # 2：满压力
    # 3：手动

    def pid_mem(self, flag):
        try:
            lis = alc.adb_get_device_pid_mem().split()
            # print lis
            for i in range(len(lis)):
                if lis[i] == "TOTAL":
                    data = lis[i + 1]
                    break
            mem = round(int(data) / 1024, 2)
            print("--------设备：mem--------")
            if mem >= 0 and flag == 0:
                pick.write_info(mem, mc.info_dir + "_" + mc.package_name + "_" + "Free_mem.pickle")
                pick.write_info(time.strftime("%H:%M:%S", time.localtime(time.time())),
                                mc.info_dir + "_" + mc.package_name + "_" + "Free_mem.pickle")
            elif mem >= 0 and flag == 1:
                pick.write_info(mem, mc.info_dir + "_" + mc.package_name + "_" + "Medium_mem.pickle")
                pick.write_info(time.strftime("%H:%M:%S", time.localtime(time.time())),
                                mc.info_dir + "_" + mc.package_name + "_" + "Medium_mem.pickle")
            elif mem >= 0 and flag == 2:
                pick.write_info(mem, mc.info_dir + "_" + mc.package_name + "_" + "Full_mem.pickle")
                pick.write_info(time.strftime("%H:%M:%S", time.localtime(time.time())),
                                mc.info_dir + "_" + mc.package_name + "_" + "Full_mem.pickle")
            elif mem >= 0 and flag == 3:
                pick.write_info(mem, mc.info_dir + "_" + mc.package_name + "_" + "Manual_mem.pickle")
                pick.write_info(time.strftime("%H:%M:%S", time.localtime(time.time())),
                                mc.info_dir + "_" + mc.package_name + "_" + "Manual_mem.pickle")
        # return mem
        except Exception as e:

            print("捕捉内存error %s" % (e))

    # 获取cpu核数
    def get_cpu_core_number(self):
        li = os.popen("adb shell cat //proc//cpuinfo").readlines()
        sum = 0
        for line in li:
            if "processor" in line:
                sum += 1
        return sum

    # top命令获取cpu
    def getCpu(self):
        try:
            li = os.popen("adb shell top -m 100 -n 1 -s " + str(
                self.get_cpu_core_number())).readlines()  # 这个命令有BUG，CPU核数需要取出来，然后变量传进去
            rate = 0.0
            for line in li:
                if mc.package_name.split(".")[1] in line:
                    cpulist = line.split(" ")
                    if mc.package_name.split(".")[1] in cpulist[-1].strip():
                        while '' in cpulist:  # 将list中的空元素删除
                            cpulist.remove('')
                        # print(cpulist)
                        rate = float(cpulist[2].strip('%'))

            print("--------设备：cpurate--------")
            if rate >= 0:
                pick.write_info(rate, mc.info_dir + "_" + mc.package_name + "_" + "Manual_cpu.pickle")
                pick.write_info(time.strftime("%H:%M:%S", time.localtime(time.time())),
                                mc.info_dir + "_" + mc.package_name + "_" + "Manual_cpu.pickle")

        except Exception as e:
            print("捕捉cpu2error %s" % (e))

    # 获取电量
    def get_battery_info(self):
        try:
            os.popen("adb shell dumpsys battery unplug")  # 断电

            battery_cmd = "adb shell dumpsys battery"
            output = os.popen(battery_cmd).read().split("\n")
            dict = {}
            for i in output:
                new_i = i.strip(" ").split(":")
                if len(new_i) == 1:
                    del new_i
                else:
                    key = new_i[0]
                    value = new_i[1]
                    dict[key] = value
            battery_remain = int(dict["level"].strip(""))
            battery_statu = int(dict["status"].strip(""))
            os.popen("adb shell dumpsys battery reset")  # 复位
            if battery_statu == 2:
                print("Info:充电中...")
            else:
                print("Info:手机未充电...")
            print("Info:手机电量目前为:%d%%" % (battery_remain))
            pick.write_info(battery_remain, mc.info_dir + "_" + mc.package_name + "_" + "Manual_battery.pickle")
            pick.write_info(time.strftime("%H:%M:%S", time.localtime(time.time())),
                            mc.info_dir + "_" + mc.package_name + "_" + "Manual_battery.pickle")

        except Exception as e:
            print("捕捉电量异常 %s" % (e))

    # 获取App启动时间
    def getRunAppTime(self):
        try:
            # 启动APP
            cmd = 'adb shell am start -W -n %s/%s' % (mc.package_name, mc.activity_name)
            self.content = os.popen(cmd)
            # time.sleep(5)
            # 获取启动total时间
            totalTime = 0
            for line in self.content.readlines():
                if "TotalTime" in line:
                    totalTime = int(line.split(":")[1].strip(""))

                    break
            # 停止APP
            cmd = "adb shell input keyevent 3"
            os.popen(cmd)
            pick.write_info(totalTime, mc.info_dir + "_" + mc.package_name + "_" + "Manual_appruntime.pickle")
            pick.write_info(time.strftime("%H:%M:%S", time.localtime(time.time())),
                            mc.info_dir + "_" + mc.package_name + "_" + "Manual_appruntime.pickle")

        except Exception as e:
            print("捕捉App启动时间异常 %s" % (e))

    def getFlow(self):
        pid = alc.adb_get_pid()
        flow_info = os.popen("adb shell cat /proc/" + pid + "/net/dev").readlines()
        flow = [0, 0]
        for info in flow_info:
            if mc.net_status in info:
                flow[0] = \
                    info.split(":")[1].strip().split(" 0    0    0     0          0         0")[0].strip().split(" ")[
                        0]  # 下载
                flow[1] = \
                    info.split(":")[1].strip().split(" 0    0    0     0          0         0")[1].strip().split(" ")[
                        0]  # 发送

                print(flow[0])
                print(flow[1])
            # temp_list = info.split()
            # t.append(temp_list)
        # k1=math.ceil(int(t[6][1])/1024)
        # k2=math.ceil(int(t[6][9])/1024)
        # flow[0] = t[6][1]  # 下载
        # flow[1] = t[6][9]  # 发送
        # print(flow)
        return flow

    def getliuliang(self):
        try:
            T = [0, 0]
            t1 = CalculateData().getFlow()
            time.sleep(1)
            t2 = CalculateData().getFlow()
            k1 = int(t2[0]) - int(t1[0])
            k2 = int(t2[1]) - int(t1[1])
            T[0] = math.ceil(k1 / 1024)
            T[1] = math.ceil(k2 / 1024)
            # print(T[0],T[1])
            pick.write_info(int(T[0]), mc.info_dir + "_" + mc.package_name + "_" + "Manual_liuliang.pickle")
            pick.write_info(time.strftime("%H:%M:%S", time.localtime(time.time())),
                            mc.info_dir + "_" + mc.package_name + "_" + "Manual_liuliang.pickle")
        except Exception as e:
            print("捕捉流量下载异常 %s" % (e))


if __name__ == '__main__':
    pass
