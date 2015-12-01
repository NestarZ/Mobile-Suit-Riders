import matplotlib.pyplot as plt
import instances, main
import time, timeit

def mainf(iters,Nmax=None,Mmax=None,Omax=None):
    exectime = []
    tailles = range(10,60,10)

    for K in tailles:
        endmoy = 0
        N = Nmax if Nmax is not None else K
        M = Mmax if Mmax is not None else K
        O = Omax if Omax is not None else K
        for i in range(iters):
            g = instances.generate_grid(N,M,O)
            p, goal, o = instances.generate_robot(g)
            #START COUNTING
            t = time.time()
            g = main.generateGraph(g)
            g.bfs_path((p,o), goal)
            #END
            end = time.time() - t
            endmoy += end
        exectime.append(endmoy/iters)
        print((N,M), O, endmoy/iters)

    if isinstance(Nmax, int) and Omax is None:
        l = "N=M={}, O".format(Nmax)
    elif Nmax is None and isinstance(Omax, int):
        l = "N=M, O={}".format(Omax)
    else:
        l = "N=M=O"

    fig = plt.figure()
    ax = plt.subplot(111)
    ax.plot([i for i in tailles], exectime, label=l)
    ax.legend()
    plt.ylabel('Overall time (graph conversion + bfs resolution)')
    plt.xlabel('Obstacles amount')

if __name__ == "__main__":
    iters = 200
    # N=M=20, itération sur O
    mainf(iters, 20, 20, None)
    # O=0, itération sur N (N=M)
    #mainf(iters, None, None, 0)
    # itération sur N (N=M=O)
    #mainf(iters, None, None, None)

    plt.show()
