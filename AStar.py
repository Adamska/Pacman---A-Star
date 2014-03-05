class Path:
    def __init__(self, nodes, totalCost):
        self.nodes = nodes;
        self.totalCost = totalCost;

    def getNodes(self): 
        return self.nodes    

    def getTotalMoveCost(self):
        return self.totalCost

class Node:
    def __init__(self, location, mCost, lid, parent=None):
        self.location = location # where is this node located
        self.mCost = mCost # total move cost to reach this node
        self.parent = parent # parent node
        self.score = 0 # calculated score for this node
        self.lid = lid # set the location id - unique for each location in the maphandler

    #Compare id of two nodes    
    def __eq__(self, n):
        if n.lid == self.lid:
            return 1
        else:
            return 0

class AStar:
    def __init__(self, maphandler):
        self.mh = maphandler
    
    #Return the node with the lower score
    def _getBestOpenNode(self):
        bestNode = None        
        for n in self.on:
            if not bestNode:
                bestNode = n
            else:
                if n.score <= bestNode.score:
                    bestNode = n
        return bestNode

    #Return the path made with each node of the path found
    def _tracePath(self, n):
        nodes = [];
        totalCost = n.mCost;
        p = n.parent;
        nodes.insert(0, n);       
        
        while 1:
            if p.parent is None: 
                break

            nodes.insert(0, p)
            p = p.parent
        
        return Path(nodes, totalCost)

    #Choose and place the nodes on closed and opened list
    def _handleNode(self, node, end):        
        i = self.o.index(node.lid)
        self.on.pop(i)
        self.o.pop(i)
        self.c.append(node.lid)

        nodes = self.mh.getAdjacentNodes(node, end)
                   
        for n in nodes:
            if n.location == end:
                # reached the destination
                return n
            elif n.lid in self.c:
                # already in close, skip this
                continue
            elif n.lid in self.o:
                # already in open, check if better score
                i = self.o.index(n.lid)
                on = self.on[i];
                if n.mCost < on.mCost:
                    self.on.pop(i);
                    self.o.pop(i);
                    self.on.append(n);
                    self.o.append(n.lid);
            else:
                # new node, append to open list
                self.on.append(n);                
                self.o.append(n.lid);

        return None

    #Create the closed and opened list, calculate the path and return it, if it exists
    def findPath(self, fromlocation, tolocation):
        self.o = []
        self.on = []
        self.c = []

        end = tolocation
        fnode = self.mh.getNode(fromlocation)
        self.on.append(fnode)
        self.o.append(fnode.lid)
        nextNode = fnode 
               
        while nextNode is not None: 
            finish = self._handleNode(nextNode, end)
            if finish:                
                return self._tracePath(finish)
            nextNode = self._getBestOpenNode()
                
        return None
      
#class which represent a 2D coordinate
class SQ_Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, l):
        if l.x == self.x and l.y == self.y:
            return 1
        else:
            return 0

#class which represent a map in one dimension
class SQ_MapHandler:

    def __init__(self, mapdata, width, height):
        self.m = mapdata
        self.w = width
        self.h = height

    #Return a new node speficied by the location on the map
    def getNode(self, location):
        x = location.x
        y = location.y
        if x < 0 or x >= self.w or y < 0 or y >= self.h:
            return None
        
        d = int(self.m[(y * self.w) + x]) 
        if d == 1 or d == 2 or d == 3:
            return None 
        return Node(location, d + 1, ((y * self.w) + x));                

    #See in the neigbourhood of the node and continue to build the path
    def getAdjacentNodes(self, curnode, dest):
        result = []
       
        cl = curnode.location
        dl = dest
        
        n = self._handleNode(cl.x + 1, cl.y, curnode, dl.x, dl.y)
        if n: result.append(n)
        n = self._handleNode(cl.x - 1, cl.y, curnode, dl.x, dl.y)
        if n: result.append(n)
        n = self._handleNode(cl.x, cl.y + 1, curnode, dl.x, dl.y)
        if n: result.append(n)
        n = self._handleNode(cl.x, cl.y - 1, curnode, dl.x, dl.y)
        if n: result.append(n)
                
        return result

    #Calculate the cost of the move and affect a parent
    def _handleNode(self, x, y, fromnode, destx, desty):
        n = self.getNode(SQ_Location(x, y))
        if n is not None:
            dx = max(x, destx) - min(x, destx)
            dy = max(y, desty) - min(y, desty)
            emCost = dx + dy
            n.mCost += fromnode.mCost                                   
            n.score = n.mCost + emCost
            n.parent = fromnode
            return n

        return None    
