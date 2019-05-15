import sys

k = 1.0

def updateActiveSequences(actSeqs,char,vocab):
	completedSeqs = set([])
	seqsToPrune = set([])

	# update currently active sequences
	for (seq,index) in actSeqs.items():
		if seq[index] == char:
			actSeqs[seq] += 1
			if actSeqs[seq] == len(seq):
				completedSeqs.add(seq)
				seqsToPrune.add(seq)
		else:
			# prune inactive sequences
			seqsToPrune.add(seq)

	for seq in seqsToPrune:
		actSeqs.pop(seq)

	# add new active sequences that start with char
	for seq in set(vocab.keys()) - set(actSeqs.keys()):
		if seq == char:
			completedSeqs.add(seq)
		elif seq.startswith(char):
			actSeqs[seq] = 1

	return completedSeqs

# returns True if seq predicts char strongly enough
# that is, if P(char|seq) > k*P(char), k > 1.0
def predicts(seq,char,vocab,seen):
	if 1.0*seen.count(seq+char) / vocab[seq] > k*vocab[char]/len(seen):
		return True

	return False

def updateVocab(char,seen,prevCompletedSeqs,vocab):
	seqsToPrune = set([])

	# add char as an item if not in vocab already
	if char not in vocab:
		vocab[char] = 1
	else:
		vocab[char] += 1
		# try to extend sequences that were completed just before char
		for seq in prevCompletedSeqs:
			# update frequency if seq+char already in vocab
			if seq+char in vocab:
				vocab[seq+char] += 1
			# add seq+char as new vocab item, if seq strongly predicts char
			elif predicts(seq,char,vocab,seen):
				vocab[seq+char] = seen.count(seq+char)

				# prune intermediate vocab items made redundant by extension
				if vocab[seq] == vocab[seq+char]:
					seqsToPrune.add(seq)

		for seq in seqsToPrune:
			vocab.pop(seq)

def outputDic(dic):
    for key in dic:
    	sys.stdout.write(key + ': ' + repr(dic[key]) + '\n')

def outputSet(s):
	sys.stdout.write(', '.join([repr(x) for x in list(s)]) + '\n')


inputFileName = sys.argv[1]
with open(inputFileName) as inputFile:
	seen = ''
	vocab = {} # {sequence: frequency}
	activeSequences = {} # { potential vocab item: end index of active prefix }
	prevCompletedSequences = set([])
	char = inputFile.read(1)
	seen += char
	while char != '':
		sys.stderr.write(seen + '\n')
		newCompletedSequences = updateActiveSequences(activeSequences,char,vocab)

		sys.stdout.write('Active sequences:\n')
		outputDic(activeSequences)
		sys.stdout.write('\n')

		updateVocab(char,seen,prevCompletedSequences,vocab)

		sys.stdout.write('Vocab:\n')
		outputDic(vocab)
		sys.stdout.write('\n')

		prevCompletedSequences = newCompletedSequences
		char = inputFile.read(1)
		seen += char
        
outputDic(vocab)
sys.stdout.write('\n')
