import re, sys, operator, jaccardLib

# To do:
# - for bigrams, include all previous elements ending at start of current element

# identify all substrings in line that are also in vocab
def parse(line, vocab):
    parsedElems = [] # contains tuples, ((start,end),elem)

    if len(line) == 0: return parsedElems

    [start,end] = [0,1]
    while end <= len(line):
        substring = line[start:end]
        if substring in vocab:
            parsedElems.append(((start,end),substring))
        if len([e for e in vocab if type(e) is str and e.startswith(substring) and e != substring]) > 0:
            end += 1
        else:
            start = end
            end = start + 1

    return parsedElems

[vocabFileName,cliquesFileName,corpusFileName] = sys.argv[1:4]
totalElems = 0
BIGRAM_RATIO_THRESH = 1.0

def tallyFreq(item, dic):
    if item in dic: dic[item] += 1
    else: dic[item] = 1
    return

# read vocab file; set up frequency table
vocabFreqs = {}
with open(vocabFileName) as vocabFile:
    vocabFileLines = vocabFile.readlines()
    for line in vocabFileLines:
        splitLine = line.rstrip().split('\t')
        if len(splitLine) == 2:
            [elem,freq] = splitLine
            vocabFreqs[elem] = int(freq)

newVocabFreqs = {}

# read cliques file
elems2cliques = {}
with open(cliquesFileName) as cliquesFile:
    cliquesFileLines = cliquesFile.readlines()
    cliqueNum = None
    for line in cliquesFileLines:
        if line[-1] == '\n':
            line = line[:-1]
        if line.startswith('Clique '):
            cliqueNumStr = line[len('Clique '):-1]
            cliqueNum = int(cliqueNumStr)
        elif cliqueNum != None:
            elem = line
            elems2cliques[elem] = cliqueNum

# count frequencies of old and new elements in corpus
totalElems = 0
parsedLines = []
with open(corpusFileName) as corpusFile:
    lineNum = 0
    for line in corpusFile:
        parsedLine = parse(line.rstrip(), set(vocabFreqs.keys()))
        parsedLines.append(parsedLine)
        lineNum += 1
        sys.stderr.write('Parsed line ' + repr(lineNum) + '\n')

        for elemNum in range(len(parsedLine)):
            (indices,elem) = parsedLine[elemNum]
            (start,end) = indices
            cliqueNum = elems2cliques[elem]

            tallyFreq(cliqueNum, vocabFreqs)

            # tally new bigrams
            prevIndexedElems = [((i1,i2),e) for ((i1,i2),e) in parsedLine if i2 == start]
            for prevIndexedElem in prevIndexedElems:
                (prevIndices,prevElem) = prevIndexedElem
                prevCliqueNum = elems2cliques[prevElem]
                
                tallyFreq((prevElem,elem), newVocabFreqs)
                tallyFreq((prevCliqueNum,elem), newVocabFreqs)
                tallyFreq((prevElem,cliqueNum), newVocabFreqs)
                tallyFreq((prevCliqueNum,cliqueNum), newVocabFreqs)
                
            totalElems += 1
    #sys.stderr.write('\n')
	
# merge two adjacent elements a, b if P(ab) > k*P(a)*P(b), where k > 1 is a constant
ratios = {}
for bigram in newVocabFreqs.keys():
    (item1,item2) = bigram
    #sys.stderr.write('new element: ' + repr(item1) + ' ' + repr(item2) + '\n')

    ratio = 1.0 * newVocabFreqs[bigram] / (vocabFreqs[item1] * vocabFreqs[item2]) * totalElems
    #sys.stderr.write('ratio: ' + repr(ratio) + '\n')
    ratios[bigram] = ratio
    if ratio > BIGRAM_RATIO_THRESH:
        sys.stderr.write('adding new elements to vocab\n')
        vocabFreqs[bigram] = newVocabFreqs[bigram]
sys.stderr.write('\n')

# output probability ratios of new vocab
#sys.stdout.write('new elements, with ratios:\n')
#for bigram, ratio in sorted(iter(ratios.items()), key=operator.itemgetter(1), reverse=True):
#    sys.stdout.write(repr(bigram) + '\t' + repr(ratio) + '\n')
#sys.stdout.write('\n')

# output sorted elements with their ratios and frequencies
#sys.stdout.write('updated vocab, with frequencies:\n')
for elem, freq in sorted(iter(vocabFreqs.items()), key=operator.itemgetter(1), reverse=True):
    sys.stdout.write(repr(elem) + '\t' + repr(1.0*freq/totalElems))
    if elem in ratios:
        sys.stdout.write('\t' + repr(ratios[elem]))
    sys.stdout.write('\n')
sys.stdout.write('\n')

sys.stdout.write('total element instances: ' + repr(totalElems) + '\n')
