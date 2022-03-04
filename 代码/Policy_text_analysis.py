# -*- codeing = utf-8 -*-
# @Author :hcy
# @File ：Policy_text_analysis
# @Time : 2022/1/11-10:35

import wordcloud
import matplotlib.pyplot as plt
from random import randint
import jieba
import jieba.analyse
from gensim import corpora,models,similarities
import os
import xmnlp


plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

xmnlp.set_model('./model/xmnlp-onnx-models')

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


def wc_show(word_counts, word_num, height, width):
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
    wc.to_file('./output/词云.jpg')  # 保存为背景图1
    # image_colors = wordcloud.ImageColorGenerator(mask)  # 从背景图建立颜色方案
    # wc.recolor(color_func=image_colors)  # 将词云颜色设置为背景图方案
    plt.imshow(wc)  # 显示词云
    plt.axis('off')  # 关闭坐轴
    plt.show()  # 显示图像


def get_tf_idf(txtpath, top):
    """tf_idf关健词获取
        输入：文本、词的数量
        输出：tf_idf前top个词
    """
    with open(txtpath, 'r', encoding="utf-8") as file:
        text = file.read()
    tags = jieba.analyse.extract_tags(text, topK=top, allowPOS=('ns','n'))
    return '、'.join(tags)


def get_textrank(txtpath, top):
    """textrank关健词获取
        输入：文本、词的数量
        输出：textrank前top个关健词
    """
    with open(txtpath, 'r', encoding="utf-8") as file:
        text = file.read()
    tags = jieba.analyse.textrank(text, topK=top)
    return '、'.join(tags)


def text_similarity(txtpath,txtpah):
    """t_idf文本相似度
        输入：文本
        输出：相似度
    """
    policy_text_list=[]
    for file in os.listdir(txtpath):
        file_path = os.path.join(txtpath, file)
        policy_text_list.append(jieba.lcut(open(file_path, encoding='utf-8').read()))

    mypolicy = jieba.lcut(open(txtpah, encoding='utf-8').read())
    # 创建词典
    dictionary = corpora.Dictionary(policy_text_list)
    # 获取语料库
    corpus = [dictionary.doc2bow(i) for i in policy_text_list]
    tfidf = models.TfidfModel(corpus)
    # 特征数
    featureNUM = len(dictionary.token2id.keys())
    # 通过TfIdf对整个语料库进行转换并将其编入索引，以准备相似性查询
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=featureNUM)
    # 稀疏向量.dictionary.doc2bow(doc)是把文档doc变成一个稀疏向量，[(0, 1), (1, 1)]，表明id为0,1的词汇出现了1次，至于其他词汇，没有出现。
    new_vec = dictionary.doc2bow(mypolicy)
    # 计算向量相似度
    sim = index[tfidf[new_vec]]
    i=0
    res=[]
    for file in os.listdir(txtpath):
        newdict=[file,sim[i]]
        res.append(newdict)
        i+=1
    res.sort(key=lambda x:x[1],reverse=True)
    return res


def sentiment_analysis(txtpath):
    """情感分析
        输入：文本
        输出：情感分析结果
    """
    with open(txtpath, 'r', encoding="utf-8") as file:
        text = file.read()
    sentiment_list=[xmnlp.sentiment(text)[0],xmnlp.sentiment(text)[1]]
    labels = ['negative', 'positive']
    plt.pie(x=sentiment_list, labels=labels,autopct='%0.1f%%')
    plt.show()

def keyword_bar(txtpath,stopword,n):
    dic=word_frequency(txtpath, stopword)
    keyword_list=sorted(dic.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    x=[]
    y=[]
    for i in range(n):
        x.append(keyword_list[i][0])
        y.append(keyword_list[i][1])
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.bar(x=x, height=y)
    ax.set_title("政策文本词频统计", fontsize=15)
    plt.show()

if __name__ == "__main__":
    # dic = word_frequency("./data/政策文本/1.txt", "./data/stopword.txt")
    # wc_show(dic, 100, 1200, 1600)
    # print(get_tf_idf("./data/policy.txt", 10))
    # print(get_textrank("./data/policy.txt",10))
    # print(text_similarity("./data/政策文本","./data/政策文本/1.txt"))
    # sentiment_analysis("./data/政策文本/0.txt")
    keyword_bar("./data/政策文本/1.txt", "./data/stopword.txt",10)
