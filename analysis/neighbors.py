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

    # no features
    labels = numpy.vstack(list(raceLabelGen(dbf)))
 
    features = numpy.ones((len(labels), 1), dtype='float')
    edgelist = edgeList(shapes)

    return (features, edgelist), labels


def raceLabelGen(dbf) :
    white_index = dbf.header.index('P0050003')
    black_index = dbf.header.index('P0050004')
    hispanic_index = dbf.header.index('P0040003')
    for row in dbf :
        races = (int(row[hispanic_index]), int(row[black_index]), int(row[white_index]))
        races = numpy.array(races)
        
        if sum(races) == 0:
            import pdb
            pdb.set_trace()
        yield races
        #yield numpy.argmax(races)

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
        features = city_indicator.copy()
        features[i] = 0
        features = numpy.tile(features, (n_nodes, 1))
        X.append((features, edgelist))
        Y.append(y)

    return X, Y




if __name__ == '__main__' :
    import itertools
    import os

    from pysal.contrib.viz import mapping

    data_path = '../data/'
    iterations = 1000

    base_names = [name.split('_county_race')[0] 
                  for name in os.listdir(data_path) 
                  if name.endswith('_race.shp')]

    sample_size = len(base_names)

    #base_name = base_names[3]
    base_name = 'chicago_pop'

    X, Y = trainingData([base_name], data_path)
    n_observations = Y[0].sum(axis=1)[:, numpy.newaxis]

    features, edges = X[0]
    A = to_adjacency(edges)

    potts = CenteredPotts(C=float('inf'))

    potts.fit((features, A), Y[0])
    print(potts.coef_)
    print(potts.intercept_)

    print(Y[0])
    print(Y[0].sum(axis=0))
    sample = rmultinomial((features, A), n_observations, potts)
    print(sample)
    print(sample.sum(axis=0))


    city_shp = '../data/chicago_pop.shp'
    mapping.plot_choropleth(city_shp, Y[0].argmax(axis=1), 'unique_values')
    mapping.plot_choropleth(city_shp, sample.argmax(axis=1), 'unique_values')
    
