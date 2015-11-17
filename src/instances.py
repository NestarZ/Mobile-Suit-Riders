import random
from main import ORIENTATIONS

def genInstances(N,M,O):
    assert 0 < N <= 50
    assert 0 < M <= 50

    grid_info = "{} {}".format(N, M)

    obs_indexes = random.sample(range(N*M), O)
    gl = ['1' if k in obs_indexes else '0' for k in range(N*M)]
    g = [gl[M*i:M*(i+1)] for i in range(N)]
    grid = '\n'.join([' '.join(_) for _ in g])

    lpos = set([(x,y) for x in range(N) for y in range(M) for i in (x,max(0,x-1)) for j in (y,max(0,y-1)) if g[i][j] == '1'])
    z = list(set((i,j) for i in range(N) for j in range(M)) - lpos)
    robot_pos, goal = random.sample(z, 2)
    robot_ori = random.sample(ORIENTATIONS.keys(), 1)
    robot_info = ' '.join(map(str, robot_pos + goal)) + ' ' + robot_ori[0]

    return "{}\n{}\n{}\n".format(grid_info, grid, robot_info)

def writeInstances(r, fname):
    with open('../data/instances/{}.dat'.format(fname), 'w') as f:
        f.write(r + "0 0")

if __name__ == "__main__":
    r = ""
    for _ in range(10):
        r += genInstances(10,10,10)
        writeInstances(r, 'inputs')
