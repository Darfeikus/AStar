#Oscar Barbosa Aquino
#23/08/2019
#Based on code by Ajinkya Sonawane
import random

class Node:
    def __init__(self,data,level,val,parent,direction):
        self.data = data
        self.level = level
        self.val = val
        #Direction
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
        self.open = set()
        self.closed = set()

    def accept(self):
        puz = []
        for _ in range(0,self.n):
            temp = input().split(",")
            puz.append(temp)
        return puz

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
                print("")
            print()

    def solve(self,start, goal, open, closed, f, h, debug):

        while True:           
            
            current = min(open,key = lambda x:x.val)
            
            if(h(current.data,goal) == 0):
                return current

            open.remove(current)
            closed.add(current)

            if debug==1:
                print("---------------------")                
                self.printM(current)
                print(f"f(M) =  {current.val}")
                print(f"g(M) =  {current.level}")
            
            kids = current.generate_child()

            for i in kids:
                
                i.val = f(i,goal)
                alreadyClosed=False
                old = None
                
                for k in closed:
                    if i.data == k.data:
                        alreadyClosed=True
                        break
                
                if alreadyClosed==False: #Not in closed

                    for k in open: #Search if it hasn't been visited
                        if i.data == k.data:
                            old = k
                            break
                
                    if old==None: #First time seeing it
                        open.add(i)
                    else:
                        if i.compare(old) == 0: #If better, replace, else, do nothing
                            open.remove(old)
                            open.add(i)

    def process(self,debug):
        start = self.accept()
        goal = self.accept()

        start = Node(start,0,0, None, "Start")
        
        f = self.f
        h = self.h

        start.val = f(start,goal)
        self.open.add(start)

        current = self.solve(start,goal,self.open,self.closed,f,h, debug)
        
        s = ""
        while current.prevDir != "Start":
            s = current.prevDir+","+s
            current=current.parent
        print(s[0:-1])

def main():
    n = int(input())
    puz = Puzzle(n)
    puz.process(0)

from time import time

if __name__ == "__main__":
    initial = time()
    main()
    final = time()
    print(f'ETA: {final - initial}')