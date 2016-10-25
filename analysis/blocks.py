import pysal
from pysal.weights.Contiguity import buildContiguity
from pseudolikelihood.centered_potts import CenteredPotts, rpotts, to_adjacency
from pseudolikelihood.mcmc import rmultinomial
import numpy

def example(base_name, data_path) :
    shapes = pysal.open(data_path + base_name + '.shp','r')
    dbf = pysal.open(data_path + base_name + '.dbf', 'r')

    labels = numpy.vstack(list(raceLabelGen(dbf)))
 
    features = numpy.zeros((labels.shape[0], 1), dtype='float')
    edgelist = edgeList(shapes)

    return (features, edgelist), labels

def raceLabelGen(dbf) :
    white_index = dbf.header.index('P0050003')
    black_index = dbf.header.index('P0050004')
    hispanic_index = dbf.header.index('P0040003')
    for row in dbf :
        races = (int(row[black_index]), int(row[hispanic_index]), int(row[white_index]))
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
        A = to_adjacency(edges)

        potts = CenteredPotts(C=float('inf'))

        potts.fit((features, A), y)

        raveled_params = numpy.hstack((potts.intercept_.reshape(-1, 1),
                                       potts.coef_)).ravel()
        writer.writerow([place] + list(raveled_params))

