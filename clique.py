import sys, jaccardLib

# retruns the subset of sortedNeighbours with the lowest score
def findNearest(sortedNeighbours):
    nearestNeighbours = set([])
    minScore = 0.0
    for i in range(len(sortedNeighbours)):
        (neighbourElem,neighbourScore) = sortedNeighbours[i]
        if i == 0:
            if neighbourScore < 1.0:
                minScore = neighbourScore
            else:
                return nearestNeighbours
        if neighbourScore == minScore:
            nearestNeighbours.add((neighbourElem,neighbourScore))
        elif neighbourScore > minScore:
            break

    return nearestNeighbours

# clique: a set of elements whose nearest neighbours are all found within in the clique
def findClique(elem, clique):
#	sys.stderr.write('elem: ' + elem + '\n')
#	sys.stderr.write('clique: ' + repr(clique) + '\n')

	if elem in clique:
	    return clique

	clique.add(elem)

	sortedNeighbours = jaccardLib.findSortedNeighbours(elem, contextsTable)
	nearestNeighbours = set([x for (x,y) in findNearest(sortedNeighbours)])

#	sys.stderr.write('nearest neighbours of ' + elem + ' are ')
#	sys.stderr.write(' '.join(list(nearestNeighbours)) + '\n')

	if len(nearestNeighbours - clique) == 0:
	    return clique

	for neighbour in nearestNeighbours:
	    clique = findClique(neighbour, clique)

	return clique
 

contextsFileName = sys.argv[1]

contextsFileLines = []
with open(contextsFileName) as contextsFile:
    sys.stderr.write('reading contexts file . . . ')
    contextsFileLines = contextsFile.readlines()
    sys.stderr.write('done.\n\n')

contextsTable = {}
jaccardLib.fillProfiles(contextsTable, contextsFileLines)

cliques = []
elem2clique = {}
for elem in contextsTable:
#   sys.stderr.write(elem + '\n')

    if elem not in elem2clique:
#	sys.stderr.write(elem + ' is new. Clique contains ')
	clique = findClique(elem, set([]))
#	sys.stderr.write(' '.join(list(clique)) + '\n')

	cliquedElems = clique.intersection(elem2clique.keys())
#	sys.stderr.write('already cliqued: ' + ' '.join(list(cliquedElems)) + '\n')

	if len(cliquedElems) > 0:
    	cliqueIndex = min([elem2clique[e] for e in cliquedElems])
#	sys.stderr.write('merging everything to Clique ' + repr(cliqueIndex) + '\n')

    	for e in clique:
            if e in elem2clique:
		cliqueToMerge = cliques[elem2clique[e]]
		cliques[cliqueIndex] = cliques[cliqueIndex].union(cliqueToMerge)
            else:
                cliques[cliqueIndex].add(e)
		elem2clique[e] = cliqueIndex
	    else:
		cliques.append(clique)
#	    	sys.stderr.write('adding Clique ' + repr(len(cliques)-1) + '\n')

    	for e in clique:
            elem2clique[e] = len(cliques)-1

#	sys.stderr.write('\n')
            
# print results
for clique_i in range(len(cliques)):
    sys.stdout.write('Clique ' + repr(clique_i) + ':\n')
    for elem in cliques[clique_i]:
        sys.stdout.write(elem + '\n')
