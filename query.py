__author__ = "han wang"

#An ugly draft for debugging Homework 1 of Information Retrieval
#This homework can be found at http://courses.cse.tamu.edu/caverlee/csce670/hw/hw1.html

import os
import collections
import re


wlist = []
export = []
words = []
bindex = []
pindex = []
windex = []
text = []
dictionary = []
keywords = collections.namedtuple('keywords','word bolnindex posindex wcindex')
record_b = set()
record_p = set()
record_w = set()

def getwlist():
#    tmp = []
    contents = os.walk('books')
    for root,dirs,files in contents:
        for file_a in files:
            export.append(os.path.join(root,file_a))
'''    for i in range(len(export)):
        wlist.append([])
        with open(export[i],'r') as f:
            for line in f:
                l = re.findall(r'\w+',line)
                if len(l)>0:
                    tmp += [w.lower() for w in l]
            wlist[i] += tmp
#            file('./dict.txt','a').writelines(str(tmp))
#            file('./dict.txt','a').write('\n')
            tmp = []'''
            
            
def read():
    words = []
    with open('./dict.txt','r') as f:
        for line in f:
            l = re.findall(r'\w+',line)
            l = list(set(l))
            words += l
            words = list(set(words))
    words.sort()
    for i in words:
        file('./list.txt','a').write(str(i)+'\n')


def boolindex():
    bindex = []
    words = []
    with open('./list.txt','r') as f:
        for line in f:
            words.append(str(line)[:-1])
    for i in words:
        tmp = []
        for j in range(len(export)):
            if wlist[j].count(i)>0:
                tmp.append(j)
        bindex.append(tmp)
        file('./bindex.txt','a').writelines(str(tmp)+'\n')

def wcbuild():
    windex = []
    words = []
    with open('./list.txt','r') as f:
        for line in f:
            words.append(str(line[:-1])+'$')
    for i in range(len(words)):
        tmp = []
        for j in range(len(words[i])):
            tmp.append(words[i][j:]+words[i][:j])
        windex.append(tmp)
    file('./windex.txt','w').writelines(str(windex))
        
def mapping():
    words = []
    bindex = []
    with open('./list.txt','r') as f:
        for line in f:
            words.append(str(line)[:-1])
    f.close()
    with open('./bindex.txt','r') as f:
        for line in f:
            tmp = re.findall(r'\d+',line)
            tmp = [int(i) for i in tmp]
            bindex.append(tmp)
    f.close()
    
#    file('./test_1.txt','w').writelines(str(bindex))
    
    
def positional():
    pindex = []
    tmp = []
    with open('./list.txt','r') as f:
        for line in f:
            words.append(str(line)[:-1])
    f.close()
    with open('./bindex.txt','r') as f:
        for line in f:
            tmp = re.findall(r'\d+',line)
            tmp = [int(i) for i in tmp]
            bindex.append(tmp)
    f.close()
    
    for elem in range(len(bindex)):
        for i in bindex[elem]:
            for k in range(len(wlist[i])):
                if wlist[i][k]==words[elem]:
                    tmp.append(k)
            pindex.append(tmp)
            tmp = []
        print words[elem],pindex
        file('./pindex.txt','a').writelines(str(pindex)+'\n')
        pindex = []

def dictbuild():
    collection1 = []
    with open('./list.txt','r') as f:
        for line in f:
            collection1.append(str(line)[:-1])
    f.close()
    print len(collection1),'Word list loaded...'
    
    collection2 = []
    with open('./bindex.txt','r') as f:
        for line in f:
            tmp = re.findall(r'\d+',line)
            tmp = [int(i) for i in tmp]
            collection2.append(tmp)
    f.close()
    print len(collection2),'Index 1 loaded...'
    
    collection3 = []
    with open('./pindex.txt','r') as f:
        for line in f:
            tmp = line.split('], [')
            for i in range(len(tmp)):
                tmp[i] = re.findall(r'\d+',tmp[i])
                tmp[i] = [int(x) for x in tmp[i]]
            collection3.append(tmp)
    f.close()
    print len(collection3),'Index 2 loaded...'
    
    collection4 = []
    with open('./windex.txt','r') as f:
        for line in f:
            collection4 = line.split('], [')
    f.close()
    print len(collection4),'Index 3 loaded...'
    global dictionary
    for i in range(len(collection3)):
        dictionary.append(keywords(word = collection1[i],bolnindex = collection2[i],posindex = collection3[i], wcindex = collection4[i]))
    dictionary = tuple(dictionary)
    print 'Dictionary built...'
    
    
def booleanquery(que):
    global record_b
    tmp = []
    for elem in que:
        for i in range(len(dictionary)):
            if elem!='' and dictionary[i][0] == elem:
                tmp += dictionary[i][1]
    for i in tmp:
        if tmp.count(i) == len(que):
            tmp.remove(i)
            record_b.add(re.findall(r'\d+',export[i])[0])

def phrasequery(que):
    global record_p
    for elem in que:
        tmp_1 = []
        tmp = []
        for x in elem:
            for i in range(len(dictionary)):
                if x!='' and dictionary[i][0] == x:
                    tmp_1.append(i)
                    tmp += dictionary[i][1]
        tmp_3 = []
        for i in tmp:
            if tmp.count(i)==len(elem):
                tmp_3.append(i)
        tmp_3 = list(set(tmp_3))
        tmp = []
        for i in tmp_3:
            tmp_2 = []
            for j in range(len(tmp_1)):
                tmp_2.append(dictionary[tmp_1[j]][2][dictionary[tmp_1[j]][1].index(i)])
            for k in range(len(tmp_2)):
                tmp_2[k] = [int(x)-k for x in tmp_2[k]]
            tmp_2 = re.findall(r'\d+',str(tmp_2))
            for z in tmp_2:
                if tmp_2.count(z)==len(elem):
                    tmp.append(i)
    if tmp!=[]:
        for i in tmp:
            record_p.add(re.findall(r'\d+',export[i])[0])
            
    
def wildcard(que):
    global record_w
    for i in range(len(que)):
        que[i] = str(que[i])+'$'
        que[i] = que[i][que[i].find('*')+1:]+que[i][:que[i].find('*')]
    tmp = []
    for elem in que:
        tmp_1 = []
        for i in range(len(dictionary)):
            if dictionary[i][3].find(elem)!= -1:
                tmp_1 += dictionary[i][1]
        tmp.append(list(set(tmp_1)))
    tmp = re.findall(r'\d+',str(tmp))
    for i in tmp:
        if tmp.count(i) == len(que):
            record_w.add(re.findall(r'\d+',export[int(i)])[0])
    
def query():
    global record,record_b,record_p,record_w
    while True:
        q1=[]
        q2=[]
        q3=[]
        record = set()
        a = raw_input('Query:    ')
        while a.find('"')!=-1:
            q2.append(a[a.find('"')+1:a.find('"',2)].split(' '))
            a=a.replace(a[a.find('"'):a.find('"',2)+1],'')
        q1 = a.split(' ')
        q1 = [x for x in q1 if x!='' and x!=' ']
        q1.sort(key = lambda x:x.count('*'))
        while q1!=[] and q1[-1].count('*')>0:
            q3.append(q1[-1])
            q1.remove(q1[-1])
               
        record_b = set()
        record_p = set()
        record_w = set()   
        
        if q1!=[]:
            booleanquery(q1)
        if q2!=[]:
            phrasequery(q2)
        if q3!=[]:
            wildcard(q3)
        
        if len(record_b)>0:
            record = record_b
        elif len(record_p)>0:
            record = record_p
        elif len(record_w)>0:
            record = record_w
        if len(record_b)>0 and len(record_p)>0:
            record = record_b & record_p
        elif len(record_b)>0 and len(record_w)>0:
            record = record_b & record_w
        elif len(record_p)>0 and len(record_w)>0:
            record = record_p & record_w
        
        if len(record_b)>0 and len(record_p)>0 and len(record_w)>0:
            record = record_b & record_p and record_w
        if len(record) == 0:
            print  'sorry no match :('    
        else:
            for i in record:
                print i,
        print
    
if __name__ == '__main__':
    getwlist()
#    read()
#    boolindex()
#    mapping()
#    positional()
    dictbuild()
    query()
#    wcbuild()
