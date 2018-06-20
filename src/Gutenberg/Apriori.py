# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 20:11:48 2018

@author: spy
"""
from dataHandle import DataSet
import math

'''
    Apriori：用于进行Apriori算法，挖掘频繁项集
'''
class Apriori:
    def __init__(self):
        #设置最小支持度，此处设置为0.5%
        self.minSupport_Percent = 0.5
        #获得Baskets，调用dataHandle中的DataSet进行处理
        self.Baskets = DataSet("../../data/Lincoln/").getParagraphs()
        #获得最小支持度代表多少个事务
        self.BasketNum = len(self.Baskets)
        self.minSupport = int(self.minSupport_Percent * self.BasketNum /100)
        #频繁项集的输出位置
        self.resultFile = "../../result/ResultView.txt"
        #保存频繁项集
        self.Items = {}

    '''
        Function：获得一阶项集
        Principle：统计每个篮子，计算获得符合最小支持度要求的一阶频繁项集
        Use：获得一阶项集
    '''
    def get_L1(self):
        #一阶频繁项集的候选集
        L1_Candidates = {}
        #L存放一阶频繁项集
        L = [] 
        #对每一个篮子进行统计
        for sentence in self.Baskets:
            #对每一个单词统计在篮子中出现的次数
            for word in sentence:
                if word in L1_Candidates:
                    L1_Candidates[word] = L1_Candidates[word] + 1
                else:
                    L1_Candidates[word] = 1
        #打开文件，在文件中写一阶频繁项集，同时将一阶频繁项集添加到L中
        result = open(self.resultFile, "a+")
        for word in L1_Candidates:
            if L1_Candidates[word] >= self.minSupport:
                L.append([word])
                result.write(word + "|" + str(L1_Candidates[word]/self.BasketNum) + "\n")
                self.Items[word] = L1_Candidates[word]/self.BasketNum
        result.close()
        return L
   

    '''
        Function：从上一阶频繁项集获得新一阶的频繁项集候选集
        Principle：统计频繁项集中的所有单词，形成k个元素的组合作为候选集
        Use：获得高一阶频繁项集的候选集
    ''' 
    def getCandidates(self, L):
        #C用于储存新的频繁项集
        C = []
        wordItems = set()
        #得到L中的所有单词
        for item in L:
            for word in item:
                wordItems.add(word)
        wordItems = list(wordItems)
        #对于每一个频繁项，随意再加一个单词，获得长度+1的candidate
        for item in L:
            for word in wordItems:
                if word in item:
                    continue
                tempList = item.copy()
                tempList.append(word)
                tempList.sort()
                if not tempList in C:
                    C.append(tempList)
        return C
    '''
        Function: 对候选集进行剪枝，去掉存在子集不在上一阶频繁项集的候选项
        Principle：如果一个集合是频繁项集，则它的所有子集都是频繁项集。
        Use：对候选集进行剪枝
    '''
    def getValidC(self, C, L):
        validC = []
        #对每一个C中的item进行检查
        for item in C:
            words = item
            check_not_in = False #每次剔除一个单词，检查剩下的单词是不是都在L中
            for word in words:
                tmpwords = words.copy()
                #剔除单词的操作
                tmpwords.remove(word) 
                tmpwords.sort()
                if not tmpwords in L:
                    check_not_in = True
                    break
            #如果所有子集都在L中，就添加进validC中
            if (check_not_in == False):
                validC.append(item)
        return validC
            
    '''
        Function: 统计每个候选项在篮子中出现的次数，找出频繁项集
        Principle：计数，检查是否满足最小支持度
        Use：从候选集获得频繁项集
    '''                   
    def countValidC(self, C, k):
        #countC用于记录每个频繁项出现的次数
        countC = {}
        #valid是最终的频繁项集
        validC = []
        #打开文件，写频繁项集
        result = open(self.resultFile, "a+")
        #统计每个频繁项集在篮子中出现的次数
        for sentence in self.Baskets:
            for item in C:
                words = item
                #这个label用于检查是不是这个频繁项的所有单词都在一个事务中
                check_all_in_sentence = True
                for word in words:
                    if not word in sentence:
                        check_all_in_sentence = False
                        break
                #如果都在一个事务中，单词的相应计数+1
                if check_all_in_sentence == True:
                    #这里做了编码，把单词组合成字符串，作为keyValue
                    keyValue = ""
                    for word in item:
                        keyValue = keyValue + "+" + word
                    if keyValue in countC:
                        countC[keyValue] = countC[keyValue] + 1
                    else:
                        countC[keyValue] = 1
        #选出符合最小支持度的频繁项集，添加并输出
        for keyValue in countC:
            item = keyValue.split("+")[1:]    
            if countC[keyValue] >= self.minSupport:
                validC.append(item)
                for word in item:
                    result.write(word + " ")
                result.write("|" + str(countC[keyValue]/self.BasketNum) + "\n")
                self.Items[keyValue] = countC[keyValue]/self.BasketNum
        result.close()
        return validC
    
    '''
        Function: Apriori算法的主入口！
        Principle：循环直到新一阶的频繁项集为空
        Use：获得所有频繁项集
    '''               
    def getFrequentItems(self):
        #获得一阶频繁项集
        C = self.get_L1()
        L = C
        k = 1
        #循环直到新一阶的频繁项集为空
        while(len(L) != 0):
            k = k + 1
            #获得频繁项集候选集
            C = self.getCandidates(L)
            #对频繁项集候选集进行剪枝
            C = self.getValidC(C, L)
            #统计出现频率，检查是否满足最小支持度的要求，获得新一阶频繁项集
            L = self.countValidC(C, k)
        #返回频繁项集
        return self.Items
    
        
if __name__ == '__main__':
    a = Apriori()
    a.getFrequentItems()
