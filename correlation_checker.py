import networkx as nx
from matplotlib import pyplot as plt
import pylab
from scipy import stats
from prettytable import PrettyTable


centralities = {'Betweenness_Centrality': 0, 'Closeness_Centrality': 0, 'Communicability_Centrality': 0,
                'Degree_Centrality': 0, 'Katz_Centrality': 0, 'Weighted_Degree_Centrality': 0}

productivities = {'raw_productivity': 0, 'author_citation_sums': 0, 'author_citation_max': 0, 'author_citation_avg': 0}

# load centralities
for centrality in centralities.keys():
    with open("Centralities/"+centrality) as f:
        lines = f.read().split('\n')
        lines = filter(lambda line: len(line) > 0 and line[0] != '#', lines)
        values = {int(line.split(' ')[0]): float(line.split(' ')[1]) for line in lines}
        centralities[centrality] = values

# load productivities
for productivity in productivities.keys():
    with open('productivity_data/'+str(productivity)) as f:
        lines = f.read().split('\n')
        lines = filter(lambda line: len(line) > 0 and line[0] != '#', lines)
        values = {int(line.split('\t')[0]): float(line.split('\t')[1]) for line in lines}
        productivities[productivity] = values

# output the top 10 nodes in each metric
with open('results/top10.txt', 'w') as f:
    f.write("Top 10 most central nodes in each metric\n")
    f.write("****************************************\n")
    for centrality, values in centralities.items():
        f.write(str(centrality)+'\n')
        f.write(str(sorted(values, key=values.get, reverse=True)[:20])+'\n\n')
    f.write('\n\n')
    f.write("Top 10 most productive nodes in each metric\n")
    f.write("****************************************\n")
    for productivity, values in productivities.items():
        f.write(str(productivity)+'\n')
        f.write(str(sorted(values, key=values.get, reverse=True)[:20])+'\n\n')

# Graph each of the centrality metrics against each of the productivity metrics
# and calculate their correlation
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

        pylab.savefig('results/graphs/'+centrality+'-'+productivity+'.png')
        pylab.clf()

# output correlations
table = PrettyTable()
table.field_names = ["Centrality Metric", "Productivity Metric", "Pearson Correlation Coefficient", "Probability"]
for ((centrality, productivity), (pearson, probability)) in sorted(pearsons.items(), key=lambda x:x[1], reverse=True):
    table.add_row([centrality, productivity, pearson, probability])
with open('results/correlations.txt', 'w') as f:
    f.writelines(table.get_string())
print(table)

# calculate correlations between centrality metrics
pearsons = {}
checked=[]
for centrality0, c_values0 in centralities.items():
    checked.append(centrality0)
    for centrality1, c_values1 in [c for c in centralities.items() if c[0] not in checked]:
        points = [(j, c_values1[i]) for (i,j) in c_values0.items()]
        pearson_coefficient = stats.pearsonr(map(lambda x: x[0], points), map(lambda x: x[1], points))
        pearsons[(centrality0, centrality1)] = pearson_coefficient

table = PrettyTable()
table.field_names = ["Metric 1", "Metric 2", "Pearson Correlation Coefficient", "Probability"]
for ((centrality, productivity), (pearson, probability)) in sorted(pearsons.items(), key=lambda x:x[1], reverse=True):
    table.add_row([centrality, productivity, pearson, probability])
table.add_row(['---']*4)

# calculate correlations between productivity metrics
pearsons = {}
checked=[]
for productivity0, p_values0 in productivities.items():
    checked.append(productivity0)
    for productivity1, p_values1 in [c for c in productivities.items() if c[0] not in checked]:
        points = [(j, p_values1[i]) for (i,j) in p_values0.items()]
        pearson_coefficient = stats.pearsonr(map(lambda x: x[0], points), map(lambda x: x[1], points))
        pearsons[(productivity0, productivity1)] = pearson_coefficient

# output correlations between the same types of metrics
for ((centrality, productivity), (pearson, probability)) in sorted(pearsons.items(), key=lambda x:x[1], reverse=True):
    table.add_row([centrality, productivity, pearson, probability])
with open('results/metric_correlations.txt', 'w') as f:
    f.writelines(table.get_string())
print(table)
