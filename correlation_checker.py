import networkx as nx

# Load the graph
collab_graph = nx.Graph()

centralities = {'Betweenness_Centrality':0, 'Closeness_Centrality':0, 'Communicability_Centrality':0, 'Degree_Centrality':0, 'Katz_Centrality':0, 'Weighted_Degree_Centrality':0}

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
