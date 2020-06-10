import sys, jaccardLib

def readContextFile(contextFileName):
    contextsFileLines = []
    with open(contextsFileName) as contextsFile:
        sys.stderr.write('reading contexts file . . . ')
        contextsFileLines = contextsFile.readlines()
        sys.stderr.write('done.\n\n')

    return contextsFileLines

# returns the subset of sortedNeighbours with the lowest score
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
def findClique(elem, clique, contextsTable):
    
    if elem in clique:
        return clique

    clique.add(elem)
    sortedNeighbours = jaccardLib.findSortedNeighbours(elem, contextsTable)
    nearestNeighbours = set([x for (x,y) in findNearest(sortedNeighbours)])
    
    if len(nearestNeighbours - clique) == 0:
        return clique
    
    for neighbour in nearestNeighbours:
        clique = findClique(neighbour, clique, contextsTable)

    return clique

def findCliques(contextsTable):
    cliques = []
    elem2clique = {}
    for elem in contextsTable:
        if elem not in elem2clique:
            clique = findClique(elem, set([]), contextsTable)
            cliquedElems = clique.intersection(elem2clique.keys())

            if len(cliquedElems) > 0:
                cliqueIndex = min([elem2clique[e] for e in cliquedElems])
                for e in clique:
                    if e in elem2clique:
                        cliqueToMerge = cliques[elem2clique[e]]
                        cliques[cliqueIndex] = cliques[cliqueIndex].union(cliqueToMerge)
                    else:
                        cliques[cliqueIndex].add(e)
                        elem2clique[e] = cliqueIndex
            else:
                cliques.append(clique)

            for e in clique:
                elem2clique[e] = len(cliques)-1

    return cliques

def printCliques(cliques):
    for clique_i in range(len(cliques)):
        sys.stdout.write('Clique ' + repr(clique_i) + ':\n')
        for elem in cliques[clique_i]:
            sys.stdout.write(elem + '\n')


contextsFileName = sys.argv[1]
contextsFileLines = readContextFile(contextsFileName)

contextsTable = {}
jaccardLib.fillProfiles(contextsTable, contextsFileLines)

cliques = findCliques(contextsTable)
printCliques(cliques)
