# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 16:20:51 2018

@author: spy
"""
from Apriori import Apriori
from matplotlib import pyplot as plt
import numpy

'''
	Association：用于发现关联规则
'''
class Association:
    
    def __init__(self):
    	#输出获得的关联规则
        self.Result_Dir = "../../result/Asso_Result_View.txt"
        #频繁项集
        self.Items = {}
        #按照阶数，保存关联规则的置信度
        self.Num = {}
        #关联规则的候选集
        self.candiConfiItems = {}
        #最终获得的关联规则
        self.CondidenceResults = {}
        #最小置信度
        self.minConfidence = 0.56
    
    '''
        Function：获得频繁项集
        Principle：调用Apriori，获得频繁项集
        Use：获得频繁项集
    '''
    def getItemSet(self):
        a = Apriori()
        self.Items = a.getFrequentItems()
    
    '''
        Function：获得关联规则，并画出关联规则分布图
        Principle：
        Use：获得频繁项集
    '''
    def getAssociations(self):
    	#对每个K阶频繁项集，都寻找它和(K-1)阶频繁项集的关系
        for item in self.Items:
            words = item.split("+")
            if len(words) == 1:
                continue
            words = words[1:]
            k = len(words)
            #分子的支持度，也就是项集本身的支持度
            nume_support = self.Items[item]
            #寻找不同的(K-1)阶项集的组合，每次去掉一个元素，形成了(K-1)项集
            for word in words:
                tmpwords = words.copy()
                tmpwords.remove(word)
                if len(tmpwords) == 1:
                    keyValue = tmpwords[0]
                else:
                    keyValue = ""
                    for tmpword in tmpwords:
                        keyValue = keyValue + "+" + tmpword
                #分母的支持度为这些(k-1)元素的组合
                deno_support = self.Items[keyValue]
                #计算置信度
                confidence = nume_support/deno_support
                candiItem = keyValue + " - " + item
                #保存关联规则的候选集及置信度
                self.candiConfiItems[candiItem] = confidence
                #按照K分类，获得(K-1)阶到K阶关联规则置信度的统计数据。
                if k in self.Num:
                    self.Num[k].append(confidence)
                else:
                    self.Num[k] = []
                    self.Num[k].append(confidence)
                
    '''
        Function：按照K分类，画出不同阶关联规则的分布图
        Principle： 按照K分类，画出不同阶关联规则的分布图
        Use：获得统计数据
    '''
    def getStatistics(self):    
       	#按照K分类
        for k in self.Num:
            tmp_list = self.Num[k]
            tmp_list.sort()
            #画出直方图
            plt.hist(tmp_list)
            print(numpy.median(tmp_list))
            plt.title('Statistics about Confidence in '+ str(k) + " ItemSet")
            plt.xlabel('confidence')
            plt.ylabel('item numbers')
            plt.show()
                
    
    '''
        Function：输出关联规则
        Principle： 输出关联规则
        Use：输出前20个关联规则
    '''    
    def out(self):
        self.CondidenceResults = sorted(self.candiConfiItems.items(), key=lambda d: d[1], reverse = True)
        for x in a.CondidenceResults:
            left = x[0].split('-')[0].replace("+", " ")
            right = x[0].split('-')[1].replace("+", " ")
            value = x[1]
            if value > self.minConfidence:
            	print(left +" ============>" + right + "       Condidence= "+str(value)[0:4] )
    
        
if __name__ == "__main__":
    a = Association()
    a.getItemSet()
    a.getAssociations()
    a.getStatistics()
    a.out()