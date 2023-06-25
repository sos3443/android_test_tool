# coding=utf-8
import subprocess
import time
from lib.AdbLibCom import AdbLibCom
adb = AdbLibCom()

class Test4(object):

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
            k2 = p.stdout.readline()
            for line in p.stdout.readlines():
                print('hello')
                ll = line.strip()
                ll2 = ll.replace(' ', ',')
                ll2_list = ll2.split(',')
                traffic_list = ll2_list[5:]
                traffic_prefix = ll2_list[0:4]
                traffic_list_int = [int(e) for e in traffic_list]

                traffic_initial = [x + y for x, y in zip(traffic_initial, traffic_list_int)]
                # print traffic_list
                print(currentTime + "," + ll2)
            retval = p.wait()
            print(traffic_initial)
            traffic_list_str = [str(e) for e in traffic_initial]
            print(traffic_prefix+ traffic_list_str)
            traffic = ','.join(traffic_prefix + traffic_list_str)
            print(currentTime + ',' + traffic)

            time.sleep(6)
            print('-----------')

if __name__=='__main__':
    Test4().getLiuliang()