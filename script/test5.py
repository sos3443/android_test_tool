# coding=utf-8
import os
import math
import subprocess
import time
from lib.AdbLibCom import AdbLibCom
adb = AdbLibCom()

class Test5(object):

    def getLiuliang(self):
        pid = adb.adb_get_pid("com.stoneenglish")
        print("pid", pid)
        uid = adb.adb_get_uid("com.stoneenglish")
        print("uid", uid)
        # 获取UID对应的Traffic
        getTrafficcmd = 'adb shell cat /proc/net/xt_qtaguid/stats | grep ' + uid
        for i in range(10000):
            currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            traffic_initial = [0] * 16
            traffic_prefix = []
            p = subprocess.Popen(getTrafficcmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            k=p.stdout.readlines()

            for line in k:

                ll = line.strip()
                ll2 = ll.decode().replace(' ', ',')
                ll2_list = ll2.split(',')
                traffic_list = ll2_list[5:]
                traffic_prefix = ll2_list[0:4]
                traffic_list_int = [int(e) for e in traffic_list]

                traffic_initial = [x + y for x, y in zip(traffic_initial, traffic_list_int)]
                # print traffic_list
                # print(currentTime + "," + ll2)
            retval = p.wait()
            print(traffic_initial)
            traffic_list_str = [str(e) for e in traffic_initial]
            print(traffic_prefix+ traffic_list_str)
            traffic = ','.join(traffic_prefix + traffic_list_str)
            # print(currentTime + ',' + traffic)

            time.sleep(6)
            print('-----------')


    def getFlow(self):
        pid = adb.adb_get_pid("com.stoneenglish")
        flow_info = os.popen("adb shell cat /proc/"+pid+"/net/dev").readlines()
        t = []
        flow =[0,0]
        for info in flow_info:
            temp_list = info.split()
            t.append(temp_list)
        # k1=math.ceil(int(t[6][1])/1024)
        # k2=math.ceil(int(t[6][9])/1024)
        flow[0]=t[6][1] # 下载
        flow[1]=t[6][9] # 发送
        # print(flow)
        return flow
    def getliuliang(self):
        T=[0,0]
        t1=Test5().getFlow()
        time.sleep(1)
        t2 = Test5().getFlow()
        k1=int(t2[0])-int(t1[0])
        k2 = int(t2[1])-int(t1[1])
        T[0]=math.ceil(k1/1024)
        T[1] = math.ceil(k2/1024)
        # T[1]=k2/1024
        # print("1111",T[0])
        # print("222",T[1])
        return T[0]
if __name__=='__main__':

    # Test5().getLiuliang()
    for i in range(30):
        Test5().getliuliang()