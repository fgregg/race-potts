import pysal
from pysal.weights.Contiguity import buildContiguity
from pseudolikelihood.centered_potts import CenteredPotts, rpotts, to_adjacency
from pseudolikelihood.mcmc import rmultinomial
import numpy

def example(base_name, data_path) :
    shapes = pysal.open(data_path + base_name + '.shp','r')
    dbf = pysal.open(data_path + base_name + '.dbf', 'r')

    labels = numpy.vstack(list(raceLabelGen(dbf)))

    features = numpy.vstack(list(node_features(dbf)))
    features -= features.mean(axis=0)

    edgelist = edgeList(shapes)

    return (features, edgelist), labels

def raceLabelGen(dbf) :
    white_index = dbf.header.index('p0050003')
    black_index = dbf.header.index('p0050004')
    hispanic_index = dbf.header.index('p0040003')
    for row in dbf :
        races = (row[black_index], row[hispanic_index], row[white_index])
        races = numpy.array(races)
        
        yield races

def edgeList(shapes) :
    w = buildContiguity(shapes)

    edgelist = set([])

    for target, neighbors in w :
        for neighb in neighbors :
            if neighb > target :
                edgelist.add((target, neighb))

    return numpy.array(sorted(edgelist))

def trainingData(base_names, data_path) :
    X = []
    Y = []

    city_indicator = numpy.zeros(len(base_names))

    for i, name in enumerate(base_names) :
        x, y = example(name, data_path)
        features, edgelist = x
        n_nodes = features.shape[0]
        X.append((features, edgelist))
        Y.append(y)

    return X, Y


def node_features(dbf):
    median_monthly_gross_rent = dbf.header.index('b25064_001')
    for row in dbf:
        rent = row[median_monthly_gross_rent]
        if rent == 0:
            import pdb
            pdb.set_trace()
        yield numpy.array([numpy.log(rent)], ndmin=2)


if __name__ == '__main__' :
    import itertools
    import os
    import csv
    import sys

    writer = csv.writer(sys.stdout)
    
    data_path = '../data/'
    file_names = [name.split('.shp')[0] for name in os.listdir(data_path) 
                 if name.endswith('_blocks.shp')]

    X, Y = trainingData(file_names, data_path)
    for file_name, x, y in zip(file_names, X, Y):
        place = file_name.rsplit('_', 1)[0]
        
        features, edges = x
        A = to_adjacency(edges, features.shape[0])
        average_N_neighbors = A.sum(axis=1).mean()
        n_sites = features.shape[0]

        for use_features in (True, False):

            if use_features:
                model_features = features
            else:
                model_features = numpy.zeros_like(features)

            potts = CenteredPotts(C=float('inf'), average_spatial=False)

            potts.fit((model_features, A), y)

            raveled_params = numpy.hstack((potts.intercept_.reshape(-1, 1),
                                       potts.coef_)).ravel()
            writer.writerow([place, n_sites] + list(raveled_params))


