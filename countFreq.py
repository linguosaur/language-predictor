import re, sys, operator, jaccardLib


contextFileName = sys.argv[1]
corpusFileName = sys.argv[2]
totalTokens = 0

contextTable = {}
with open(contextFileName) as contextFile:
    contextFileLines = contextFile.readlines()
    jaccardLib.fillProfiles(contextTable, contextFileLines)
freqs = {x:0 for x in contextTable.keys()}

with open(corpusFileName) as corpusFile:
    for line in corpusFile:
        activeElems = []
        for elem in line.rstrip():
            elemsToDeactivate = []
            for i in range(len(activeElems)):
                if activeElems[i] + elem in freqs.keys():
                    freqs[activeElems[i]+elem] += 1
                    elemsToDeactivate.append(i)
                elif len([x for x.startswith(activeElems[i]+elem)]) > 0:
                    activeElems[i] += elem
                else:
                    elemsToDeactivate.append(i)
            for i in elemsToDeactivate:
                del activeElems[i]
                    
            activeElems.extend([x for x in x.startswith(elem)])

        if elem not in freqs: freqs[elem] = 1
        else: freqs[w] += 1
        totalTokens += 1

for elem, freq in sorted(freqs.iteritems(), key=operator.itemgetter(1), reverse=True):
    sys.stdout.write(elem + '\t' + repr(freq) + '\n')

sys.stdout.write('total element tokens:' + repr(totalTokens) + '\n')
