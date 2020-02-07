from cluster_utils import Cluster


cl = Cluster()

l = []

for d in cl.devices:
    l.append(d.performance)
print(l)
print(cl.divide_alg(90))