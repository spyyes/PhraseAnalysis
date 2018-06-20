# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 20:17:26 2018

@author: spy
"""

import nltk 
import os
import re

'''
	DataSet ： 用于进行数据预处理
'''
class DataSet:
    
    def __init__(self, DataDir):
        self.Data_Dir = DataDir
        self.File_Lists = []
        self.StopWords = "./stop_words.txt"
        self.Sentences = []
        self.Paragraphs = []
        self.getAllFiles()
    
    
    ''' 
        Function：获得数据集(DataDir目录)下所有文件名 
        Principle：利用os.listdir获取文件名
        Use：在__init__函数中使用
    '''
    def getAllFiles(self):
        os.chdir(self.Data_Dir)
        names = os.listdir(self.Data_Dir)
        self.File_Lists = names
    
    
    '''
        Function：将分句结果保存在Self.Sentences，并返回
        Principle：将文本连起来，调用nltk.tokenizer工具进行分句
        Use：以Sentence为Basket，获得Baskets
    '''
    def getSentences(self):
        self.Sentences = []
        #从文件中读取所有停止词，在分句的同时去掉停止词
        stop_file = open(self.StopWords, "r")
        del_list = stop_file.readlines()[0].split(',')
        for k in range(0, len(del_list)):
            del_list[k] = del_list[k].strip()
        stop_file.close()
        #nltk工具，用于分句
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        #对每个数据集中的txt文件，进行分句
        
        ss = 0
        for file in self.File_Lists:
            #打开数据txt文件
            book = open(self.Data_Dir + file, "r")
            book_Lines = book.readlines()
            book.close()
            
            Paras = []
            #One_Paragraph是临时的一段，遇到空行提交
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
            ss = ss + len(Paras)
            for p in Paras:
                #将文件的所有行连成一段，再进行分句
                One_Paragraph = p    
                sentences = tokenizer.tokenize(One_Paragraph)
                #去除停止词
                for s in sentences:
                    s_words = s.split()
                    #保存这句sentence清洗后（停止词、纯字母）的结果
                    s_word_list = []
                    for word in s_words:
                        #将所有字母之外的元素去除
                        word = re.sub("[^a-zA-Z]", "", word)
                        #转化成小写字母
                        word = word.lower()
                        #如果word是停止词或是没有字母，就将其从sentences中去除
                        if word == "" or word in del_list:
                            continue
                        s_word_list.append(word)
                    #去除这个Sentence中的重复单词
                    s_word_list = list(set(s_word_list))
                    #将这句Sentence加入Sentences集合
                    if len(s_word_list) == 0:
                        continue
                    self.Sentences.append(s_word_list)
        return self.Sentences
    
    
    '''
        Function：将分段结果保存在self.Paragraphs中，并返回
        Principle：如果有空行就表示一个段落结束
        Use：以Paragraph为Basket，获得Baskets
    '''   
    def getParagraphs(self):
        #从文件中读取所有停止词，在分句的同时去掉停止词
        stop_file = open(self.StopWords, "r")
        del_list = stop_file.readlines()[0].split(',')
        for k in range(0, len(del_list)):
            del_list[k] = del_list[k].strip()
        stop_file.close()
        
        self.Paragraphs = []
        
         #对每个数据集中的txt文件，进行分句
        for file in self.File_Lists:
        	#打开数据txt文件
            Paras = [] #存放临时的所有段落
            book = open(self.Data_Dir + file, "r")
            book_Lines = book.readlines()
            book.close()

            #One_Paragraph是临时的一段，遇到空行提交
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
                #保存这个paragraph清洗后（停止词、纯字母）的结果
                p_word_list = []
                for word in p_words:
                	##将所有字母之外的元素去除
                    word = re.sub("[^a-zA-Z]", "", word)
                    #转化成小写字母
                    word = word.lower()
                    #如果word是停止词或是没有字母，就将其从paragraphs中去除
                    if word == "" or word in del_list:
                        continue
                    p_word_list.append(word)
                if len(p_word_list) == 0:
                    continue
      			#执行去重操作
                p_word_list = list(set(p_word_list))
                #将这句Sentence加入Sentences集合
                if len(p_word_list) == 0:
                    continue
                self.Paragraphs.append(p_word_list)
        return self.Paragraphs
    
if __name__ == '__main__':
    d = DataSet("C:/Users/spy/Desktop/PhraseAnalysis/Lincoln/")
    #p = d.getParagraphs()
    s = d.getSentences()
    #p = d.getParagraphs()

            