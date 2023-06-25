# -*- coding: UTF-8 -*-
import os, subprocess, time

from MyConfig import MyConfig

mc = MyConfig()


class AdbLibCom(object):

    # 发送命令，拿到返回值，处理成string
    def adb_command(self, command):
        result = ''
        result_line = ''
        command_input = "adb %s" % (command)
        result = os.popen(command_input, "r")
        while True:
            line = result.readline()
            if not line:
                break
            result_line += line
        result.close()
        return result_line

    # return result

    def checkDevices(self):
        # res = self.adb_command("devices")
        # devices = res.partition('\n')[2].replace('\n', '').split('\tdevice')
        # print(devices)
        # return [device for device in devices if len(device) > 2]
        # dev_list = []
        rt = os.popen('adb devices').readlines()

        n = len(rt) - 2
        print(n)
        if n > 0:
            return True
        else:
            return False

    # stop adb server
    def adb_stop_server(self):
        return self.adb_command("kill-server")

    # start adb server
    def adb_start_server(self):
        return self.adb_command("start-server")

    # get adb version
    def adb_get_adb_version(self):
        return self.adb_command("version")

    # file from pc to mobile
    def adb_push(self, pc_dir, mobile_dir):
        result = self.adb_command("push %s %s" % (pc_dir, mobile_dir))
        return result

    # file from mobile to pc
    def adb_pull(self, pc_dir, mobile_dir):
        result = self.adb_command("pull %s %s" % (mobile_dir, pc_dir))
        return result

    # install apk on mobile
    # -l    将应用安装到保护目录 / mnt / asec
    # -r    允许覆盖安装
    # -t    允许安装AndroidManifest.xml里application指定android:testOnly = "true"的应用
    # -s    将应用安装到sdcard
    # -d    允许降级覆盖安装
    # -g    授予所有运行时权限
    def adb_install_apk(self, apk_name):
        return self.adb_command("install %s" % (apk_name))

    # uninstall apk from mobile
    # @parameter package_name---包名
    # -k 卸载时保留数据和缓存目录
    def adb_uninstall_apk(self):
        return self.adb_command("uninstall %s" % (mc.package_name))

    # 查看应用列表
    # 无	    所有应用
    # -f	显示应用关联的 apk 文件
    # -d	只显示 disabled 的应用
    # -e	只显示 enabled 的应用
    # -s	只显示系统应用
    # -3	只显示第三方应用
    # -i	显示应用的 installer
    # -u	包含已卸载应用
    def adb_get_package_list(self):
        return self.adb_command("shell pm list packages %s" % (mc.package_name))

    # clear cache
    def adb_clear_cache(self):
        return self.adb_command("shell pm clear %s" % (mc.package_name))

    # get app info
    def adb_get_app_info(self):
        return self.adb_command("shell dumpsys package %s" % (mc.package_name))

    # start activity
    def adb_start_activity(self, activity):
        result = self.adb_command("shell am start %s" % (activity))
        return result.rstrip().lstrip()

    # stop activity
    def adb_stop_activity(self):
        result = self.adb_command("shell am force-stop %s" % (mc.package_name))
        return result.rstrip().lstrip()

    # get device 型号
    def adb_get_device_model(self):
        result = self.adb_command("shell getprop ro.product.model")
        return result.rstrip().lstrip()

    # get device brand
    def adb_get_device_brand(self):
        result = self.adb_command("shell getprop ro.product.brand")
        return result.rstrip().lstrip()

    # get device name
    def adb_get_device_name(self):
        result = self.adb_command("shell getprop ro.product.name")
        return result.rstrip().lstrip()

    # get device cpu 型号
    def adb_get_device_cpu_board(self):
        result = self.adb_command("shell getprop ro.product.board")
        return result.rstrip().lstrip()

    # reboot mobile
    def adb_reboot_device(self):
        result = self.adb_command("reboot")
        return result.rstrip().lstrip()

    # get battery info
    def adb_get_battery_info(self):
        result = self.adb_command("shell dumpsys battery")
        return result.rstrip().lstrip()

    # get screen size
    def adb_get_screen_size(self):
        result = self.adb_command("shell wm size")
        return result.rstrip().lstrip()

    # return result

    # get screen info
    def adb_get_screen_info(self):
        result = self.adb_command("shell dumpsys window displays")
        return result.rstrip().lstrip()

    # get screen DPI
    def adb_get_screen_dpi(self):
        result = self.adb_command("shell wm density")
        return result.rstrip().lstrip()

    # get android version
    def adb_get_android_version(self):
        result = self.adb_command("shell getprop ro.build.version.release")
        return result.rstrip().lstrip()

    # get device ip
    # 不考虑异常情况，暂时不考虑Android老版本兼容问题
    def adb_get_device_ip(self):
        result = self.adb_command("shell ifconfig wlan0")
        print("1:", result)
        s1 = result.rstrip().lstrip().split(":")[1][-9:-5]
        print("2:", s1)
        if s1 == "inet":
            s2 = result.rstrip().lstrip().split(":")[2][:13]
            print("s2:", s2)
            return s2
        else:
            print("error!")
            return

        # get device mac

    def adb_get_device_mac(self):
        result = self.adb_command("shell cat /sys/class/net/wlan0/address")
        return result.rstrip().lstrip()

    # get device cpu info
    def adb_get_device_cpu_info(self):
        result = self.adb_command("shell cat /proc/cpuinfo")
        return result.rstrip().lstrip()

    # get device cpu %
    def adb_get_device_cpu_rate(self):
        result = self.adb_command('shell dumpsys cpuinfo | find "%s"' % (mc.package_name))
        return result.rstrip().lstrip()

    # get 系统内存信息
    # VSS- Virtual Set Size 虚拟耗用内存（包含共享库占用的内存）
    # RSS- Resident Set Size 实际使用物理内存（包含共享库占用的内存）
    # PSS- Proportional Set Size 实际使用的物理内存（比例分配共享库占用的内存）
    # USS- Unique Set Size 进程独自占用的物理内存（不包含共享库占用的内存）
    # 说明：
    # 一般来说内存占用大小有如下规律：VSS >= RSS >= PSS >= USS
    # 实际在统计查看某个进程内存占用情况的时候，看PSS是比较客观的
    # def adb_get_device_mem(self):
    # 	result = self.adb_command("shell cat /proc/meminfo")
    # 	return result.rstrip().lstrip()

    # get total mem
    def adb_get_device_mem(self):
        # result = self.adb_command("shell cat /proc/meminfo").split("\n")[0].split(":")[1].rstrip().lstrip()
        result = self.adb_command("shell cat /proc/meminfo").split("\n")[0][:-2]
        return str(result.rstrip().lstrip())

    # 获取package_name应用内存信息
    def adb_get_device_mem_all(self):
        result = self.adb_command('shell dumpsys meminfo | find "%s"' % (mc.package_name))
        return result.split("\n")[0].rstrip().lstrip()

    # 获取应用内存信息
    def adb_get_device_pid_mem(self):
        result = self.adb_command("shell dumpsys meminfo %s" % (mc.package_name))
        return result.rstrip().lstrip()

    # get total cpu 使用时间
    # need further dealing with result
    def adb_get_cpu_time(self):
        result = self.adb_command("shell cat /proc/stat")
        return result.strip()

    # get pid cpu 使用时间
    # need further dealing with result
    def adb_get_pid_cpu_time(self, pid):
        result = self.adb_command("shell cat /proc/%s/stat" % (pid))
        return result.rstrip().lstrip()

    # get package fps
    def adb_get_pid_fps(self):
        result = self.adb_command("shell dumpsys gfxinfo %s" % (mc.package_name))
        return result.rstrip().lstrip()

    # get pid 流量
    # 还需要研究，先不用
    # def adb_get_pid_flow(self):

    # get pid
    def adb_get_pid(self):
        result = self.adb_command("shell ps |findstr %s" % (mc.package_name)).split()[1]
        print("1:", result)
        return result.rstrip().lstrip()

    # get uid
    def adb_get_uid(self):
        pid = self.adb_get_pid(mc.package_name)
        result = self.adb_command("shell cat /proc/%s/status" % (pid)).split("\n")[7].split(":")[1].split()[0]
        print("1:", result)
        return result.rstrip().lstrip()

    # get app start time
    # 有bug 还需要调试
    def adb_get_app_start_time(self, activity_name):
        result = self.adb_command("shell am start -W %s" % (activity_name))
        print("1:", result)
        return result.rstrip().lstrip()

    # 查看单个应用程序最大内存限制
    def adb_get_heapgrowthlimit(self):
        result = self.adb_command('shell getprop | find "heapgrowthlimit"').split(":")[1].rstrip().lstrip()[1:5]
        print("1:", result)
        return result.rstrip().lstrip()


if __name__ == '__main__':
    pass
