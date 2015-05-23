import pysal
from pysal.weights.Contiguity import buildContiguity
from pystruct.models import GraphCRF
import pystruct.learners as ssvm
import numpy
import datetime

def example(base_name) :
    shapes = pysal.open(base_name + '_county_race.shp','r')
    dbf = pysal.open(base_name + '_county_race.dbf', 'r')

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


base_names = ('cook', 'la', 'hennepin', 
              'harris', 'new_york', 'fulton', 'maricopa')

X = []
Y=  []

city_indicator = numpy.zeros(len(base_names))

for i, name in enumerate(base_names) :
    x, y = example(name)
    features, edgelist = x
    n_nodes = features.shape[0]
    features = city_indicator.copy()
    features[i] = 1
    features = numpy.tile(features, (n_nodes, 1))
    X.append((features, edgelist))
    Y.append(y)

crf = GraphCRF(n_states=3, n_features=len(city_indicator))
clf = ssvm.NSlackSSVM(model=crf, C=0.0, 
                      tol=.1)


print "estimating"
clf.fit(X, Y)
weights = clf.w
unary_weights = crf.n_states * crf.n_features
unary = weights[:unary_weights]
unary = unary.reshape(crf.n_states, crf.n_features)

edges = numpy.zeros((crf.n_states, crf.n_states))
edges[numpy.tril_indices(crf.n_states)] = weights[unary_weights:]
print(numpy.tril_indices(crf.n_states))

numpy.set_printoptions(precision=1)

with open('results.txt', 'ab') as f :
    f.write('==============================\n')
    f.write(str(datetime.datetime.now())+'\n')
    f.write("Counties\n")
    f.write(str(base_names)+'\n')
    f.write("C\n")
    f.write(str(clf.get_params()['C'])+'\n')
    f.write("Unary\n")
    f.write(str(unary)+'\n')
    f.write("Edge\n")
    f.write(str(edges)+'\n')

