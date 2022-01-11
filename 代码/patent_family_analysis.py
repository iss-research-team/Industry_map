# encoding: utf-8
"""
@author: zhou
@time: 2022/1/11 10:52
@file: patent_family_analysis.py
@desc: 
"""

import csv
import json
import webbrowser
from collections import defaultdict
from math import ceil

from pyecharts import options as opts
from pyecharts.charts import Map, Page


# import webbrowser
# from snapshot_phantomjs import snapshot
# from pyecharts.render import make_snapshot


class DrawPage:

    def __init__(self, data_patent: dict):
        self.data_patent = data_patent

    def draw_page(self):
        page = Page(layout=Page.DraggablePageLayout)

        all_patent = self.data_patent["All"]
        dead_patent = self.data_patent["Dead"]
        alive_patent = self.data_patent["Alive"]

        page.add(self.map(all_patent, series_name="所有同族专利", title="同族专利全球分布",
                          upper_limit=(ceil(max(list(all_patent.values())) / 100)) * 100))
        page.add(
            self.map(dead_patent, series_name="失效同族专利", title="失效同族专利全球分布",
                     upper_limit=(ceil(max(list(dead_patent.values())) / 100)) * 100))
        page.add(
            self.map(alive_patent, series_name="有效同族专利", title="有效同族专利全球分布",
                     upper_limit=(ceil(max(list(alive_patent.values())) / 100)) * 100))

        page.render("同族专利分布情况" + ".html")
        webbrowser.open("同族专利分布情况" + ".html")

    def map(self, data: dict, series_name, title="", upper_limit=300):
        # 数据
        country = list(data.keys())
        count = list(data.values())

        c = (
            Map()
                .add(series_name, [list(z) for z in zip(country, count)], "world")
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(
                title_opts=opts.TitleOpts(title=title),
                visualmap_opts=opts.VisualMapOpts(max_=upper_limit),
            )
        )
        return c
        # webbrowser.open("map_world.html")
        # make_snapshot(snapshot, grid.render(), "test.png")  # 仅支持中文路径


class DataProcess:
    """
    数据处理，将专利数据中同族专利相关的内容提取出来，并转化为pyecharts画图所需的数据
    """
    def __init__(self, data_path: str):
        self.path = data_path
        self.file = csv.reader(open(self.path, "r", encoding="utf8"))
        self.data = {"All": defaultdict(int), "Dead": defaultdict(int), "Alive": defaultdict(int)}
        # 专利号前两位与国家名称 字典
        self.trans = json.load(open("../data/country.json", "r", encoding="utf8"))

        next(self.file)
        # 打印检索式，并且跳过前面两行总览信息
        print(self.file.__next__()[0])

    def data_process(self):
        header = self.file.__next__()
        pos = header.index("DWPI 同族专利成员 失效/有效")
        if pos:
            for line in self.file:
                patent_num = line[0]
                try:
                    self.data["All"][self.trans[patent_num[0:2]]] += 1  # 先统计本专利，再统计同族专利
                except:
                    pass

                patent_family = line[pos].split(" | ")
                self.get_patent_detail(patent_family)

    def get_patent_detail(self, patents):
        for patent in patents:
            patent_num = patent.split()[0]
            patent_state = patent.split()[1]

            if patent_state in self.data:
                try:
                    self.data[patent_state][self.trans[patent_num[0:2]]] += 1
                except:
                    pass
            try:
                self.data["All"][self.trans[patent_num[0:2]]] += 1
            except:
                pass


if __name__ == '__main__':
    # 世界地图数据
    task = DataProcess("../data/patent_demo.csv")
    task.data_process()

    test = DrawPage(task.data)
    test.draw_page()
