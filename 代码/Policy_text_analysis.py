# -*- codeing = utf-8 -*-
# @Author :hcy
# @File ：Policy_text_analysis
# @Time : 2022/1/11-10:35

import wordcloud
import matplotlib.pyplot as plt
from random import randint
from PIL import Image
import numpy as np
import jieba
import json


def word_frequency(txtpath, stopword):
    """词频获取 
    输入：txt文本路径、停用词txt文本路径
    输出：词频字典
    """

    with open(txtpath, 'r', encoding="utf-8") as file:
        novel = file.read()
    stopwordlist = []
    with open(stopword, 'r', encoding="utf-8") as f:
        for ann in f.readlines():
            ann = ann.strip('\n')  # 去除文本中的换行符
            stopwordlist.append(ann)

    # 去除标点符号
    punctuation = {'\n', ' ', '。', '，', '；', '：', '！', '？', '、'}
    for l in punctuation:
        novel = novel.replace(l, '')
    # 结巴分词
    no_list = list(jieba.cut(novel))
    dic = dict()
    for i in no_list:
        if len(i) != 1:
            dic[i] = novel.count(i)
    # 删除停用词
    for word in stopwordlist:
        if word in dic:
            dic.pop(word)

    print(sorted(dic.items(), key=lambda kv: (kv[1], kv[0]), reverse=True))
    return dic


def wc_show(word_counts,word_num,height,width):
    """词云生成
    输入：词频字典、词云图次数量、词云图高、词云图宽
    输出：词云图
    """

    def random_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None,
                          random_state=None):
        """自定义字体色调的函数"""
        # rand_sum = randint(1, 10)   #使主色调为红黄
        # if rand_sum == 1:
        #    h = 45   #选取色调范围
        # else:
        #    h = randint(10,15)
        # s = int(100.0 * 255.0 / 255.0)
        h = int(100.0 * float(randint(0, 255)) / 255.0)
        s = int(100.0 * float(randint(0, 255)) / 255.0)
        l = int(100.0 * float(randint(0, 255)) / 255.0)
        return "hsl({}, {}%, {}%)".format(h, s, l)

    # mask = np.array(Image.open('背景图_1.jpg'))  # 定义词频背景
    wc = wordcloud.WordCloud(
        font_path='C:/Windows/Fonts/simhei.ttf',  # 设置字体格式
        # mask=mask,  # 设置背景图
        max_words=word_num,  # 最多显示词数
        max_font_size=100,  # 字体最大值
        height=height,  # 高
        width=width,  # 宽
        background_color="white",  # 背景色
    )
    wc.scale = 4  # 改善分辨率
    wc.color_func = random_color_func  # 自定义字体色调
    wc.generate_from_frequencies(word_counts)  # 从字典生成词云
    wc.to_file('词云.jpg')  # 保存为背景图1
    # image_colors = wordcloud.ImageColorGenerator(mask)  # 从背景图建立颜色方案
    # wc.recolor(color_func=image_colors)  # 将词云颜色设置为背景图方案
    plt.imshow(wc)  # 显示词云
    plt.axis('off')  # 关闭坐轴
    plt.show()  # 显示图像


if __name__ == "__main__":
    dic = word_frequency("./data/policy.txt", "./data/stopword.txt")
    wc_show(dic,100,1200,1600)
