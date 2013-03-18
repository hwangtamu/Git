#define STL Queue and Stack class in python

class Queue(object):
    
    def __init__(self):
        self.queue = []
   
    def enqueue(self,elem):
        self.queue.append(elem)
    
    def dequeue(self):
        if self.queue != []:
            return self.queue.pop(0)
        else:
            return None
    
    def head(self):
        if self.queue != []:
            return self.queue[0]
        else:
            return None
    
    def tail(self):
        if self.queue != []:
            return self.queue[-1]
        else:
            return None
    
    def length(self):
        return len(self.queue)
    
    def isempty(self):
        return self.queue == []
    
    
class Stack(object):
    
    def __init__(self):
        self.stack = []
    
    def push(self,elem):
        self.stack.append(elem)
    
    def pop(self):
        if self.stack != []:
            return self.stack.pop(-1)
        else:
            return None
        
    def top(self):
        if self.stack != []:
            return self.stack[-1]
        else:
            return None
        
    def length(self):
        return len(self.stack)
    
    def isempty(self):
        return self.stack == []
