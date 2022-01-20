# -*- coding: utf-8 -*-
# @Time    : 2022/1/17 17:00
# @Author  : tao xingkai
# @FileName: enterprise_migration_dynamic.py


import os
import pandas as pd
from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import ChartType, SymbolType

# 只需要在顶部声明 CurrentConfig.ONLINE_HOST 即可  解决html空白问题
from pyecharts.globals import CurrentConfig
CurrentConfig.ONLINE_HOST = "http://127.0.0.1:8000/assets/"

# 导入数据
date = pd.read_csv('data/企业迁移数据.csv', encoding='GBK')

# mdate = date[date['count']>100000]
# 挑选人口流入地为广州
sdate = date[date['to'] == '广东']

# 设置pyecharts-assets-master下载路径
c = (
    Geo()
        .add_schema(
        maptype="china",
        itemstyle_opts=opts.ItemStyleOpts(color="#323c48", border_color="white"),
        label_opts=opts.LabelOpts(is_show=True)
    )
        # 设置地图类型，背景和边界颜色
        .add(
        "",
        sdate[['from', 'count']].values.tolist(),
        type_=ChartType.EFFECT_SCATTER,
        color="white",
    )
        # 添加图表类型，点的颜色等
        .add(
        "",
        sdate[['from', 'to']].values.tolist(),
        type_=ChartType.LINES,
        effect_opts=opts.EffectOpts(
            symbol=SymbolType.ARROW, symbol_size=6, color="white"
        ),
        linestyle_opts=opts.LineStyleOpts(curve=0.1),  # 轨迹线弯曲度
    )
        # 添加图表类型，符号类型、大小、颜色等
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        # 系列配置项，忽略标签
        .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            is_piecewise=True,
            pieces=[
                {"min": 0, "max": 1000, "label": "0-1000", "color": "white"},
                {"min": 1001, "max": 5000, "label": "1001-5000", "color": "cyan"},
                {"min": 5001, "max": 10000, "label": "5001-10000", "color": "green"},
                {"min": 10001, "max": 50000, "label": "10001-50000", "color": "yellow"},
                {"min": 50001, "max": 100000, "label": "50001-100000", "color": "blue"},
                {"min": 100001, "max": 500000, "label": "100001-5000000", "color": "blue"}
            ]
        ),
        title_opts=opts.TitleOpts(title="流入广东企业分布", pos_right="center", pos_top="5%")
    )
        # 全局配置项，设置动画、颜色、标题等
        .render("data/流入广东企业分布.html")
    # 把制作完成的图表输出为html文件
)
