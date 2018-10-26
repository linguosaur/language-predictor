import sys

trainingFileName = sys.argv[1]
trainingText = []
elemDic = {}

with open(trainingFileName) as trainingFile:
    trainingText = trainingFile.readlines()

for line in trainingText:
    line = line.strip()
    for elem_i in range(len(line)):
        elem = line[elem_i]
        if elem not in elemDic:
            elemDic[elem] = set()
        (leftContext,rightContext) = ('','')
        if elem_i > 0:
            leftContext = line[elem_i-1]
        if elem_i < len(line)-1:
            rightContext = line[elem_i+1]
        elemDic[elem].add((leftContext,rightContext))

# print results
for elem in elemDic:
    sys.stdout.write(elem + ':\n')
    for context in elemDic[elem]:
        (leftContext,rightContext) = context
        sys.stdout.write(leftContext + ' ___ ' + rightContext + '\n')
    sys.stdout.write('\n')
