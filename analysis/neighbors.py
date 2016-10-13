import pysal
from pysal.weights.Contiguity import buildContiguity
from pseudolikelihood.centered_potts import CenteredPotts, rpotts, to_adjacency
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
        races = (row[white_index], row[black_index], row[hispanic_index])
        races = numpy.array([int(race) for race in races])
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
    base_name = 'chicago'

    X, Y = trainingData([base_name], data_path)
    features, edges = X[0]
    A = to_adjacency(edges)

    potts = CenteredPotts(C=1)
    print(A.sum(axis=1).mean())

    potts.fit((features, A), Y[0])
    print(potts.coef_)
    print(potts.intercept_)

    print('len', len(Y[0]))
    print('0', (Y[0]==0).sum())
    print('1', (Y[0]==1).sum())
    print('2', (Y[0]==2).sum())
    print(Y[0])
    sample = rpotts((features, A), potts)
    print(sample.T)
    print((sample==0).sum())
    print((sample==1).sum())
    print((sample==2).sum())


    city_shp = '../data/chicago.shp'
    mapping.plot_choropleth(city_shp, Y[0], 'unique_values')
    mapping.plot_choropleth(city_shp, sample.T[0], 'unique_values')
    
