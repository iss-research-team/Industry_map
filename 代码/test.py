#-*- codeing = utf-8 -*-
#@Author :hcy
#@File ：test
#@Time : 2022/1/19-15:52

import jieba
from gensim import corpora,models,similarities
doc1 = './data/policy1.txt'
doc2 = './data/policy2.txt'
doc3 = './data/policy.txt'
list1 = jieba.lcut(open(doc1,encoding='utf-8').read())
list2 = jieba.lcut(open(doc2,encoding='utf-8').read())
list3=jieba.lcut(open(doc3,encoding='utf-8').read())
list1_2 = [list1,list2]
print(list1_2)
#创建语料库
dictionary = corpora.Dictionary(list1_2)
#保存语料库
# dictionary.save("./output/dict.txt")
#获取语料库
corpus = [dictionary.doc2bow(i) for i in list1_2]
tfidf = models.TfidfModel(corpus)
#特征数
featureNUM = len(dictionary.token2id.keys())
#通过TfIdf对整个语料库进行转换并将其编入索引，以准备相似性查询
index = similarities.SparseMatrixSimilarity(tfidf[corpus],num_features=featureNUM)
#稀疏向量.dictionary.doc2bow(doc)是把文档doc变成一个稀疏向量，[(0, 1), (1, 1)]，表明id为0,1的词汇出现了1次，至于其他词汇，没有出现。
new_vec = dictionary.doc2bow(list3)
#计算向量相似度
sim = index[tfidf[new_vec]]
print(sim)