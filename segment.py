## finds most frequently-repeated substrings in text

import sys
from math import log2

phraseBook = set([])

def codeLenPerChar(string, text, freq):
    return log2(len(text)/len(string)/freq)/len(string)

def segment(text):
    string = ''
    lastCodeLenPerChar = 0.0
    charsRead = 0
    for char in text:
        string += char
        freq = text.count(string)
        thisCodeLenPerChar = codeLenPerChar(string, text, freq)
        if freq == 1 or lastCodeLenPerChar > 0.0 and thisCodeLenPerChar > lastCodeLenPerChar:
            phraseBook.add(string[:-1])
            string = char
            lastCodeLenPerChar = codeLenPerChar(char, text, freq)
        else:
            lastCodeLenPerChar = thisCodeLenPerChar
            
        charsRead += 1
        if charsRead % 50 == 0:
            sys.stderr.write(repr(charsRead) + ', ')
            sys.stderr.flush()
        if charsRead == 1000:
            return

def printPhrases(phraseBook):
    for phrase in sorted(phraseBook):
        print(phrase)

textFilename = sys.argv[1]
text = open(textFilename).read()

segment(text)
printPhrases(phraseBook)