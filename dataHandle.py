# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 20:17:26 2018

@author: spy
"""

import nltk 
import os
import re

class DataSet:
    
    def __init__(self, DataDir):
        self.Data_Dir = DataDir
        self.File_Lists = []
        self.StopWords = "C:/Users/spy/Desktop/PhraseAnalysis/stop_words.txt"
        self.Sentences = []
        self.getAllFiles()
    
    ''' 获得数据集(DataDir目录)下所有文件名 '''
    def getAllFiles(self):
        os.chdir(self.Data_Dir)
        names = os.listdir(self.Data_Dir)
        self.File_Lists = names
    ''' 获得Sentences '''
    def getSentences(self):
        #获得停止词
        stop_file = open(self.StopWords, "r")
        del_list = stop_file.readlines()[0].split(',')
        for k in range(0, len(del_list)):
            del_list[k] = del_list[k].strip()
        stop_file.close()
        #分句工具
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        for file in self.File_Lists:
            book = open(self.Data_Dir + file, "r")
            book_Lines = book.readlines()
            book.close()
            One_Paragraph = ""
            for line in book_Lines: #把所有练成一个大段再分句
                One_Paragraph = One_Paragraph + " " + line.strip()
            sentences = tokenizer.tokenize(One_Paragraph)
            for s in sentences:
                s_words = s.split()
                s_word_list = []
                for word in s_words:
                    word = re.sub("[^a-zA-Z]", "", word)
                    word = word.lower()
                    if word == "" or word in del_list:
                    #if word == "":
                        continue
                    s_word_list.append(word)
                if len(s_word_list) == 0:
                    continue
                s_word_list = list(set(s_word_list))#执行去重操作
                self.Sentences.append(s_word_list)
        print(len(self.Sentences))
        return self.Sentences
    
    def getParagraphs(self):
        #获得停止词
        stop_file = open(self.StopWords, "r")
        del_list = stop_file.readlines()[0].split(',')
        for k in range(0, len(del_list)):
            del_list[k] = del_list[k].strip()
        stop_file.close()
        
        #分句工具
        Paras = []
        FinalParas = []
        for file in self.File_Lists:
            book = open(self.Data_Dir + file, "r")
            book_Lines = book.readlines()
            book.close()
            One_Paragraph = ""
            for line in book_Lines:
                if line.strip() == "":
                    if One_Paragraph == "":
                        continue
                    else:
                        Paras.append(One_Paragraph)
                        One_Paragraph = ""
                else:
                    One_Paragraph = One_Paragraph + " " + line.strip()

            for p in Paras:
                p_words = p.split()
                p_word_list = []
                for word in p_words:
                    word = re.sub("[^a-zA-Z]", "", word)
                    word = word.lower()
                    if word == "" or word in del_list:
                    #if word == "":
                        continue
                    p_word_list.append(word)
                if len(p_word_list) == 0:
                    continue
                p_word_list = list(set(p_word_list))#执行去重操作
                FinalParas.append(p_word_list)
        return FinalParas
    
if __name__ == '__main__':
    d = DataSet("C:/Users/spy/Desktop/PhraseAnalysis/Lincoln/")
    #p = d.getParagraphs()
    s = d.getSentences()
    print(p[5])
            