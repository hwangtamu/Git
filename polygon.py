import os
import re
import csv
import math

export = []
doc = []
data = []
features = []

def catalog():
    for i in range(26):
        contents = os.walk('sketch\\'+str(3466+i))
        for root,dirs,files in contents:
            tmp = []
            for file_a in files:
                tmp.append(os.path.join(root,file_a))
            export.append(tmp)
            tmp = []
    return export

def getdata(filename):
    global doc
    global data
    with open(filename) as f:
        for line in f:
            doc=line.split('><')
    doc = [x[x.find('time'):-1] for x in doc if x.find('point id')!=-1]
    data = [re.findall(r'\d+',x) for x in doc]
    for i in range(len(data)):
        data[len(data)-i-1][0] = float(data[len(data)-i-1][0]) - float(data[0][0])
        data[i][1] = float(data[i][1])
        data[i][2] = float(data[i][2])
    data = [tuple(x) for x in data]
    return data

def write(f):
    for i in collection:
        print i
    csvfile = file(f,'wb')
    writer = csv.writer(csvfile)
    writer.writerow(['f1','f2','f3','f4','f5','f6','f7','f8','f9','f10','f11','f12','f13'])
    writer.writerows(collection)
    csvfile.close()

def feature(data):
    global features
    tmp = (data[2][1]-data[0][1])/math.sqrt((data[2][1]-data[0][1])*(data[2][1]-data[0][1])+(data[2][2]-data[0][2])*(data[2][2]-data[0][2]))
    features.append(tmp)    #1
    tmp = (data[2][2]-data[0][2])/math.sqrt((data[2][1]-data[0][1])*(data[2][1]-data[0][1])+(data[2][2]-data[0][2])*(data[2][2]-data[0][2]))
    features.append(tmp)    #2
    x_max = sorted(data,cmp = lambda x,y:cmp(x[1],y[1]))[-1][1]
    y_max = sorted(data,cmp = lambda x,y:cmp(x[2],y[2]))[-1][2]
    x_min = sorted(data,cmp = lambda x,y:cmp(x[1],y[1]))[0][1]
    y_min = sorted(data,cmp = lambda x,y:cmp(x[2],y[2]))[0][2]
    tmp = math.sqrt((x_max-x_min)*(x_max-x_min)+(y_max-y_min)*(y_max-y_min))
    features.append(tmp)    #3
    tmp = math.atan2((y_max-y_min),(x_max-x_min))
    features.append(tmp)    #4
    tmp = math.sqrt((data[-1][1]-data[0][1])*(data[-1][1]-data[0][1])+(data[-1][2]-data[0][2])*(data[-1][2]-data[0][2]))
    features.append(tmp)    #5
    features.append((data[-1][2]-data[0][2])/tmp)   #6
    features.append((data[-1][1]-data[0][1])/tmp)   #7
    tmp = 0
    x = []
    y = []
    for i in range(len(data)-1):
        x_delta = data[i+1][1] - data[i][1]
        y_delta = data[i+1][2] - data[i][2]
        x.append(x_delta)
        y.append(y_delta)
        tmp += math.sqrt(x_delta*x_delta+y_delta*y_delta)
    features.append(tmp)    #8
    tmp = 0
    tmp_abs = 0
    tmp_sq = 0
    for i in range(len(x)-1):
        tmp += math.atan2((x[i+1]*y[i]-x[i]*y[i+1]),(x[i]*x[i+1]+y[i]*y[i+1]))
        tmp_sq += math.atan2((x[i+1]*y[i]-x[i]*y[i+1]),(x[i]*x[i+1]+y[i]*y[i+1]))*math.atan2((x[i+1]*y[i]-x[i]*y[i+1]),(x[i]*x[i+1]+y[i]*y[i+1]))
        tmp_abs += abs(math.atan2((x[i+1]*y[i]-x[i]*y[i+1]),(x[i]*x[i+1]+y[i]*y[i+1])))
    features.append(tmp)    #9
    features.append(tmp_abs)    #10
    features.append(tmp_sq) #11
    speed = []
    for i in range(len(data)-1):
        speed.append((x[i]*x[i]+y[i]*y[i])/((data[i+1][0]-data[i][0])*(data[i+1][0]-data[i][0]))) # 1000 makes this value into an adequate scale
    tmp = sorted(speed)[-1]
    features.append(tmp)    #12
    tmp = data[-1][0] - data[0][0]
    features.append(tmp)    #13

    
    return features
    
if __name__=='__main__':
    export = []
    data = []
    doc = []
    features = []
    collection = []
    catalog()
    print export
    for i in export:
        for j in i:
            features = []
            feature(getdata(j))
            collection.append(tuple(features))
    write('rubine.csv')
