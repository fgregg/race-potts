import pysal
from pysal.weights.Contiguity import buildContiguity
from pseudolikelihood.centered_potts import CenteredPotts, rpotts, to_adjacency
from pseudolikelihood.mcmc import rmultinomial
import numpy
import datetime
import time

def example(base_name, data_path) :
    shapes = pysal.open(data_path + base_name + '.shp','r')
    dbf = pysal.open(data_path + base_name + '.dbf', 'r')

    labels = numpy.vstack(list(raceLabelGen(dbf)))
 
    features = numpy.zeros((labels.shape[0], 1), dtype='float')
    edgelist = edgeList(shapes)

    return (features, edgelist), labels

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

def raceLabelGen(dbf) :
    white_index = dbf.header.index('B03002_003')
    black_index = dbf.header.index('B03002_004')
    hispanic_index = dbf.header.index('B03002_012')
    for row in dbf :
        races = (int(row[white_index]), int(row[hispanic_index]), int(row[black_index]))
        races = numpy.array(races)
        if sum(races) == 0:
            import pdb
            pdb.set_trace()
        
        yield races


if __name__ == '__main__' :
    import itertools
    import os

    from pysal.contrib.viz import mapping

    data_path = './'

    places = ['chicago']

    X, Y = trainingData(places, data_path)
    for place, x, y in zip(places, X, Y):
        features, edges = x
        A = to_adjacency(edges)
        n_observations = y.sum(axis=1)[:, numpy.newaxis]

        potts = CenteredPotts(C=float('inf'))

        potts.fit((features, A), y)

        print(numpy.hstack((potts.intercept_.reshape(-1, 1),
                            potts.coef_)))

        print(y)
        print(y.sum(axis=0))
        print(y.shape[0])
        n_observations[:] = 1
        sample = rmultinomial((features, A), n_observations, potts)
        print(sample)
        print(sample.sum(axis=0))

        city_shp = data_path + '{}.shp'.format(place)
        mapping.plot_choropleth(city_shp, y.argmax(axis=1), 'unique_values')
        mapping.plot_choropleth(city_shp, sample.argmax(axis=1), 'unique_values')
    
