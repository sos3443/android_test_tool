# -*- coding: UTF-8 -*-

# 说明

# 通用配置项

# xyAxis：直角坐标系中的 x、y 轴(Line、Bar、Scatter、EffectScatter、Kline)
# dataZoom：dataZoom 组件 用于区域缩放，从而能自由关注细节的数据信息，或者概览数据整体，或者去除离群点的影响。(Line、Bar、Scatter、EffectScatter、Kline、Boxplot)
# legend：图例组件。图例组件展现了不同系列的标记(symbol)，颜色和名字。可以通过点击图例控制哪些系列不显示。
# label：图形上的文本标签，可用于说明图形的一些数据信息，比如值，名称等。
# lineStyle：带线图形的线的风格选项(Line、Polar、Radar、Graph、Parallel)
# grid3D：3D笛卡尔坐标系组配置项，适用于 3D 图形。（Bar3D, Line3D, Scatter3D)
# axis3D：3D 笛卡尔坐标系 X，Y，Z 轴配置项，适用于 3D 图形。（Bar3D, Line3D, Scatter3D)
# visualMap：是视觉映射组件，用于进行『视觉编码』，也就是将数据映射到视觉元素（视觉通道）
# markLine&markPoint：图形标记组件，用于标记指定的特殊数据，又标记线和标记点两种。（Bar、Line、Kline）
# tooltip：提示框组件，用于移动或点击鼠标时弹出数据内容

# 图表详细

# Bar（柱状图/条形图）
# Bar3D（3D 柱状图）
# Boxplot（箱形图）
# EffectScatter（带有涟漪特效动画的散点图）
# Funnel（漏斗图）
# Gauge（仪表盘）
# Geo（地理坐标系）
# Graph（关系图）
# HeatMap（热力图）
# Kline（K线图）
# Line（折线/面积图）
# Line3D（3D 折线图）
# Liquid（水球图）
# Map（地图）
# Parallel（平行坐标系）
# Pie（饼图）
# Polar（极坐标系）
# Radar（雷达图）
# Sankey（桑基图）
# Scatter（散点图）
# Scatter3D（3D 散点图）
# ThemeRiver（主题河流图）
# WordCloud（词云图）

# 用户自定义

# Grid 类：并行显示多张图
# Overlap 类：结合不同类型图表叠加画在同张图上
# Page 类：同一网页按顺序展示多图
# Timeline 类：提供时间线轮播多张图

from pyecharts import Line


class Chart(object):

    # @parameter dev---设备名
    # @parameter chart_name---标题
    # @parameter flag---信号量
    def __init__(self, dev, flag):
        self.dev = dev;
        # self.chart_name = chart_name
        self.flag = flag

    # generate_line_chart---绘制折线图

    # @parameter main_title---主标题
    # @parameter second_title---副标题
    # @parameter data1---生成折线图的数据（数组）
    def generate_line_chart(self, main_title, second_title, data1):
        line = Line(main_title, second_title, width=1200, height=400);
        line.add(main_title, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], data1, is_smooth=True, is_stack=True,
                 is_label_show=True,
                 is_more_utils=True, is_datazoom_show=False, yaxis_formatter="%", mark_point=["max", "min"],
                 mark_line=["average"]);
        line.show_config();
        line.render();
