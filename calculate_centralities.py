import networkx as nx


# nx only provides a non-weighted degree centrality function
def weighted_degree_centrality(graph):
    total_weight = graph.size(weight='weight')
    results = {}
    for node in graph:
        degree = sum([edge[1]['weight'] for edge in graph[node].items()])
        degree /= total_weight
        results[node] = degree
    return results

# print to file
def output_centralities(centralities, centrality_type):
    with open('Centralities/'+centrality_type, 'w') as f:
        f.write('# Node '+centrality_type+'\n\n')
        f.writelines([str(node)+' '+str(centrality)+'\n' for (node, centrality) in centralities.items()])

def distance_from_erdos(graph, erdos):
    results = {}
    for node in graph:
        try:
            distance = nx.shortest_path_length(graph, source=node, target=erdos)
        except nx.NetworkXNoPath:
            distance = None
        results[node] = distance
    return results

# Load the graph
collab_graph = nx.Graph()
with open("productivity_data/raw_productivity") as f:
    details = f.read().split('\n')
    for line in details:
        if len(line) > 0 and line[0] != '#':
            node = line.split('\t')[0]
            productivity = line.split('\t')[1]
            collab_graph.add_node(int(node), productivity=int(productivity))

with open("collab_graph_weighted.txt") as f:
    details = f.read().split('\n')
    for line in details:
        if len(line) > 0 and line[0] != '#':
            node0 = line.split(' ')[0]
            node1 = line.split(' ')[1].split('\t')[0]
            weight = line.split('\t')[1]
            collab_graph.add_edge(int(node0), int(node1), weight=int(weight))

distances = distance_from_erdos(collab_graph, 1095)
output_centralities(distances, 'Distance_From_Erdos')
exit()

# Calculate and output the centralities
degree_centrality = nx.degree_centrality(collab_graph)
output_centralities(degree_centrality, 'Degree_Centrality')

degree_centrality_weighted = weighted_degree_centrality(collab_graph)
output_centralities(degree_centrality_weighted, 'Weighted_Degree_Centrality')

normalised_closeness_centrality = nx.closeness_centrality(collab_graph)
output_centralities(normalised_closeness_centrality, "Closeness_Centrality")

betweenness_centrality = nx.betweenness_centrality(collab_graph, endpoints=True)
output_centralities(betweenness_centrality, "Betweenness_Centrality")

katz_centrality = nx.katz_centrality(collab_graph, alpha=0.005)
output_centralities(katz_centrality, "Katz_Centrality")

communicability_centrality = nx.communicability_centrality(collab_graph)
output_centralities(communicability_centrality, "Communicability_Centrality")
