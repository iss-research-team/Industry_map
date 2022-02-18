# -*- codeing = utf-8 -*-
# @Author :hcy
# @File ：industry_scale_bar_time
# @Time : 2022/2/18-11:54

import pyecharts.options as opts
from pyecharts.charts import Timeline, Bar, Pie
import random


def values(start: int = 5, end: int = 50) -> list:
    return [random.randint(start, end) for _ in range(11)]


total_data = {}
name_list = ["杭州市", "宁波市", "温州市", "嘉兴市", "湖州市", "绍兴市", "金华市", "衢州市", "舟山市", "台州市", "丽水市"]
data_gdp = {
    2011: values(3000, 10000),
    2010: values(3000, 9500),
    2009: values(3000, 9000),
    2008: values(3000, 8500),
    2007: values(3000, 8000),
    2006: values(2500, 7500),
    2005: values(2500, 7000),
    2004: values(2000, 6500),
    2003: values(1500, 6000),
    2002: values(1000, 5000),
}

data_pi = {
    2011: values(300, 1000),
    2010: values(000, 950),
    2009: values(300, 900),
    2008: values(300, 850),
    2007: values(300, 800),
    2006: values(250, 750),
    2005: values(250, 700),
    2004: values(200, 650),
    2003: values(150, 600),
    2002: values(100, 500),
}

data_si = {
    2011: values(300, 1000),
    2010: values(000, 950),
    2009: values(300, 900),
    2008: values(300, 850),
    2007: values(300, 800),
    2006: values(250, 750),
    2005: values(250, 700),
    2004: values(200, 650),
    2003: values(150, 600),
    2002: values(100, 500),
}

data_ti = {
    2011: values(300, 1000),
    2010: values(000, 950),
    2009: values(300, 900),
    2008: values(300, 850),
    2007: values(300, 800),
    2006: values(250, 750),
    2005: values(250, 700),
    2004: values(200, 650),
    2003: values(150, 600),
    2002: values(100, 500),
}

def format_data(data: dict) -> dict:
    for year in range(2002, 2012):
        max_data, sum_data = 0, 0
        temp = data[year]
        max_data = max(temp)
        for i in range(len(temp)):
            sum_data += temp[i]
            data[year][i] = {"name": name_list[i], "value": temp[i]}
        data[str(year) + "max"] = int(max_data / 100) * 100
        data[str(year) + "sum"] = sum_data
    return data


total_data["dataGDP"] = format_data(data=data_gdp)
total_data["dataPI"] = format_data(data=data_pi)
total_data["dataSI"] = format_data(data=data_si)
total_data["dataTI"] = format_data(data=data_ti)


def get_year_overlap_chart(year: int) -> Bar:
    bar = (
        Bar()
            .add_xaxis(xaxis_data=name_list)
            .add_yaxis(
            series_name="数控机床产业总值",
            y_axis=total_data["dataGDP"][year],
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add_yaxis(
            series_name="数控机床生产数量",
            y_axis=total_data["dataPI"][year],
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add_yaxis(
            series_name="数控机床企业数量",
            y_axis=total_data["dataSI"][year],
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add_yaxis(
            series_name="数控机床产业从业人员数量",
            y_axis=total_data["dataTI"][year],
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="{}浙江数控产业宏观情况".format(year), subtitle="数据来自浙江省统计局"
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True, trigger="axis", axis_pointer_type="shadow"
            ),
        )
    )

    return bar


# 生成时间轴的图
timeline = Timeline(init_opts=opts.InitOpts(width="1600px", height="800px"))

for y in range(2002, 2012):
    timeline.add(get_year_overlap_chart(year=y), time_point=str(y))

# 1.0.0 版本的 add_schema 暂时没有补上 return self 所以只能这么写着
timeline.add_schema(is_auto_play=False, play_interval=1000)
timeline.render("./output/industry_scale.html")
