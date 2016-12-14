# Productivity of authors from network structure.

Some scientists (like Erdos) are very productive and write many articles. Is there any relation between the productivity of authors and their position in the network?

In many types of networks, nodes that are more centrally located are seen to be more influential or important. For example, in economic networks, these are powerful entities, in the internet, these are the major ISPs controlling the internet backbones, etc. Does this pattern also hold among scientific authors? If so, what is the right measure of centrality? Or are there better non-trivial measure that predicts the productivity?

#### Datasets used:

[HEP-th dataset from KDD cup](http://www.cs.cornell.edu/projects/kddcup/datasets.html), the abstract and citation graph sets

## To run:

Download and unzip hep-th-abs from [http://www.cs.cornell.edu/projects/kddcup/datasets.html](http://www.cs.cornell.edu/projects/kddcup/datasets.html)

Run create_network.ipynb and citation_counting.ipynb to parse the dataset into the form we need.

Run Graph_Exploration.ipynb to see some interesting features of the dataset.

Run calculate_centralities.py to compute each of the Centralities of each node.

Run correlation_checker.py to output the graphs and text results of the correlations between each of the metrics.

The outputs will be put in the `results/` folder.
