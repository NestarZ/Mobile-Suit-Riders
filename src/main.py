ORIENTATIONS = {
    'nord': (1, 0),
    'est': (0, 1),
    'sud': (-1, 0),
    'ouest': (0, -1),
    }

class Robot:
    pass

class Graph(dict):
    """ Data structure for graph inherited from dictionaries """

    def __init__(self, *arg, **kw):
        super(Graph, self).__init__(*arg, **kw)

    @property
    def nodes(self):
        return self.keys()

    def has_node(self, node):
        """ Check if node already exist in graph """
        return node in self.nodes

    def add_node(self, node):
        """ Add new node in graph """
        assert not self.has_node(node), "Node {} already exist".format(node)
        self.update({node: set()})

    def add_arc(self, node1, node2):
        """ Add arc between nodes, accept list of nodes for destination """
        if isinstance(node2, list):
            for node in node2:
                self.add_arc(node1, node)
        else:
            assert self.has_node(node1), "Node {} undefined".format(node1)
            assert self.has_node(node2), "Node {} undefined".format(node2)
            self[node1].add(node2)

    def bfs_paths(self, start, goal):
        """ Find shortest path between two nodes, if exists """
        queue = [(start, [start])]
        while queue:
            (vertex, path) = queue.pop(0)
            for next in self[vertex] - set(path):
                if next[:2] == goal:
                    return path + [next]
                else:
                    queue.append((next, path + [next]))

def isNearObstacle(x, y, grid):
    """ Detect if an obstacle is near the cross-road """
    return any(grid[i][j]=='1' for i in (x,max(0,x-1)) for j in (y,max(0,y-1)))

def neighbors(node, grid):
    """ List all neighbors nodes according to rules """

    N, M = len(grid), len(grid[0])
    x, y, ori = node

    neighblist = [(x, y, ((ori[0]+1) % n, (ori[1]+1) % n)) for n in (-2,2)]

    for n in range(1, 4):
        x2, y2 = x+ori[0]*n, y+ori[1]*n
        if 0 <= x2 < N and 0 <= y2 < M and not isNearObstacle(x2, y2, grid):
            neighblist.append((x2, y2, ori))
        else:
            break

    return neighblist


def generateGraph(grid):
    """ From grid create a graph with nodes and arcs (with respect of rules) """

    N, M = len(grid), len(grid[0])

    graph = Graph()

    # Create node for each cross-road and for each orientation
    for x in range(N):
        for y in range(M):
            for o in ORIENTATIONS.values():
                graph.add_node((x, y, o))

    # Create arc between all nodes knowing grid and robot workspace rules
    for node in graph.nodes:
        if grid[node[0]][node[1]] == '0':
            nodes = neighbors(node, grid)
            graph.add_arc(node, nodes)

    return graph


def getInstance(data, index):
    """ Get each instance from data by recursive calls (while moving index) """

    N, M = map(int, data[index])
    assert N <= 50 and M <= 50, "Broken rule (N<=50 and M<=50)"

    if (N, M) == (0, 0):
        return []

    grid = data[index + 1:index + M]
    graph = generateGraph(grid)

    x1, y1, x2, y2 = map(int, data[index + M][:4])
    robot_ori = data[index + M][4]

    return [[graph, (x1, y1, ORIENTATIONS[robot_ori]), (x2, y2)]
            ] + getInstance(data, index + N + 2)


def importData(fname):
    """ Import data and return a list of all instances in """

    with open(fname, 'r') as f:
        data = [_.split() for _ in f.read().split('\n')]
        return getInstance(data, 0)


def format_path(path):
    """ Format a path for output read """

    cmd = lambda x, y: "a{}".format(abs(x[:2][0] - y[:2][0]) + abs(x[:2][1] - y[:2][1])) if x[
        :2] != y[:2] else "D" if (x[2][0], x[2][1]) == ((y[2][0] + 1) % 2, (y[2][1] + 1) % 2) else "G"
    return "{} {}".format(len(path) - 1, ' '.join(
        [cmd(path[i], path[i + 1]) for i in range(len(path) - 1)]))

r = importData('../data/instances/inputs.dat')

graph1, start, end = r[0]
p = graph1.bfs_paths(start, end)

print(format_path(p))
