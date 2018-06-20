# -*- coding: utf-8 -*-


import pickle, gzip

def process_data(path="../data/FilteredDBLP.txt"):
    
    f = open(path, 'r', encoding="utf8")
    lines = f.readlines()
    f.close()
    
    words = []
    for line in lines:
        words.append(line.strip("\n").split("\t"))
        
    data = []
    conferences = ['IJCAI', 'AAAI', 'COLT', 'CVPR', 'NIPS', 'KR', 'SIGIR', 'SIGKDD']
    tmp = None
    cnt = 0
    for w in words:
        if w[0] == '#########':
            tmp = {"author": [], "title": "", "id": None,
                   "year": None, "Conference": ""}
        elif w[0] == 'author':
            tmp['author'].append(w[1])
        elif w[0] == 'title':
            tmp['title'] = w[1]
        elif w[0] == 'year':
            tmp['year'] = int(w[1])
        elif w[0] == 'Conference':
            for c in conferences:
                if c in w[1] or c.upper() in w[1] or c.lower() in w[1]:
                    tmp['id'] = cnt
                    tmp['Conference'] = c
                    data.append(tmp)
                    cnt += 1
                    if cnt % 1000 == 0:
                        print ("%d processed." % cnt)
                    break
            if "KDD" in w[1] or "kdd" in w[1]:
                tmp['id'] = cnt
                tmp['Conference'] = c
                data.append(tmp)
                cnt += 1
                if cnt % 1000 == 0:
                    print ("%d processed." % cnt)
    
    return data
    
def stat_data(data):
    
    stat = {"author": [], "title": [],
            "year": [], "Conference": []}

    for d in data:
        for i in d["author"]:
            if i not in stat["author"]:
                stat["author"].append(i)
        if d['title'] not in stat["title"]:
            stat["title"].append(d['title'])
        if d['year'] not in stat["year"]:
            stat["year"].append(d['year'])
        if d['Conference'] not in stat["Conference"]:
            stat["Conference"].append(d['Conference'])
    
    return stat
    
def store_data(data, stat, path="../data/DBLP.pkl.gz"):
    
    f = gzip.open(path, 'wb')
    pickle.dump({"data": data, "stat": stat}, f)
    f.close()
    
def load_data(path="../data/DBLP.pkl.gz"):
    
    f = gzip.open(path, 'rb')
    data = pickle.load(f)
    f.close()
    
    return data["data"], data["stat"]

def split_by_item(data, stat, item):
    
    if item not in stat.keys():
        return None
        
    s_data = {}
    for i in stat[item]:
        s_data[i] = []

    for d in data:
        s_data[d[item]].append(d)
    
    return s_data
        
def get_L(path):
    
    f = gzip.open(path, 'rb')
    L = pickle.load(f)
    f.close()
    return L
    
if __name__ == "__main__":
    
    #data = process_data()
    #stat = stat_data(data)
    #store_data(data, stat)
    data, stat = load_data()
    s_data = split_by_item(data, stat, "year")