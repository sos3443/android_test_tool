import time
import string
import os
from lib.AdbLibCom import AdbLibCom
adb=AdbLibCom()
# 控制类
class Test3(object):

    # 单次测试过程
    def testprocess(self):
        # 执行获取进程的命令
        pid=adb.adb_get_pid("com.stoneenglish")
        print("pid",pid)
        uid=adb.adb_get_uid("com.stoneenglish")
        print("uid",uid)
        # 获取进程ID使用的流量
        traffic = os.popen("adb shell cat /proc/"+pid+"/net/dev")
        receive=0
        transmit=0
        receive2=0
        transmit2=0
        for line in traffic:
            if "wlan0" in line:
                # 将所有空行换成#
                line = "#".join(line.split())
                # 按#号拆分,获取收到和发出的流量
                receive = line.split("#")[1]
                transmit = line.split("#")[9]
            elif "eth1" in line:
                # 将所有空行换成#
                line = "#".join(line.split())
                # 按#号拆分,获取收到和发出的流量
                receive2 = line.split("#")[1]
                transmit2 = line.split("#")[9]

        # 计算所有流量的之和
        # alltraffic = int(receive) + int(transmit) + int(receive2) + int(transmit2)
        alltraffic = int(receive)
        alltraffic2 = int(transmit)
        # 按KB计算流量值
        alltraffic = alltraffic / 1024
        alltraffic2 = alltraffic2 / 1024
        print("alltraffic",alltraffic)
        print("alltraffic2", alltraffic2)
    # 多次测试过程控制
    def run(self):
        while self.counter > 0:
            self.testprocess()
            self.counter = self.counter - 1
            # 每5秒钟采集一次数据
            time.sleep(5)

    # 获取当前的时间戳
    def getCurrentTime(self):
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return currentTime



if __name__ == "__main__":
    Test3().testprocess()