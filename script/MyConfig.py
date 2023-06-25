# -*- coding: UTF-8 -*-

import os


class MyConfig(object):
    # 包名
    # package_name = "com.lexue.courser" # gaokao
    # package_name = "com.stoneenglish" # peiyou
    package_name = "com.qiyu.android.vrapp"  # qiyu app
    # package_name = "com.stoneenglish.teacher" # peiyouteacher
    # 活动名
    # activity_name = ".main.view.MainActivity" # gaokao
    # activity_name = ".SplashActivity" # peiyou
    activity_name = ".MainActivity"  # qiyu first activity
    # activity_name = ".teacher.SplashActivity" # peiyouteacher
    # 网络名
    net_name = "wifi"
    # monkey parameters
    monkey_parameters_full = "--throttle 50 --ignore-crashes --ignore-timeouts --pct-touch 80 --pct-trackball 5 " \
                             "--pct-appswitch 9 --pct-syskeys 1 --pct-motion 5 -v -v -v 10000 "
    monkey_parameters_medi = "--throttle 50 --ignore-crashes --ignore-timeouts --pct-touch 80 --pct-trackball 5 " \
                             "--pct-appswitch 9 --pct-syskeys 1 --pct-motion 5 -v -v -v 5000 "
    monkey_seed = 200

    # 报告名称
    report_name = "奇遇Android客户端 V2.0.0 性能测试报告"

    # 网络状态 wifi-wlan0/移动数据-rmnet0
    net_status = "wlan0"

    # log dir
    log_dir = os.path.dirname(os.path.realpath(__file__)) + "\\log"
    # 性能数据目录
    info_dir = os.path.dirname(os.path.realpath(__file__)) + "\\info" + "\\"
    # report路径
    report_dir = os.path.dirname(os.path.realpath(__file__)) + "\\report\\"

    # 获取脚本执行时间，也就是采样时间
    @staticmethod
    def get_time1(self, flag):
        seed = ""
        if flag == 1:
            seed = MyConfig().monkey_parameters_full
        elif flag == 2:
            seed = MyConfig().monkey_parameters_medi
        else:
            seed = 0
        str_list = seed.split()
        x = str_list[1]
        y = str_list[-1]
        print(x)
        print(y)
        return int(x) * int(y) / 1000

    # 初始化pickle文件，不管是否存在直接创建
    @staticmethod
    def prepare_pickle(self):
        pickle_file = [MyConfig.info_dir + "_" + MyConfig.package_name + "_cpu_.pickle",
                       MyConfig.info_dir + "_" + MyConfig.package_name + "_mem_.pickle",
                       MyConfig.info_dir + "_" + MyConfig.package_name + "_battery_.pickle",
                       MyConfig.info_dir + "_" + MyConfig.package_name + "_liuliang_.pickle"]
        for i in pickle_file:
            if os.path.exists(i):
                os.remove(i)
                f = open(i, "w")
                f.close()
            else:
                f = open(i, "w")
                f.close()
