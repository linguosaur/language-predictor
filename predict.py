import sys

def tally(key,dic):
	if key in dic:
		dic[key] += 1
	else:
		dic[key] = 1

def getPredictions(predictor,model):
	if predictor in model:
		return model[predictor].keys()

	return None

def predictRight(char,predictor,model):
	predictions = getPredictions(predictor,model)
	#sys.stdout.write('predictor: ' + predictor + '\n')
	#sys.stdout.write('prediction: ' + repr(predictions) + '\n')
	if predictions != None and char in predictions:
		#sys.stdout.write('prediction correct!\n')
		return True

	return False

def updateModel(char,seen,predictor,predictionIsRight,model):
	if seen != '':
		for i in range(len(predictor)):
			subseq = predictor[i:len(predictor)]
			if subseq not in model:
				model[subseq] = {}
			tally(char,model[subseq])

			if predictionIsRight: # look for previous occurence of subseq in seen
				newKey = subseq+char
				if newKey not in model:
					#sys.stdout.write('adding ' + newKey + ' as key\n')
					charLastTime = seen[seen.index(newKey)+len(newKey)]
					model[newKey] = {}
					tally(charLastTime,model[newKey])

def outputDic(dic):
	sys.stdout.write('Model:\n')
	for key in dic:
		sys.stdout.write(key + ': ' + repr(dic[key]) + '\n')

seen = ''
model = {}
inputFileName = sys.argv[1]
with open(inputFileName) as inputFile:
	[predictor,prediction] = ['','']
	char = inputFile.read(1)
	while char != '':
		#sys.stdout.write('char: ' + char + '\nseen: ' + seen + '\n')
		predictionIsRight = predictRight(char,predictor,model)
		updateModel(char,seen,predictor,predictionIsRight,model)
		
		seen += char
		if predictionIsRight:
			predictor += char
		else:
			predictor = seen[-1]
		
		char = inputFile.read(1)
		#sys.stdout.write('\n')
	
	outputDic(model)
