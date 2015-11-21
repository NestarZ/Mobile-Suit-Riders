import time

A = dict.fromkeys((range(10000)))
B = list(range(10000))
C = set(range(10000))

t = time.time()
for i in range(10000):
    i in A
d = time.time() - t

print(d)

t = time.time()
for i in range(10000):
    i in B
d = time.time() - t

print(d)

t = time.time()
for i in range(10000):
    i in C
d = time.time() - t
print(d)
