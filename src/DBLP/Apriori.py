# -*- coding: utf-8 -*-


from dataset import load_data
from dataset import split_by_item
import Itemset

class apriori():
    #初始化
    def __init__(self):
        
        self.L = []
        self.C = []
        self.k = 0
    #获得一阶频繁项集
    def L_1(self, data, minsup):
        
        self.L.append([])
        self.C.append([])
        self.k = 1
        
        candidates = []
        for i in data:
            for j in i:
                if j not in candidates:
                    candidates.append(j)
        sup = [0 for i in candidates]
        for i in data:
            for j in i:
                sup[candidates.index(j)] += 1
        
        sets = []
        for i in range(len(sup)):
            if sup[i] >= minsup:
                sets.append(set([candidates[i]]))
                    
        self.L.append(sets)
        self.C.append([])
    # 挖掘候选集  
    def C_k_p_1(self):
        
        L = self.L[self.k]
        sets = Itemset.add_1(L)
        new_sets = []
        for s in sets:
            tmp = Itemset.sub_1(s)
            flag = False
            for i in tmp:
                if i not in L:
                    flag = True
                    break
            if not flag:
                new_sets.append(s)
        self.C.append(new_sets)
    #挖掘频繁项集    
    def L_k_p_1(self, data, minsup):
        
        C = self.C[self.k + 1]
        sup = [0 for i in C]
        for d in data:
            for c in range(len(sup)):
                if C[c].issubset(set(d)):
                    sup[c] += 1
        sets = []
        for c in range(len(sup)):
            if sup[c] >= minsup:
                sets.append(C[c])
        self.L.append(sets)
        self.k += 1
        
        
if __name__ == "__main__":
    
    _data, stat = load_data()
    s_data = split_by_item(_data, stat, "year")
    data = s_data[stat["year"][0]]
    _input = []
    for d in data:
        _input.append([])
        for author in d['author']:
            _input[-1].append(author)
    miner = apriori()
    
    miner.L_1(_input, 3)
    while not miner.L[miner.k] == []:
        print (miner.k, len(miner.C[miner.k]), len(miner.L[miner.k]))
        miner.C_k_p_1()
        miner.L_k_p_1(_input, 3)
    