ORIENTATIONS = {
    'nord': (-1, 0),
    'est': (0, 1),
    'sud': (1, 0),
    'ouest': (0, -1),
    }

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

    def bfs_path(self, start, goal):
        """ Find shortest path between two nodes, if exists """
        queue = [(start, [start])]
        visited = set([start])
        while queue:
            (vertex, path) = queue.pop(0)
            if vertex[0] == goal: # orientation doesnt matter
                return path
            for nextv in self[vertex]-visited:
                visited.add(nextv)
                queue.append((nextv, path + [nextv]))
        return []


def isNearObstacle(x, y, grid):
    """ Detect if an obstacle is near the cross-road """
    return any(grid[i][j] in ('1', 1) for i in (x,max(0,x-1)) for j in (y,max(0,y-1)))

def neighbors(node, grid):
    """ List all neighbors nodes according to rules """

    N, M = len(grid), len(grid[0])
    (x, y), ori = node

    neighblist = [((x, y), ((ori[0]+1) % n, (ori[1]+1) % n)) for n in (-2,2)]

    for n in range(1, 4):
        x2, y2 = x+ori[0]*n, y+ori[1]*n
        if 0 <= x2 < N and 0 <= y2 < M and not isNearObstacle(x2, y2, grid):
            neighblist.append(((x2, y2), ori))
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
                graph.add_node(((x, y), o))

    # Create arc between all nodes knowing grid and robot workspace rules
    for node in graph.nodes:
        if grid[node[0][0]][node[0][1]] in ('0', 0):
            nodes = neighbors(node, grid)
            graph.add_arc(node, nodes)
    return graph


def getInstance(data, index):
    """ Get each instance from data by recursive calls (while moving index) """

    N, M = map(int, data[index])
    #assert 0 < N <= MAX_N
    #assert 0 < M <= MAX_M

    if (N, M) == (0, 0):
        return []

    grid = data[index + 1:index + N + 1]
    graph = generateGraph(grid)

    x1, y1, x2, y2 = map(int, data[index + N + 1][:4])
    robot_ori = data[index + N + 1][4]
    return [[graph, ((x1, y1), ORIENTATIONS[robot_ori]), (x2, y2)]
            ] + getInstance(data, index + N + 2)


def importData(fname):
    """ Import data and return a list of all instances in """

    with open(fname, 'r') as f:
        data = [_.split() for _ in f.read().split('\n')]
        return getInstance(data, 0)


def format_path(path):
    """ Format a path for output read """

    cmd = lambda x, y: "a{}".format(abs(x[0][0] - y[0][0]) + abs(x[0][1] - y[0][1])) if x[
        0] != y[0] else "D" if ((x[1][0] + 1) % 2, (x[1][1] + 1) % 2) == (y[1][0], y[1][1]) else "G"
    return "{} {}".format(len(path) - 1, ' '.join(
        [cmd(path[i], path[i + 1]) for i in range(len(path) - 1)]))

def write_result(path, fname):
    with open(fname, 'w') as f:
        f.write(path)

if __name__  == "__main__":
    import sys, time
    import matplotlib.pyplot as plt

    s = ''
    if len(sys.argv) > 1 and sys.argv[1] in ("-d", "--demo"):
        s = '_demo'

    dirc = "../data/inputs/"
    fname = "instances{}".format(s)
    if len(sys.argv) > 1:
        if len(sys.argv[1]) > 4 and sys.argv[1][-4:] == '.dat':
            fname = sys.argv[1].split('/')[-1][:-4]
        else:
            fname = sys.argv[1].split('/')[-1]

    t = time.time()
    r = importData('{}{}.dat'.format(dirc, fname))
    end = time.time() - t
    print("{} Import mean time on {} instances from {}.dat file".format(end/len(r), len(r), fname))

    X = []
    paths_str = ""
    for ins in r:
        graph, start, end = ins
        t = time.time()
        p = graph.bfs_path(start, end)
        end = time.time() - t
        X.append(end)
        paths_str += "{}\n".format(format_path(p))
    print("{} BFS mean time on {} instances from {}.dat file".format(abs(sum(X)/len(X)), len(r), fname))

    dirc = "../data/outputs/"
    write_result(paths_str, '{}{}_output.dat'.format(dirc, fname))
