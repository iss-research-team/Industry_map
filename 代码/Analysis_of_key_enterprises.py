# -*- codeing = utf-8 -*-
# @Author :Liu Ming
# @File ：Analysis_of_key_enterprises.py
# @Time : 2022/1/13 9:12
import csv

from pyecharts import options as opts
from pyecharts.charts import Geo, Page, Map


def analysis_of_key_enterprises():
    page = Page(layout=Page.SimplePageLayout)
    # 1.绘制产业规模分析图，按省来划分每种产业随时间的分布
    csv_readA = list(csv.reader(open("data\\产业A.csv", 'r')))
    csv_readB = list(csv.reader(open("data\\产业B.csv", 'r')))
    length = len(csv_readA)
    area_list = csv_readA[0]
    start_year = 2011
    for i in range(1, length):
        arr_A = []
        arr_B = []
        for j in range(1, len(area_list)):
            arr_A.append([area_list[j], csv_readA[i][j]])
            arr_B.append([area_list[j], csv_readB[i][j]])
        geo1 = (
            Map(init_opts=opts.InitOpts(width="800px", height="600px"))
                .add("刀具产业", arr_A, "china")
                .set_global_opts(
                title_opts=opts.TitleOpts(title="产业规模分析图".format(i + start_year)),
                visualmap_opts=opts.VisualMapOpts(max_=1614 + 4003),
            )
                .add("滚珠丝杠产业", arr_B, "china")
        )
    # 2.绘制产业规模分步图，根据企业的地址和企业的资本绘图
    geo2 = (
        Geo(init_opts=opts.InitOpts(width="800px", height="600px"))
            .add_coordinate_json("data/analysis_of_key_enterprises.json")
            .add_schema(maptype="china")
            .add("数控机床企业", [["A企业", 100],
                            ["B企业", 80],
                            ["C企业", 15],
                            ["D企业", 54],
                            ["E企业", 84],
                            ["F企业", 25], ])
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(is_piecewise=True),
            title_opts=opts.TitleOpts(title="产业规模分布图"),
        )
    )

    page.add(geo1)
    page.add(geo2)
    page.render("output\\analysis_of_key_enterprises.html")


if __name__ == '__main__':
    analysis_of_key_enterprises()
