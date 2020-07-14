## finds most frequently-repeated substrings in text

import sys
from math import log2


def codeLenPerChar(string, text, freq):
    stringLen, textLen = len(string), len(text)
    codeLen = log2(textLen/stringLen/freq)
    return codeLen/stringLen

def getFreq(string, text, freqsCache, phraseBook, iteration):
    freq = 0
    if string in freqsCache:
        freq = freqsCache[string]
    else:
        if iteration == 0:
            freq = text.count(string)
        else:
            possiblePhrases = [phraseBook[p] for p in phraseBook if p.startswith(string)]
            if len(possiblePhrases) > 0:
                freq = sum(possiblePhrases)
            else:
                freq = 1
        if freq > 1:
            freqsCache[string] = freq

    return freq

def tallyPhraseBook(string, phraseBook):
    if string not in phraseBook:
        phraseBook[string] = 1
    else:
        phraseBook[string] += 1

def cutString(freq, lastCodeLenPerChar, thisCodeLenPerChar):
    return freq == 1 or lastCodeLenPerChar > 0.0 and thisCodeLenPerChar > lastCodeLenPerChar

def segment(text):
    phraseBook, lastTotalCodeLen = {}, 0.0
    iteration, iterate = 0, True
    MAX_ITERATIONS = 5
    while iterate:
        string, lastCodeLenPerChar, charsRead, freqsCache, thisTotalCodeLen, newPhraseBook = '', 0.0, 0, {}, 0.0, {}

        sys.stderr.write('Iteration ' + repr(iteration) + ':\n')
        for char in text:
            string += char
            freq = getFreq(string, text, freqsCache, phraseBook, iteration)
            thisCodeLenPerChar = codeLenPerChar(string, text, freq)

            if cutString(freq, lastCodeLenPerChar, thisCodeLenPerChar):
                phrase = string[:-1]
                tallyPhraseBook(phrase, newPhraseBook)
                thisTotalCodeLen += len(phrase)*lastCodeLenPerChar
                string = char
                lastCodeLenPerChar = codeLenPerChar(char, text, freq)
            else:
                lastCodeLenPerChar = thisCodeLenPerChar
            
            charsRead += 1
            if charsRead % 10000 == 0:
                sys.stderr.write(repr(charsRead) + ', ')
                sys.stderr.flush()

        sys.stderr.write('\Average code length per character: ' + repr(thisTotalCodeLen/len(text)) + '\n')
        if iteration == 0 or thisTotalCodeLen < lastTotalCodeLen and iteration < MAX_ITERATIONS:
            iteration += 1
            lastTotalCodeLen = thisTotalCodeLen
            phraseBook = newPhraseBook
        else:
            iterate = False

        sys.stderr.write('\n')

    return phraseBook

def printPhrases(phraseBook):
    for phrase, freq in sorted(phraseBook.items()):
        sys.stdout.write('\t'.join([phrase, repr(freq)]) + '\n')


textFilename = sys.argv[1]
with open(textFilename) as textFile:
    text = textFile.read()

phraseBook = segment(text)
printPhrases(phraseBook)
