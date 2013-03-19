__author__ = 'han wang'
import STL
import copy

q = STL.Queue()
s = STL.Stack()
trace = {}

#Goal state and initial state
g = [1,2,3,4,5,6,7,8,0]
a = [2,7,3,1,0,6,5,4,8]

#list to string
def l2str(z):
    b = ''
    for i in z:
        b+=str(i)
    return b

#string to list
def str2l(b):
    c = []
    for i in b:
        c.append(int(i))
    return c

#initialize
def init():
    trace.update({l2str(a):0})
    q.enqueue(a)

def record(z,b):
    trace.update({l2str(b):l2str(z)})
    q.enqueue(b)
    
def display(z):
    for i in range(3):
        print z[3*i:3*i+3]
    print

def unvisited(z):
    if l2str(z) in trace:
        return False
    return True

def up(z,o):
    b = copy.deepcopy(z)
    b[o] = b[o-3]
    b[o-3] = 0
    return b

def down(z,o):
    b = copy.deepcopy(z)
    b[o] = b[o+3]
    b[o+3] = 0
    return b

def left(z,o):
    b = copy.deepcopy(z)
    b[o] = b[o-1]
    b[o-1] = 0
    return b

def right(z,o):
    b = copy.deepcopy(z)
    b[o] = b[o+1]
    b[o+1] = 0
    return b

def move(z):
    for o in range(9):
        if z[o] == 0:
            break
    if o > 2 and unvisited(up(z,o)):
        record(z,up(z,o))
    if o < 6 and unvisited(down(z,o)):
        record(z,down(z,o))
    if o%3 > 0 and unvisited(left(z,o)):
        record(z,left(z,o))
    if o%3 < 2 and unvisited(right(z,o)):
        record(z,right(z,o))

#BFS       
def bfs():
    while unvisited(g):
        if q.isempty():
            break
        else:
            move(q.head())
            q.dequeue()

def show():
    s.push(g)
    while trace.get(l2str(s.top())) != 0:
        s.push(str2l(trace.get(l2str(s.top()))))
    while s.isempty() == False:
        display(s.top())
        s.pop()
    
if __name__ == '__main__':
    init()
    bfs()
    show()
