import networkx as nx
from matplotlib import pyplot as plt
import pylab

plt.xkcd()

# Load the graph
collab_graph = nx.Graph()

centralities = {'Betweenness_Centrality': 0, 'Closeness_Centrality': 0, 'Communicability_Centrality': 0,
                'Degree_Centrality': 0, 'Katz_Centrality': 0, 'Weighted_Degree_Centrality': 0}

productivities = {'author_productivity.txt': 0, 'author_citation_sums': 0, 'author_citation_max': 0}

for centrality in centralities.keys():
    with open("Centralities/"+centrality) as f:
        lines = f.read().split('\n')
        lines = filter(lambda line: len(line) > 0 and line[0] != '#', lines)
        values = {int(line.split(' ')[0]): float(line.split(' ')[1]) for line in lines}
        centralities[centrality] = values

print
print "Top 10 most central nodes in each metric"
print "****************************************"
for centrality, values in centralities.items():
    print centrality
    print sorted(values, key=values.get, reverse=True)[:20]
print


for productivity in productivities.keys():
    with open(productivity) as f:
        lines = f.read().split('\n')
        lines = filter(lambda line: len(line) > 0 and line[0] != '#', lines)
        values = {int(line.split('\t')[0]): float(line.split('\t')[1]) for line in lines}
        productivities[productivity] = values


print
print "Top 10 most productive nodes in each metric"
print "****************************************"
for productivity, values in productivities.items():
    print productivity
    print sorted(values, key=values.get, reverse=True)[:20]
print


for centrality, c_values in centralities.items():
    for productivity, p_values in productivities.items():
        points = [(j, p_values[i]) for (i,j) in c_values.items()]
        plt.scatter(map(lambda x: x[0], points), map(lambda x: x[1], points))
        plt.suptitle(centrality+' '+productivity, fontsize=14, fontweight='bold')
        plt.show()
