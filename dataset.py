# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 08:36:18 2018

@author: spy
"""
import re
import os


class Data_Init:
    def __init__(self, DataDir):
        self.Data_Dir = DataDir
        self.File_Lists = []
        self.StopWords = "C:/Users/spy/Desktop/PhraseAnalysis/stop_words.txt"
        self.Authors = []
        self.getAllFiles()
        self.getAuthors()
    
    ''' 获得数据集(DataDir目录)下所有文件名 '''
    def getAllFiles(self, ):
        os.chdir(self.Data_Dir)
        names = os.listdir(self.Data_Dir)
        self.File_Lists = names
    
    ''' 获得数据集中所有作者名 '''
    def getAuthors(self,):
        Authors = []
        for file in self.File_Lists:
            author = file.split("_")[0]
            Authors.append(author)
        self.Authors = list(set(Authors))

    ''' 获得某本书所有词语 '''
    def getWords(self, bookName):
        stop_file = open(self.StopWords, "r")
        del_list = stop_file.readlines()[0].split(',')
        for k in range(0, len(del_list)):
            del_list[k] = del_list[k].strip()
        stop_file.close()
        
        book = open(self.Data_Dir + bookName, "r")
        book_Lines = book.readlines()
        book.close()
        book_Words = {}
        for line in book_Lines:
            words = line.split()
            for word in words:
                word = re.sub("[^a-zA-Z]", "", word)
                word = word.lower()
                if word == "" or word in del_list:
                    continue
                if word in book_Words:
                    book_Words[word] = book_Words[word] + 1
                else:
                    book_Words[word] = 1
        return (book_Words)
    
    ''' 获得数据集中所有作者名 '''
    def getWordsByAuthor(self, author):
        Author_Words = {}
        for bookName in self.File_Lists:
            if not author in bookName:
                continue
            bookWords = self.getWords(bookName)
            for word in bookWords:
                if word in Author_Words:
                    Author_Words[word] = Author_Words[word] + 1
                else:
                    Author_Words[word] = 1

        Author_Words = sorted(Author_Words.items(), key=lambda d: d[1])
        #Author_Words = sorted(Author_Words.items(), key=lambda d: d[1], reverse = True)
        print(Author_Words)
        print(len(Author_Words))

if __name__ == '__main__':
    Da = Data_Init("C:/Users/spy/Desktop/PhraseAnalysis/Lincoln/")
    Da.getWordsByAuthor("Abraham Lincoln")
