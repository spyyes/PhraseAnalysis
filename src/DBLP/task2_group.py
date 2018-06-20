# -*- coding: utf-8 -*-

from dataset import load_data
from dataset import split_by_item
from dataset import get_L
from Apriori import apriori
import gzip, pickle
import os


def process(data_path = "../data/DBLP.pkl.gz",
            dir_path = "../result/group_of_year/"):
    '''
        Function：寻找关联项集。
        Principle: 运行Apirori算法，寻找频繁项集，然后进行关联项集的挖掘
        Use: 用于寻找关联项集
    '''
    _data, stat = load_data()
    s_data = split_by_item(_data, stat, "year")
    # 加载数据，并且按照author、year等进行划分
    for s in stat["year"]:
        print ("year = %d" % s)
        data = s_data[s]
        _input = []
        for d in data:
            _input.append([])
            for author in d['author']:
                _input[-1].append(author)
        #加载Apriori模型
        miner = apriori()
        #以最小支持度为3个进行一阶频繁项集的挖掘
        miner.L_1(_input, 3)
        #循环直到没有更多频繁项被挖掘出
        while not miner.L[miner.k] == []:
            print ("iter %d, size of C = %d, size of L = %d"
                   % (miner.k, len(miner.C[miner.k]), len(miner.L[miner.k])))
            miner.C_k_p_1()
            miner.L_k_p_1(_input, 3)
        #保存结果
        path = dir_path + str(s)
        f = gzip.open(path, 'wb')
        pickle.dump(miner.L, f)
        f.close()

def get_result(dir_path="../result/group_of_year/"):
    '''
        Function：从文件中读取结果
        Pinciple：已经执行完之后，从文件中读取结果，进行显示
    '''
    files = os.listdir(dir_path)
    ret = {}

    for file in files:
        #print(dir_path + file)
        ret[file] = get_L(dir_path + file)
        
    return ret

def get_group(Ls):
    '''
        Funtion：已经执行完之后，获得分组信息
        Use：被get_groups()调用
    '''
    
    if len(Ls) < 4 or Ls[3] == []:
        return []

    groups = []
    for i in range(len(Ls)-2, 2, -1):
        for j in Ls[i]:
            if j in groups:
                continue
            cont = False
            for g in groups:
                if set(j).issubset(set(g)):
                    cont = True
                    break
            if cont:
                continue
            groups.append(set(j))
    return groups
    

def get_groups(Ls):
    '''
        Funtion：已经执行完之后，获得分组信息
    '''
    groups = {}
    for key in Ls.keys():
        groups[key] = get_group(Ls[key])
    return groups
    
def save_group_txt(gs, path="../result/group.txt"):
    '''
        Function：保存分组信息到txt文件
    '''
    f = open(path, "w", encoding="utf8")
    for key in gs.keys():
        f.write(("year %s:\n" % key))
        for g in range(len(gs[key])):
            f.write(("%d. " % (g+1)))
            for author in gs[key][g]:
                f.write(("%s, " % author))
            f.write("\n")
    f.close()
    
def get_group_data(gs, data):
    '''
        用group的组合从data里寻找全部的记录
    '''
    res = {}
    for key in gs.keys():
        for g_ in gs[key]:
            g = ""
            for a in list(g_):
                g += (a+",")
            if g not in res.keys():
                res[g] = []
            for d in data:
                if len(set(g_).intersection(set(d["author"]))) >= 2:
                    res[g].append(d)
                    
    res_ = res
    res = {}
    for key in res_.keys():
        k1 = set(key.split(","))
        apd = True
        for k in res.keys():
            k2 = set(k.split(","))
            if k1 == k2:
                apd = False
                for tmp in res_[key]:
                    res[k].append(tmp)
        if apd:
            res[key] = res_[key]
                    
    return res
    
def save_group_data(gd, path="../result/group_data.pkl.gz"):
    '''
        Function:保存分组数据
        Principle：调用Pickle工具
    '''
    f = gzip.open(path, "wb")
    pickle.dump(gd, f)
    f.close()
    
def load_group_data(path="../result/group_data.pkl.gz"):
    '''
        Function：加载分组数据
        Principle：调用Pickle工具
    '''
    f = gzip.open(path, "rb")
    ret = pickle.load(f)
    f.close()
    
    return ret
    
    
if __name__ == "__main__":
    #执行关联规则挖掘
    process()
    # 执行完之后，直接读取数据
    #data, stat = load_data()
    #显示结果并保存
    Ls = get_result()
    gs = get_groups(Ls)
    save_group_txt(gs)
    
    gd = get_group_data(gs, data)
    save_group_data(gd)
    gd = load_group_data()
    #显示结果
    for key in gs.keys():
        print ("\nyear %s:" % key)
        for g in range(len(gs[key])):
            print (("%d" % g), end=". ")
            for author in gs[key][g]:
                print (author, end=', ')
            print ("")
            
    