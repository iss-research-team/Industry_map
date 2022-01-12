# -*- codeing = utf-8 -*-
# @Author :Liu Ming
# @File ：Industry_Entry
# @Time : 2022/1/12 10:29


import csv
import numpy as np
import pyecharts.options as opts
from pyecharts.charts import Line


def industry_entry():
    csv_read = list(csv.reader(open("data\\月度数据.csv", 'r', encoding='UTF-8')))
    year = csv_read[0]
    x = csv_read[1]
    y = csv_read[2]
    res = np.zeros(len(year) - 1)
    for index in range(len(year) - 1):
            res[index] = (float(x[index]) / float(y[index - 1]))
    (
        Line()
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="企业进入率分析"),
            xaxis_opts=opts.AxisOpts(name="年"),
            yaxis_opts=opts.AxisOpts(name="企业进入率")
            )
            .add_xaxis(xaxis_data=year)
            .add_yaxis(
            series_name="",
            y_axis=res,
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
            .render("basic_line_chart.html")
    )

if __name__ == '__main__':
    industry_entry()







