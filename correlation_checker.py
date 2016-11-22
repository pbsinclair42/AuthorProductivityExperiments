import networkx as nx
from matplotlib import pyplot as plt
import pylab
from scipy import stats
from prettytable import PrettyTable

plt.xkcd()


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

pearsons = {}

for centrality, c_values in centralities.items():
    for productivity, p_values in productivities.items():
        points = [(j, p_values[i]) for (i,j) in c_values.items()]

        fig = plt.figure()
        plt.suptitle(centrality+' '+productivity, fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        fig.subplots_adjust(top=0.85)
        ax.set_xlabel('Centrality')
        ax.set_ylabel('Productivity')

        pearson_coefficient = stats.pearsonr(map(lambda x: x[0], points), map(lambda x: x[1], points))
        pearsons[(centrality, productivity)] = pearson_coefficient
        ax.set_title("Pearson Coefficient: "+str(pearson_coefficient[0])+'\nProbability: '+str(pearson_coefficient[1]),
            fontdict = {'fontsize': 12})

        plt.scatter(map(lambda x: x[0], points), map(lambda x: x[1], points))

        #plt.show()

        #pylab.savefig('graphs/'+centrality+'-'+productivity+'.png')
        pylab.clf()

table = PrettyTable()
table.field_names = ["Centrality Metric", "Productivity Metric", "Pearson Correlation Coefficient", "Probability"]
for ((centrality, productivity), (pearson, probability)) in sorted(pearsons.items(), key=lambda x:x[1], reverse=True):
    table.add_row([centrality, productivity, pearson, probability])

with open('correlations.txt', 'w') as f:
    f.writelines(table.get_string())
print(table)
