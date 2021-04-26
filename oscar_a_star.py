#Oscar Barbosa Aquino
#23/08/2019
#Based on code by Ajinkya Sonawane
import random

class Node:
    def __init__(self,data,level,val,parent,direction):
        self.data = data
        self.level = level
        self.val = val
        self.parent = parent
        self.prevDir = direction

    def generate_child(self):
        x,y = self.find(self.data,'0')
        val_list = [[[x,y-1],"L"],[[x,y+1],"R"],[[x-1,y],"U"],[[x+1,y],"D"]]
        children = []
        for i in val_list:
            child = self.changePlaces(self.data,x,y,i[0][0],i[0][1])
            if child is not None:
                child_node = Node(child,self.level+1,0,self,i[1])
                children.append(child_node)
        return children
        
    def changePlaces(self,puz,x1,y1,x2,y2):
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data):
            temp_puz = []
            temp_puz = self.copy(puz)
            temp = temp_puz[x2][y2]
            temp_puz[x2][y2] = temp_puz[x1][y1]
            temp_puz[x1][y1] = temp
            return temp_puz
        else:
            return None
            
    def copy(self,root):
        temp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp    
            
    def find(self,puz,x):
        for i in range(0,len(self.data)):
            for j in range(0,len(self.data)):
                if puz[i][j] == x:
                    return i,j
    
    def compare(self,node):
        if self.data == node.data:
            if self.val < node.val:
                return 0 #Better value
            if self.val == node.val:
                return 1 #Equal value
            if self.val > node.val:
                return 2 #Same value
        else:
            return -1 #They're different

class Puzzle:
        
    def __init__(self,size):
        self.n = size
        self.open = dict()
        self.closed = dict()
        self.min = []

    def toTuple(self,l):
        return tuple(tuple(x) for x in l)

    def accept(self):
        puz = []
        for _ in range(0,self.n):
            temp = input().split(",")
            puz.append(temp)
        return self.toTuple(puz)

    def f(self,start,goal):
        return self.h(start.data,goal)-self.g(start.level)

    def g(self,level):
        return level*(0.001)

    def h(self,start,goal):
        temp = 0
        size = range(0,self.n)
        for i in size:
            for j in size:
                curr = start[i][j]
                if curr != "0":
                    for z in size:
                        for k in size:
                            if goal[z][k] == curr:
                                temp+=abs(i-z)+abs(j-k)
                                break;
        return temp
        
    def printM(self, current):
        if current is not None:
            for i in current.data:
                for j in i:
                    print('{num:2d}'.format(num=int(j)), end=" ")
                print()

    def insertMin(self, data, val):
        inserted = False
        
        if self.min == []:
            self.min.append([data,val])
            inserted=True
        else:
            for i in range(0,len(self.min)):
                if self.min[i][1] > val:
                    self.min.insert(i,[data,val])
                    inserted=True
                    break;
        if inserted==False:
            self.min.append([data,val])
        
    def updateMin(self, data, val):        
        for i in range(0,len(self.min)):
            if self.min[i][0] == data:
                self.min[i][1] = val
                break;

    def solve(self,start, goal, open, closed, f, h, debug):
        start.val = f(start,goal)
        self.open[start.data] = start
        self.insertMin(start.data, start.val)

        while True:           

            key,val = self.min.pop(0)

            current = open[self.toTuple(key)]
            closed[self.toTuple(key)] = 1
            
            if(h(current.data,goal) == 0):
                return current
            
            kids = current.generate_child()

            for node in kids:
                node.val = f(node,goal)
                if closed.get(self.toTuple(node.data))==None: #Not in closed                    
                    key = self.toTuple(node.data) #key
                    if open.get(key) == None: #First time seeing it
                        open[key] = node
                        self.insertMin(node.data, node.val)
                    else:
                        if node.compare(open[key]) == 0: #If better, replace, else, do nothing
                            open[key] = node
                            self.updateMin(node.data, node.val)

    def process(self,debug, start, goal):
        start = Node(start,0,0, None, "Start")
        
        f = self.f
        h = self.h

        start.val = f(start,goal)
        
        self.open[start.data] = start
        self.min.append( [start.data,start.val] )

        current = self.solve(start,goal,self.open,self.closed,f,h, debug)
        
        s = ""
        while current.prevDir != "Start":
            s = current.prevDir+","+s
            current=current.parent
        # print(s[0:-1])

def main(puz,start,goal):
    puz.process(0, start, goal)

from time import time

if __name__ == "__main__":
    n = int(input())
    puz = Puzzle(n)
    start = puz.accept()
    goal = puz.accept()

    # import cProfile
    # cProfile.run('main(puz,start, goal)')

    promedio = []
    iteraciones = 1000

    for i in range(iteraciones):
        initial = time()
        main(puz,start, goal)
        final = time()
        puz.open = dict()
        puz.closed = dict()
        puz.min = []
        promedio.append(final-initial)
        if i % int(iteraciones / 10) == 0:
            print(i)
    print(f"ETA: {sum(promedio)/iteraciones}")
