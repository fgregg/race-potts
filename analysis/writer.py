import numpy
import itertools

edges = numpy.load('edges.npy')
print(edges.shape)

race = {i : race for i, race in enumerate(['white', 'black', 'hispanic'])}
for j, i in itertools.combinations_with_replacement(race.keys(), 2) :
    print i,j
    file_name = '%s-%s' % (race[i], race[j])
    print file_name
    numpy.save(file_name, edges[..., i, j])
