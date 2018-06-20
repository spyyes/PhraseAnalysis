# -*- coding: utf-8 -*-


from dataset import load_data

def active(data, stat):
    '''
        Function： 统计每一年的每个论文的Author
        Principle：遍历数据集，进行统计
    '''
    res = {}
    for author in stat["author"]:
        res[author] = {}
        for conference in stat["Conference"]:
            res[author][conference] = {}
    #对每一条记录进行统计
    for d in data:
        author = d["author"]
        year = d["year"]
        conference = d["Conference"]
        for a in author:
            if year in res[a][conference].keys():
                res[a][conference][year] += 1
            else:
                res[a][conference][year] = 1
    return res
    
def find_active(a, stat, minsup = 5):
    '''
        寻找满足最小支持度要求的一阶项集（也就是作者的集合）
    '''
    res = {}
    for conf in stat["Conference"]:
        res[conf] = {}
        for year in stat["year"]:
            res[conf][year] = []
    #判断是否满足最小置信度的要求
    for author in a.keys():
        for conf in a[author].keys():
            for year in a[author][conf].keys():
                if a[author][conf][year] > minsup:
                    res[conf][year].append(author)
                
    return res
    
if __name__ == "__main__":
    #加载数据
    data, stat = load_data()
    authors = {}
    for conf in stat["Conference"]:
        authors[conf] = []
    for d in data:
        author = d["author"]
        conf = d["Conference"]
        for a in author:
            if a not in authors[conf]:
                authors[conf].append(a)
    
    f = open("../result/authors.txt", "w", encoding="utf8")
    for key in authors.keys():
        count = 0
        f.write(("%s:\n" % key))
        for author in authors[key]:
            count += 1
            f.write(("%s, " % author))
            if count % 5 == 0:
                f.write("\n")
        f.write("\n\n")
    f.close()

    a = active(data, stat)
    #选取最小支持度为：每年发表4篇论文
    res = find_active(a, stat, 4) 
    act = {}
    #按照年份和会议对作者进行划分
    for conf in stat["Conference"]:
        act[conf] = []
    for author in a.keys():
        for conf in res.keys():
            if author in res[conf][2015] or author in res[conf][2016] or author in res[conf][2017]:
                act[conf].append(author)
    #打开文件进行输出
    f = open("../result/active_authors.txt", "w", encoding="utf8")
    for key in act.keys():
        count = 0
        f.write(("%s:\n" % key))
        for author in act[key]:
            count += 1
            f.write(("%s, " % author))
            if count % 5 == 0:
                f.write("\n")
        f.write("\n\n")
    f.close()
  