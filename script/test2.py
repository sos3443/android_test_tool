import os
import time
from MyConfig import MyConfig
mc = MyConfig()
class App(object):


 # 获取App启动时间
    def getRunAppTime(self):

        # 启动APP
        cmd = 'adb shell am start -W -n %s/%s'%(mc.package_name,mc.activity_name)
        self.content = os.popen(cmd)
        time.sleep(5)
        # 获取启动total时间
        totalTime =0
        for line in self.content.readlines():
            if "TotalTime" in line:
                totalTime = line.split(":")[1].strip()

                break
        # 停止APP
        cmd = "adb shell input keyevent 3"
        os.popen(cmd)
        return  totalTime

if __name__=="__main__":

     result= App().getRunAppTime()
     print(result)