# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 20:11:48 2018

@author: spy
"""
from dataHandle import DataSet
class Apriori:
    def __init__(self):
        self.minSupport_Percent = 1
        self.Baskets = DataSet("C:/Users/spy/Desktop/PhraseAnalysis/lincoln/").getParagraphs()
        self.minSupport = int(self.minSupport_Percent * len(self.Baskets) /100)
        self.resultFile = "C:/Users/spy/Desktop/PhraseAnalysis/result.txt"

    def get_L1(self):
        L1_Candidates = {}
        L = []
        for sentence in self.Baskets:
            for word in sentence:
                if word in L1_Candidates:
                    L1_Candidates[word] = L1_Candidates[word] + 1
                else:
                    L1_Candidates[word] = 1
        result = open(self.resultFile, "a+")
        for word in L1_Candidates:
            if L1_Candidates[word] >= self.minSupport*10:
                L.append([word])
                result.write(word + "|" + str(L1_Candidates[word]) + "\n")
        result.close()
        return L
    
    def getCandidates(self, L):
        C = []
        wordItems = set()
        #得到L中的所有单词
        for item in L:
            for word in item:
                wordItems.add(word)
        wordItems = list(wordItems)
        #获得长度+1的candidate
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
        Function: 对候选集的检查1
        检查是不是子集都在L中
    '''
    def getValidC(self, C, L):
        validC = []
        #对每一个C中的item进行检查
        for item in C:
            words = item
            check_not_in = False #每次剔除一个单词，检查剩下的单词是不是都在L中
            for word in words:
                tmpwords = words.copy()
                tmpwords.remove(word) #剔除单词的操作
                tmpwords.sort()
                if not tmpwords in L:
                    check_not_in = True
                    break
            #如果所有子集都在L中，就添加进validC中
            if (check_not_in == False):
                validC.append(item)
        return validC
            
    '''
        Function: 对候选集的检查2
        计数，检查是否满足最小支持度
    '''                   
    def countValidC(self, C):
        countC = {}
        validC = []
        result = open(self.resultFile, "a+")
        for sentence in self.Baskets:
            for item in C:
                words = item
                check_all_in_sentence = True
                for word in words:
                    if not word in sentence:
                        check_all_in_sentence = False
                        break
                if check_all_in_sentence == True:
                    keyValue = ""
                    for word in item:
                        keyValue = keyValue + "+" + word
                    if keyValue in countC:
                        countC[keyValue] = countC[keyValue] + 1
                    else:
                        countC[keyValue] = 1
        for keyValue in countC:
            item = keyValue.split("+")[1:]        
            if countC[keyValue] >= self.minSupport:
                validC.append(item)
                for word in item:
                    result.write(word + " ")
                result.write("|" + str(countC[keyValue]) + "\n")
        result.close()
        return validC

    def run(self):
        C = self.get_L1()
        L = C
        while(len(L) != 0):
            C = self.getCandidates(L)
            #print(len(C))
            C = self.getValidC(C, L)
            L = self.countValidC(C)
            
        
if __name__ == '__main__':
    a = Apriori()
    a.run()
        