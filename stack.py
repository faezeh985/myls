#!usr/bin/env python3

class Stack(object):
    def __init__(self,lst=[]):
        self.lst = lst

    def top(self):
        if len(self.lst) > 0:
            return self.lst[len(self.lst)-1]
        else:
            return None

    def pop(self):
        if len(self.lst) > 0:
            return self.lst.pop()
        else:
            return None

    def length(self):
        return len(self.lst)

    def push(self, x):
        return self.lst.append(x)
