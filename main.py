#Oscar Barbosa Aquino
#23/08/2019 - 5/3/2021

from time import time

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
            child = self.changePlaces(x,y,i[0][0],i[0][1])
            if child is not None:
                child_node = Node(child,self.level+1,0,self,i[1])
                children.append(child_node)
        return children
        
    def changePlaces(self,x1,y1,x2,y2):
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data):
            temp_puz = []
            temp_puz = self.copy(self.data)
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
        self.start = None
        self.goal = None
        self.min = []
        self.manhattan_cell_dict = dict()

    def toTuple(self,l):
        return tuple(tuple(x) for x in l)

    def set_start(self):
        puz = []
        for _ in range(0,self.n):
            temp = input().split(",")
            puz.append(temp)
        self.start = self.toTuple(puz)
    
    def set_goal(self):
        puz = []
        for _ in range(0,self.n):
            temp = input().split(",")
            puz.append(temp)
        self.goal = self.toTuple(puz)

    #Precalculation of all manhattan distances, provided by Antonio Diaz Flores
    def precalc_manhattan_distance(self):
        size = len(self.goal)
        for row in range(size):
            for column in range(size):
                for row_goal in range(size):
                    for column_goal in range(size):
                        self.manhattan_cell_dict[(self.goal[row_goal][column_goal], row, column)] = abs(row - row_goal) + abs(column - column_goal)

    def f(self,node):
        h = self.h(node.data)
        return h-self.g(node.level) if h != 0 else 0

    def g(self,level):
        return level*(0.001)

    def h(self,node):
        temp = 0
        size = range(0,self.n)
        for i in size:
            for j in size:
                curr = node[i][j]
                if curr != "0":
                    temp += self.manhattan_cell_dict[(curr, i, j)]
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

    def solve(self, debug): #A Estrella
        root = Node(self.start, level=0, val=0, parent=None, direction="Start") #Create start node
        root.val = self.f(root) #set value of node with f function
        self.open[root.data] = root #introduce node to open dict
        self.insertMin(root.data, root.val) #Insert as current minimum value
        interations = 1000 #set number of iterations
        while interations:
            interations-=1
            key,val = self.min.pop(0) #Pop minimum value from list of minimums
            minimum = self.open[self.toTuple(key)] #get data from open dict
            self.closed[self.toTuple(key)] = 1 #Put minimum into closed since we are visiting it        
            for node in minimum.generate_child(): #For each kid in minimum
                node.val = self.f(node) #Set the value f for the kid
                if node.val == 0: #If is None, it means it's the answer
                    return node
                if self.closed.get(self.toTuple(node.data))== None: #If not in closed (already visited)
                    key = self.toTuple(node.data) #get key for dict to search for it
                    if self.open.get(key) == None: #First time seeing it means it's not in open
                        self.open[key] = node #Set node in open
                        self.insertMin(node.data, node.val) #Insert int minimums list
                    else: #If it was found in open
                        if node.compare(self.open[key]) == 0: #If better, replace, else, do nothing
                            self.open[key] = node
                            self.updateMin(node.data, node.val)

    def process(self, debug):
        self.precalc_manhattan_distance() #Get all of the manhattan distances
        current = self.solve(debug)
        s = ""
        nodes = []
        if current == None:
            print("No solution found in 10000 nodes")
            return nodes
        while current.prevDir != "Start":
            nodes.insert(0,current)
            s = current.prevDir+","+s
            current=current.parent
        print(s[0:-1])
        return nodes

def main():
    n = int(input())
    puz = Puzzle(n)
    puz.set_start()
    puz.set_goal()
    puz.process(0)

if __name__ == "__main__":
    initial = time()
    main()
    final = time()
    print(f"ETA: {final-initial}")