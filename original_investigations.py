import networkx as nx
from matplotlib import pyplot
import random

ROOT_DIR = '/afs/inf.ed.ac.uk/user/s13/s1337523/Documents/STN/Project/Datasets/'
DATASET_DIRS = [
    'CA-HepTh/CA-HepTh.txt',
    'HepTh/Cit-HepTh.txt',
    'HepPh/Cit-HepPh.txt',
    'CA-AstroPh.txt',
    'CA-CondMat.txt',
    'CA-GrQc.txt',
    'CA-HepPh.txt'
]

graphs = {dataset: nx.Graph() for dataset in DATASET_DIRS}

for dataset, graph in graphs.items():
    with open(ROOT_DIR+dataset) as f:
        details = file.read(f).split('\n')
        for line in details:
            if len(line)>0 and line[0]!='#':
                nodes = line.split(' ')
                graph.add_edge(int(nodes[0]), int(nodes[1]))


for dataset, graph in graphs.items():
    print dataset
    print( sorted(map(len,list(nx.connected_components(graph))),reverse=True))
    print
    #components = sorted(nx.connected_components(g), key=len)
thisone =max(nx.connected_components(graphs['CA-HepTh/CA-HepTh.txt']), key=len)
print(type(thisone))
#print(thisone)
nx.draw(thisone)
#self_loops = [38614, 66349, 55119, 29509, 29715, 47770, 33543, 47490, 67605, 13577, 29595, 46139, 29437, 3498, 24603, 67118, 25287, 50300, 374, 16619, 49, 36148, 4318, 2125, 2125, 2689, 16623, 243, 24772, 32415]
#self_loops_not_in_main_component = [3498, 49, 16623, 24772, 32415]
#print len(self_loops)
#print len(self_loops_not_in_main_component)
#networkx.draw(g, cmap = pyplot.get_cmap('jet'))
#pyplot.show()
