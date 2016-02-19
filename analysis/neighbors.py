import pysal
from pysal.weights.Contiguity import buildContiguity
from pystruct.models import GraphCRF
import pystruct.learners as ssvm
import numpy
import datetime
import time

def example(base_name, data_path) :
    shapes = pysal.open(data_path + base_name + '_county_race.shp','r')
    dbf = pysal.open(data_path + base_name + '_county_race.dbf', 'r')

    # no features
    labels = numpy.fromiter(raceLabelGen(dbf), 
                            dtype='int32')
    
    features = numpy.ones((len(labels), 1), dtype='float')
    edgelist = edgeList(shapes)

    return (features, edgelist), labels


def raceLabelGen(dbf) :
    for row in dbf :
        _, _, white, black, hispanic = row
        races = (white, black, hispanic)
        yield numpy.argmax(races)


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
        features[i] = 1
        features = numpy.tile(features, (n_nodes, 1))
        X.append((features, edgelist))
        Y.append(y)

    return X, Y

def train(clf, X, Y) :

    clf.fit(X, Y)

    weights = clf.w

    return weights

def extractWeights(crf, weights) :
    unary_weights = crf.n_states * crf.n_features
    unary = weights[:unary_weights]
    unary = unary.reshape(crf.n_states, crf.n_features)

    edges = numpy.zeros((crf.n_states, crf.n_states))
    edges[numpy.tril_indices(crf.n_states)] = weights[unary_weights:]

    return unary, edges


def printParameters(unary, edges, selector, clf, results_file) :
    with open(results_file, 'ab') as f :
        f.write('==============================\n')
        f.write(str(datetime.datetime.now())+'\n')
        f.write("Counties\n")
        f.write(str(selector)+'\n')
        f.write("C\n")
        f.write(str(clf.get_params()['C'])+'\n')
        f.write("Unary\n")
        f.write(str(unary)+'\n')
        f.write("Edge\n")
        f.write(str(edges)+'\n')


if __name__ == '__main__' :
    import itertools
    import os

    data_path = '../data/'
    iterations = 1000

    base_names = [name.split('_county_race')[0] 
                  for name in os.listdir(data_path) 
                  if name.endswith('_race.shp')]

    sample_size = len(base_names)

    X, Y = trainingData(base_names, data_path)

    crf = GraphCRF(n_states=3, n_features=sample_size)
    clf = ssvm.NSlackSSVM(model=crf, C=0.0, 
                          tol=.1)

    weights = train(clf, X, Y)
    unary, edge = extractWeights(crf, weights)

    printParameters(unary, edge, base_names, clf, 'param.txt')
    numpy.save('edge_param', edge)

    unaries = numpy.empty((iterations, 3, sample_size))
    edges = numpy.empty((iterations, 3, 3))

    average_time = 0
    for i in xrange(1, iterations+1) :

        start_time = time.time()

        selector = numpy.random.choice(sample_size, sample_size)

        resampled_X = [X[j] for j in selector]
        resampled_Y = [Y[j] for j in selector]

        weights = train(clf, resampled_X, resampled_Y)
        unary, edge = extractWeights(crf, weights)

        printParameters(unary, edge, selector, clf, 'bootstrap.txt')

        unaries[i-1, ...] = unary
        edges[i-1, ...] = edge

        end_time = time.time()
        elapsed_time = end_time - start_time
        
        average_time += (elapsed_time - average_time)/float(i)

        hours_left = (average_time * (iterations - i))/float(60 * 60)
        print str(hours_left) + ' hours left'
        

    numpy.save('unaries1.npy', unaries)
    numpy.save('edges1.py', edges)

    race = {i : race for i, race in enumerate(['white', 'black', 'hispanic'])}

    for j, i in itertools.combinations_with_replacement(race.keys(), 2) :
        file_name = '%s-%s' % (race[i], race[j])
        numpy.save(file_name, edges[..., i, j])


