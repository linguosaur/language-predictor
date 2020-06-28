import sys
from operator import itemgetter

phrasesInWindowOrdered = []
phraseBook = {}
posLastSeen = {}
longestPrefix = ''
activePhrases = set([])
charsRead = 0

BYTES_IN_CHAR = 1
WINDOW_SIZE = 5000

def updateActivePhrases(phrase):
    global phraseBook, activePhrases
    if len(activePhrases) == 0 and len(phraseBook) > 0:
        activePhrases = set(phraseBook.keys())
    activePhrases = set([p for p in activePhrases if p.startswith(phrase)])

def inPhraseBook(phrase):
    updateActivePhrases(phrase)
    return len(activePhrases) > 0

def tallyPhraseBook(phrase):
    global phraseBook
    if phrase in phraseBook:
        phraseBook[phrase] += 1
    else:
        phraseBook[phrase] = 1        

def inWindow(pos):
    global charsRead, WINDOW_SIZE
    if pos >= charsRead - WINDOW_SIZE:
        return True

    return False

def prune():
    global charsRead, posLastSeen, phrasesInWindowOrdered, phraseBook
    phrase, pos = phrasesInWindowOrdered[0]
    while not inWindow(pos):
        phrasesInWindowOrdered.pop(0)
        if phrase in posLastSeen and not inWindow(posLastSeen[phrase]):
            del phraseBook[phrase]
            del posLastSeen[phrase]
        phrase, pos = phrasesInWindowOrdered[0]

def recordInAll(phrase, startPos):
    global phrasesInWindowOrdered, phraseBook, posLastSeen
    tallyPhraseBook(phrase)
    phrasesInWindowOrdered.append((phrase, startPos))
    posLastSeen[phrase] = startPos

def readNextChar(textfile):
    global charsRead, phrasesInWindowOrdered, phraseBook, posLastSeen, longestPrefix
    
    nextChar = textfile.read(BYTES_IN_CHAR)
    startPos = charsRead-len(longestPrefix)
    newPhrase = longestPrefix + nextChar
    
    if inPhraseBook(newPhrase):
        longestPrefix = newPhrase
    else:
        if len(longestPrefix) > 0:
            recordInAll(longestPrefix, startPos)
            longestPrefix = nextChar

        if nextChar == None:
            return None

        recordInAll(newPhrase, startPos)
        prune()

    charsRead += 1

    return nextChar

def printPhraseBook():
    global phraseBook, posLastSeen
    for phrase,freq in sorted(phraseBook.items(), key=itemgetter(1), reverse=True):
        sys.stdout.write('\t'.join([phrase,repr(freq),repr(posLastSeen[phrase])]) + '\n')

def processStream():
    while readNextChar(textFile) != None and charsRead <= 500000:
##        sys.stderr.write(longestPrefix + '\t')
##        sys.stderr.flush()
        if charsRead % 5000 == 0:
            sys.stderr.write(repr(charsRead) + ', ')
            sys.stderr.flush()
        continue


textFilename = sys.argv[1]
textFile = open(textFilename)

processStream()
printPhraseBook()
