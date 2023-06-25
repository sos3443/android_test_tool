# -*- coding: UTF-8 -*-
import os
from pyecharts import Bar, Line, Page, Overlap
# from pyecharts.charts import Overlap
from MyConfig import MyConfig
from lib.AppPickle import OperatePickle

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(os.path.realpath('__file__')), p))  # os.path.realpath(path)  返回path的真实路径
pick = OperatePickle()
mc = MyConfig()


# 0: 空闲状态--Free
# 1：中等压力--Medium
# 2：满压力--Full
# 3：手动--Manual

class Report(object):
    def __init__(self, reportName, flag):
        self.reportName = reportName
        self.pack = mc.package_name
        self.flag = flag

    def createComparReport(self):
        pass

    def createReport(self):
        lisMem = pick.read_info(mc.info_dir + '_' + self.pack + '_' + self.flag + "_mem.pickle")
        lisCpu = pick.read_info(mc.info_dir + '_' + self.pack + '_' + self.flag + "_cpu.pickle")
        lisbattery = pick.read_info(mc.info_dir + '_' + self.pack + '_' + self.flag + "_battery.pickle")
        # lisappruntime = pick.read_info(mc.info_dir + '_' + self.pack + '_' + self.flag + "_appruntime.pickle")
        lisliuliang = pick.read_info(mc.info_dir + '_' + self.pack + '_' + self.flag + "_liuliang.pickle")
        lisDevinfo = pick.read_info(mc.info_dir + "info.pickle")[0]
        print("lisDevinfo:", lisDevinfo)
        # release phone_name phone_model screen_size mem_total cpu_sum
        release = str(lisDevinfo["release"])
        print(lisDevinfo["release"])
        phone_name = str(lisDevinfo["phone_name"])
        print(lisDevinfo["phone_name"])
        phone_model = str(lisDevinfo["phone_model"])
        print(lisDevinfo["phone_model"])
        screen_size = str(lisDevinfo["screen_size"])
        print(lisDevinfo["screen_size"])
        mem_total = str(lisDevinfo["mem_total"])
        print(lisDevinfo["mem_total"])
        cpu_sum = str(lisDevinfo["cpu_sum"])
        print(lisDevinfo["cpu_sum"])

        devinfo = "版本号:" + release + "\\" \
                  + "手机名称:" + phone_name + "\\" \
                  + "手机型号:" + phone_model + "\\" \
                  + "屏幕尺寸:" + screen_size + "\\" \
                  + "CPU核数:" + cpu_sum + "\\" \
                  + "内存容量：" + mem_total + "MB"

        v1 = [i for i in lisCpu if type(i) == str]
        v2 = [i for i in lisCpu if type(i) != str]
        v3 = [i for i in lisMem if type(i) == str]
        v4 = [i for i in lisMem if type(i) != str]
        v5 = [i for i in lisbattery if type(i) == str]
        v6 = [i for i in lisbattery if type(i) != str]
        # v7 = [i for i in lisappruntime if type(i) == str]
        # v8 = [i for i in lisappruntime if type(i) != str]
        v9 = [i for i in lisliuliang if type(i) == str]
        v10 = [i for i in lisliuliang if type(i) != str]

        page = Page(self.reportName)
        # page = Page(self.reportName.decode('utf-8'))
        attr = v1
        bar = Bar()
        bar.add("qiyu_bar", attr, v2)
        # bar.add_xaxis(attr)
        # bar.add_yaxis(v2)
        line = Line(self.reportName + "-" + "CPU占用", devinfo, width=1200, height=400)
        line.add("qiyu_line", attr, v2, is_stack=True, is_label_show=True,
                 is_smooth=False, is_more_utils=True, is_datazoom_show=False, yaxis_formatter="%",
                 mark_point=["max", "min"], mark_line=["average"])
        # bar.add(line)
        overlap = Overlap(self.reportName + "-" + "CPU占用", width=1200, height=400)
        overlap.add(line)
        overlap.add(bar)
        page.add(overlap)

        attr1 = v3
        line1 = Line(self.reportName + "-" + "MEM消耗", width=1200, height=400)
        line1.add("qiyu_line", attr1, v4, is_stack=True, is_label_show=True, is_smooth=False, is_more_utils=True,
                  is_datazoom_show=False,
                  yaxis_formatter="MB", mark_point=["max", "min"], mark_line=["average"])
        bar1 = Bar()
        bar1.add("qiyu_bar", attr1, v4)
        overlap1 = Overlap(width=1200, height=400)
        overlap1.add(line1)
        overlap1.add(bar1)
        page.add(overlap1)

        attr5 = v5
        line5 = Line(self.reportName + "-" + "电量剩余", width=1200, height=400)
        line5.add("qiyu_line", attr5, v6, is_stack=True, is_label_show=True, is_smooth=False, is_more_utils=True,
                  is_datazoom_show=False,
                  yaxis_formatter="%", mark_point=["max", "min"], mark_line=["average"])
        bar5 = Bar()
        bar5.add("qiyu_bar", attr5, v6)
        overlap5 = Overlap(width=1200, height=400)
        overlap5.add(line5)
        overlap5.add(bar5)
        page.add(overlap5)

        # attr7 = v7
        # line7 = Line(self.reportName + "-" + "启动时间", width=1200, height=400)
        # line7.add("qiyu_line", attr7, v8, is_stack=True, is_label_show=True, is_smooth=False, is_more_utils=True,
        #           is_datazoom_show=False,
        #           yaxis_formatter="ms", mark_point=["max", "min"], mark_line=["average"])
        # bar7 = Bar()
        # bar7.add("qiyu_bar", attr7, v8)
        # overlap7 = Overlap(width=1200, height=400)
        # overlap7.add(line7)
        # overlap7.add(bar7)
        # page.add(overlap7)
        # page.render(mc.report_dir + "_" + self.pack + "_" + self.flag + "_" + "report.html")

        line9 = Line(self.reportName + "-" + "下载流量", width=1200, height=400)
        line9.add("qiyu_line", v9, v10, is_stack=True, is_label_show=True, is_smooth=False, is_more_utils=True,
                  is_datazoom_show=False,
                  yaxis_formatter="KB", mark_point=["max", "min"], mark_line=["average"])
        bar9 = Bar()
        bar9.add("qiyu_bar", v9, v10)
        overlap9 = Overlap(width=1200, height=400)
        overlap9.add(line9)
        overlap9.add(bar9)
        page.add(overlap9)

        page.render(mc.report_dir + "_" + self.pack + "_" + self.flag + "_" + "report.html")


if __name__ == '__main__':
    # rep= Report("乐学高考 V3.1.3 性能测试报告", "Manual")
    # rep = Report("乐学培优家长端 V2.2.1 性能测试报告", "Manual")
    rep = Report(mc.report_name, "Manual")
    # rep= Report("乐学培优教师端 V2.0.0 性能测试报告", "Manual")
    rep.createReport()
