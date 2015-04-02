import pysal
from pysal.weights.Contiguity import buildContiguity
from pystruct.models import GraphCRF
import pystruct.learners as ssvm
import numpy

def example(base_name) :
    shapes = pysal.open(base_name + '.shp','r')
    dbf = pysal.open(base_name + '.dbf', 'r')

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


crf = GraphCRF(n_states=3, n_features=1)
clf = ssvm.OneSlackSSVM(model=crf, C=100, inference_cache=100,
                        tol=.1)

base_names = ('la_race', 'chicago_race')

X = []
Y=  []
for name in base_names :
    x, y = example(name)
    X.append(x)
    Y.append(y)

print "estimating"
clf.fit(X, Y)
weights = clf.w
unary_weights = crf.n_states * crf.n_features
unary = weights[:unary_weights]

edges = numpy.zeros((crf.n_states, crf.n_states))
edges[numpy.triu_indices(crf.n_states)] = weights[unary_weights:]
edges[numpy.tril_indices(crf.n_states)] = weights[unary_weights:]

print 'unary'
print unary
print 'edges'
print edges
