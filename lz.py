import sys
from operator import itemgetter

phraseBook = {}
longestPrefix = ''
activePhrases = set([])

BYTES_IN_CHAR = 1

def updateActivePhrases(string):
    global phraseBook, activePhrases
    if len(activePhrases) == 0 and len(phraseBook) > 0:
        activePhrases = set(phraseBook.keys())
    activePhrases = set([s for s in activePhrases if s.startswith(string)])

def inPhraseBook(string):
    updateActivePhrases(string)
    return len(activePhrases) > 0

def readNextChar(textfile):
    nextChar = textfile.read(BYTES_IN_CHAR)
    if nextChar == None:
        return None

    global phraseBook, longestPrefix
    if inPhraseBook(longestPrefix+nextChar):
        phraseBook[longestPrefix+nextChar] += 1
        longestPrefix += nextChar
    else:
        phraseBook[longestPrefix+nextChar] = 1
        longestPrefix = ''

    return nextChar

def printPhraseBook():
    for k,v in sorted(phraseBook.items(), key=itemgetter(1), reverse=True):
        sys.stdout.write('\t'.join([k,repr(v)]) + '\n')


textFilename = sys.argv[1]
textFile = open(textFilename)

charsRead = 0
while readNextChar(textFile) != None and charsRead <= 50000:
    charsRead += 1
    if charsRead % 5000 == 0:
        sys.stderr.write(repr(charsRead) + ', ')
        sys.stderr.flush()
    
    continue

printPhraseBook()
