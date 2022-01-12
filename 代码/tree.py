# Author:Joker
# -*- codeing = utf-8 -*-
# @Time :2022/1/11 10:07
# @Author:zsj
# @Site :产业图谱开发
# @File :tree.py
# @Software:PyCharm

import json

from pyecharts import options as opts
from pyecharts.charts import Tree

data = [
    {
        "name": "数控机床产业图谱",
        "children": [
            {
                "name": "上游",
                "children": [
                    {
                        "name": "零部件",
                        "children": [
                            {"name": "机床本体及零部件", "children": [
                                {"name": "床身及底座铸件"}, {"name": "主轴级变速箱"},
                                {"name": "润滑、排屑及冷却"}, {"name": "导轨及滑台"}, ]
                             },
                            {"name": "核心功能部件", "children": [
                                {"name": "刀具"}, {"name": "滚珠丝杠"},
                                {"name": "直线导轨"}, {"name": "液压系统"}, {"name": "启动系统"}]
                             },
                            {"name": "数控系统", "children": [
                                {"name": "高速主轴"}, {"name": "驱动电机"},
                                {"name": "CNC系统"}, {"name": "PLC"},
                                {"name": "伺服电机"}, {"name": "位置检测模块"}]
                             },
                        ]
                    },
                ]
            },
            {
                "name": "中游",
                "children": [
                    {
                        "name": "机床产商",
                        "children": [
                            {"name": "切削机加工加工机床", "children": [
                                {"name": "数控机床"}, {"name": "数控钻床"},
                                {"name": "数控铣床"}, {"name": "数控镗床"},
                                {"name": "数控刨床"}, {"name": "数控拉床"},
                                {"name": "数控磨床"}, {"name": "加工中心"}, ]
                             },
                            {"name": "成型机械加工机床", "children": [
                                {"name": "锻压机床"}, {"name": "冲压机床"},
                                {"name": "折弯机床"}, {"name": "冷拔机床"}, ]
                             },
                        ]
                    },
                ]
            },
            {
                "name": "下游",
                "children": [
                    {
                        "name": "机床应用",
                        "children": [
                            {"name": "汽车", },
                            {"name": "3C类电子", },
                            {"name": "国防", },
                            {"name": "能源设备", },
                            {"name": "船舶", },
                            {"name": "医疗器械", },
                            {"name": "其他领域", },
                        ]
                    },
                ]
            },
        ]
    },
]

c = (
    Tree()
    .add(
        # 系列名称，用于 tooltip 的显示，legend 的图例筛选
        "",

        # 系列数据项
        data,

        # 标记的图形。ECharts 提供的标记类型包括 'emptyCircle', 'circle', 'rect', 'roundRect',
        # 'triangle', 'diamond', 'pin', 'arrow', 'none'。
        symbol = "circle",

        # 标记的大小，可以设置成诸如 10 这样单一的数字，也可以用数组分开表示宽和高，
        # 例如 [20, 10] 表示标记宽为 20，高为 10。
        symbol_size = 5,
        # pos_top = 'middle',
        # pos_left = 'middle',

        #节点间隔
        collapse_interval=1,

        edge_fork_position = "100%",

        # 树图初始展开的层级（深度）。根节点是第 0 层，然后是第 1 层、第 2 层，... ，
        # 直到叶子节点。该配置项主要和 折叠展开 交互一起使用，目的还是为了防止一次展示过多节点，
        # 节点之间发生遮盖。如果设置为 -1 或者 null 或者 undefined，所有节点都将展开。
        initial_tree_depth = -1,

        #方向
        orient="LR",

        # tree组件离容器上侧的距离。
        pos_top = '',

        #标签配置项
        label_opts=opts.LabelOpts(
            position="top",
            horizontal_align="right",
            vertical_align="middle",
            rotate=0,           #字角度
        ),
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="数控机床产业图谱"))
    .render("tree_top_bottom.html")
)