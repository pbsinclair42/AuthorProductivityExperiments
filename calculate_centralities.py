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


def output_centralities(centralities, centrality_type):
    with open('Centralities/'+centrality_type, 'w') as f:
        f.write('# Node '+centrality_type+'\n\n')
        f.writelines([str(node)+' '+str(centrality)+'\n' for (node, centrality) in centralities.items()])


# Load the graph
collab_graph = nx.Graph()
with open("collab_graph_weighted.txt") as f:
    details = f.read().split('\n')
    for line in details:
        if len(line) > 0 and line[0] != '#':
            node0 = line.split(' ')[0]
            node1 = line.split(' ')[1].split('\t')[0]
            weight = line.split('\t')[1]
            collab_graph.add_edge(int(node0), int(node1), weight=int(weight))

# Calculate and output the centralities
degree_centrality = nx.degree_centrality(collab_graph)
output_centralities(degree_centrality, 'Degree_Centrality')

degree_centrality_weighted = weighted_degree_centrality(collab_graph)
output_centralities(degree_centrality_weighted, 'Weighted_Degree_Centrality')

normalised_closeness_centrality = nx.closeness_centrality(collab_graph)
output_centralities(normalised_closeness_centrality, "Closeness_Centrality_Normalised")
unnormalised_closeness_centrality = nx.closeness_centrality(collab_graph, normalized=False)
output_centralities(unnormalised_closeness_centrality, "Closeness_Centrality_Unnormalised")

max_connected_component = max(nx.connected_component_subgraphs(collab_graph), key=len)
unnormalised_closeness_centrality = nx.closeness_centrality(collab_graph)
output_centralities(unnormalised_closeness_centrality, "Closeness_Centrality_Of_Largest_Connected_Component_Only")
