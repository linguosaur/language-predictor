import sys

def tally(key,dic):
	if key in dic:
		dic[key] += 1
	else:
		dic[key] = 1

def updateModel(char,seen,model):
	if seen != '':
		predictor = seen[-1]
		sys.stdout.write('predictor: ' + predictor + '\n')
		if predictor not in model:
			model[predictor] = {}
		tally(char,model[predictor])

def outputDic(dic):
	for key in dic:
		sys.stdout.write(key + ': ' + repr(dic[key]) + '\n')
	sys.stdout.write('\n')

seen = ''
model = {}
inputFileName = sys.argv[1]
with open(inputFileName) as inputFile:
	prediction = ''
	char = inputFile.read(1)
	while char != '':
		sys.stdout.write('char: ' + char + '\nseen: ' + seen + '\n')
		updateModel(char,seen,model)
		outputDic(model)
		seen += char
		char = inputFile.read(1)
