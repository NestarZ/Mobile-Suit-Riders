import random
from main import ORIENTATIONS

def generate_grid(N,M,O):
    assert 0 < N <= 50
    assert 0 < M <= 50
    obs_indexes = random.sample(range(N*M), O)
    gl = [1 if k in obs_indexes else 0 for k in range(N*M)]
    return [gl[M*i:M*(i+1)] for i in range(N)]

def generate_robot(grid):
    N, M = len(grid), len(grid[0])
    lpos = set([(x,y) for x in range(N) for y in range(M) for i in (x,max(0,x-1)) for j in (y,max(0,y-1)) if grid[i][j] == 1])
    z = list(set((i,j) for i in range(N) for j in range(M)) - lpos)
    pos, goal = random.sample(z, 2)
    orientation = random.sample(list(ORIENTATIONS.values()), 1)[0]
    return pos, goal, orientation

def generate_instances(N,M,O):
    assert 0 < N <= 50
    assert 0 < M <= 50

    g = generate_grid(N,M,O)
    grid_info = "{} {}".format(N, M)
    grid_str = '\n'.join([' '.join(map(str, _)) for _ in g])

    pos, goal, orientation = generate_robot(g)
    ori_str = [k for k,v in ORIENTATIONS.items() if v == orientation][0]
    robot_info = ' '.join(map(str, pos + goal)) + ' ' + ori_str

    return "{}\n{}\n{}\n".format(grid_info, grid_str, robot_info)

def write_instances(r, fname):
    with open('../data/instances/{}.dat'.format(fname), 'w') as f:
        f.write(r + "0 0")

if __name__ == "__main__":
    r = ""
    for _ in range(20):
        r += generate_instances(20,20,30)
        write_instances(r, 'inputs')
