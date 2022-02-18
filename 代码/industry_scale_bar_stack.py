#-*- codeing = utf-8 -*-
#@Author :hcy
#@File ：industry_scale_analysis
#@Time : 2022/2/18-11:36

from pyecharts import options as opts
from pyecharts.charts import Bar
import random

xdata=["杭州市","宁波市","温州市","嘉兴市","湖州市","绍兴市","金华市","衢州市","舟山市","台州市","丽水市"]


def values(start: int = 5, end: int = 50) -> list:
    return [random.randint(start, end) for _ in range(11)]

c = (
    Bar()
    .add_xaxis(xdata)
    .add_yaxis("机床主轴厂家数量", values(), stack="stack1")
    .add_yaxis("驱动电机厂家数量", values(), stack="stack1")
    .add_yaxis("伺服电机厂家数量", values(), stack="stack1")
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(title_opts=opts.TitleOpts(title="Bar-堆叠数据（全部）"))
    .render("./output/bar_stack0.html")
)
