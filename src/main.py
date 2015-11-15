N, E, S, W = (1,0), (0,1), (-1,0), (0,-1)
orientations = {'nord': N, 'est': E, 'sud': S, 'ouest': W}

class Robot:
    pass

class Graph(dict):
    """ Data structure for graph inherited from dictionaries """

    def __init__(self,*arg,**kw):
        super(Graph, self).__init__(*arg, **kw)

    def has_node(self, node):
        """ Check if node already exist in graph """
        #assert isinstance(node, str), "Node must be string, not {}".format(type(node))
        return node in self.keys()

    def add_node(self, node):
        """ Add new node in graph """
        assert not self.has_node(node), "Node {} already exist".format(node)
        self.update({node : list()})

    def add_arc(self, node1, node2):
        """ Add arc between nodes, accept list of nodes for destination """
        if isinstance(node2, list):
            for node in node2:
                self.add_arc(node1, node)
        else:
            assert self.has_node(node1), "Node {} undefined".format(node1)
            assert self.has_node(node2), "Node {} undefined".format(node2)
            self[node1].append(node2)

    def find_path(self, start, end, path=[]):
        """ Find path between two nodes, if exists """
        path = path + [start]
        if start[:2] == end:
            return path
        if not self.has_node(start):
            return None
        for node in self[start]:
            if node not in path:
                newpath = self.find_path(node, end, path)
                if newpath: return newpath
        return None

def neighbors(x, y, o, grid):
    max_x, max_y = len(grid), len(grid[0])
    n1 = [(x, y, o2) for o2 in (N,S,W,E) if (o != o2 and (grid[x][y] == '0'))]
    return n1 + [(x+o[0]*n,y+o[1]*n,o) for n in range(1,4) if (
         (0 <= x+o[0]*n < max_x) and
         (0 <= y+o[1]*n < max_y) and
         (grid[x+o[0]*n][y+o[1]*n] == '0'))]

def generateGraph(grid):
    graph = Graph()
    [graph.add_node((x,y,o)) for x in range(len(grid)) for y in range(len(grid[0])) for o in (N,E,S,W)]
    [graph.add_arc((x,y,o), neighbors(x,y,o,grid)) if grid[x][y] == '0' else 0 for x in range(len(grid)) for y in range(len(grid[0])) for o in (N,E,S,W)]
    return graph

def getInstance(data, index):
    N, M = map(int, data[index])
    assert N <= 50 and M <= 50, "Broken rule (N<=50 and M<=50)"

    if (N, M) == (0, 0): return []

    grid = data[index+1:index+M]
    graph = generateGraph(grid)

    x1, y1, x2, y2 = map(int,data[index+M][:4])
    robot_ori = data[index+M][4]

    return [[graph, (x1, y1, orientations[robot_ori]), (x2, y2), robot_ori]] + getInstance(data, index+N+2)

def importData(fname):
    with open(fname, 'r') as f:
        data = [_.split() for _ in f.read().split('\n')]
        r = getInstance(data, 0)
    return r

r = importData('../data/instances/inputs.dat')

graph1, start, end, ori = r[0]
print(graph1.find_path(start, end))
