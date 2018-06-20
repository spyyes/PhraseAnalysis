# -*- coding: utf-8 -*-


from dataset import load_data
from dataset import split_by_item
from dataset import get_L
from Apriori import apriori
import gzip, pickle
import os
import re

def process(data_path = "../data/DBLP.pkl.gz",
            dir_path = "../result/topic_of_year/"):
    '''
        Function：寻找关联项集。
        Principle: 运行Apirori算法，寻找频繁项集，然后进行关联项集的挖掘
        Use: 用于寻找关联项集
    '''
    _data, stat = load_data()
    s_data = split_by_item(_data, stat, "year")
    for s in s_data.keys():
        # 加载数据，并且按照author、year等进行划分
        s_data[s] = split_by_item(s_data[s], stat, "Conference")
        for s_ in s_data[s].keys():
            print ("year = %d, Conference = %s" % (s, s_))
            data = s_data[s][s_]
            _input = []
            #使用停止词去除一些数据
            for d in data:
                _input.append([])
                str_ = re.sub("[\:\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+",
                           "", d["title"])
                del_list = ["a", "an", "the", "in", "of", "with", "on", "for",
                            "and", "to", "under", "beyond", "as", "from", "-",
                            "by", "using", "when", "is", "are", "about", "at",
                            "via", "aaai", "papers", "usa", "arizona"]
                words = str_.split()
                for word in words:
                    if word.lower() not in del_list:
                        _input[-1].append(word.lower())
            #加载Apriori模型
            miner = apriori()
            #选择最小支持度为5篇论文 
            miner.L_1(_input, 5)
            while not miner.L[miner.k] == []:
            print ("iter %d, size of C = %d, size of L = %d"
                   % (miner.k, len(miner.C[miner.k]), len(miner.L[miner.k])))
            miner.C_k_p_1()
            miner.L_k_p_1(_input, 5)
            #保存结果
            path = dir_path + str(s) + "_" + str(s_)
            f = gzip.open(path, 'wb')
            pickle.dump(miner.L, f)
            print ("result saved at %s" % path)
            f.close()

def get_result(dir_path="../result/topic_of_year/"):
    '''
        Function：从文件中读取结果
        Pinciple：已经执行完之后，从文件中读取结果，进行显示
    '''   
    files = os.listdir(dir_path)
    ret = {}

    for file in files:
        #print(dir_path + file)
        year, conf = file.split("_")
        if conf not in ret.keys():
            ret[conf] = {}
        ret[conf][int(year)] = get_L(dir_path + file)
        
    return ret
    
def get_topic(res):
    '''
        Funtion：已经执行完之后，获得topic信息
    '''
    ret = {}
    for k in res.keys():
        ret[k] = {}
        for k_ in res[k].keys():
            ret[k][k_] = res[k][k_][-2]
    return ret
    
def save_topic_txt(ts, path="../result/topic.txt"):
    '''
        Function：保存分组信息到txt文件
    '''
    f = open(path, "w", encoding="utf8")
    for key in ts.keys():
        f.write("\n\nConference %s:\n" % key)
        for key_ in ts[key].keys():
            f.write("year %d:\n" % key_)
            for g in range(len(ts[key][key_])):
                f.write(("%d, " % (g+1)))
                for words in ts[key][key_][g]:
                    f.write(words + " ")
                f.write("\n")
    f.close()
    
    
if __name__ == "__main__":
    #执行关联规则挖掘
    process()
    Ls = get_result()
    ts = get_topic(Ls)
    save_topic_txt(ts)
    #显示结果
    for key in ts.keys():
        print ("\nConference %s:\n" % key)
        for key_ in ts[key].keys():
            print ("year %d:" % key_)
            for g in range(len(ts[key][key_])):
                print (("%d" % (g+1)), end=". ")
                for words in ts[key][key_][g]:
                    print (words, end=', ')
                print ("")