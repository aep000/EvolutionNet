import numpy as np
import random
from operator import itemgetter
class evModel:
	def __init__(self,inputSize, outputSize, maxSize, seed=None):
		self.outputSize=outputSize
		self.inputSize=inputSize
		if(seed==None):
			self.structure=[[[0]*inputSize]*inputSize,[1]*inputSize]*maxSize
			#print self.structure
			self.structure.append([[0]*outputSize]*inputSize)
			self.structure.append([1]*outputSize)
		else:
			self.structure=seed
	def mutate(self,rate,frequency):
		isnode=False
		outStructure=[]
		for row in self.structure:
			if(isnode):
				add=[]
				for val in row:
					change =0
					if (random.randint(0,frequency)==0):
						change = random.uniform(-rate,rate)
						if((change+val)<0):
							change=0
							val=0
						if((change+val)>1):
							change=0
							val=1
					add.append(val+change)
				outStructure.append(add)
				isnode=False
			else:
				add=[]
				for vertex in row:
					semiAdd=[]
					for val in vertex:
						change = 0
						if (random.randint(0,frequency)==0):
							change = random.uniform(-rate,rate)
						semiAdd.append(val+change)
					add.append(semiAdd)
				outStructure.append(add)
				isnode=True
			self.structure=outStructure
	def run(self,inputs):
		isnode=False
		lastNodeOut=inputs
		for row in self.structure:
			if(isnode):
				tempNodeOut=[]
				c=0
				for node in row:
					tempNodeOut.append(1 / (1 + np.exp(-lastNodeOut[c])))
					c+=1
				lastNodeOut=tempNodeOut
				isnode=False
			else:
				tempNodeOut=[]
				c=0
				while(c<len(row[0])):
					out=0
					for vertex in row:
						#print lastNodeOut
						out+=vertex[c]*lastNodeOut[c]
					tempNodeOut.append(out)
					c+=1
				lastNodeOut=tempNodeOut
				isnode=True
		return lastNodeOut


'''def generateAverages(models):
	c=0
	output=[]
	isnode=False
	while c<len(models[0]):
		if(isnode):
			row=[0]*len(models[0][c])
		else:
			row=[[0]*len(models[0][c][0])]*len(models[0][c])
		for model in models:
			if(isnode):
				k=0
				for entry in model[c]:
					row[k]+=entry
					k+=1
			else:
				semirow=[]'''
def generateAverages(models):
	c=0
	output=[]
	isnode=False
	if len(models)==0:
		return None
	while c<len(models[0].structure):
		row=[]
		for model in models:
			row.append(model.structure[c])
		output.append(np.mean(row,axis=0).tolist())
		c+=1
	return output
best = evModel(6,3,6)
bestcount = 0
def testing(template=None):
	global bestcount
	global best
	if(template==None):
		models=[evModel(6,3,2) for k in range(100)]
	else:
		models=[evModel(6,3,2,template) for k in range(100)]
	bestmods=[]
	for model in models:
		model.mutate(1,4)
		c=0
		k=0
		tests = [[random.randint(0,1) for y in range(6)] for z in range(10)]
		tests2 = [[abs(num-1)for num in test] for test in tests]
		tests+=tests2
		for test in tests:
			correct = 2
			bad = [1,0]
			if sum(test)>3:
				correct=1
				bad=[0,2]
			if sum(test)<3:
				correct = 0
				bad=[1,2]
			out=model.run(test)
			if out[correct]-out[bad[0]]>0 and out[correct]-out[bad[1]]>0:
				k+=1
		bestmods.append([k,model])
		if k>bestcount:
			bestcount=k
			best=model
	bestmods.append([bestcount,best])
	bestmods=sorted(bestmods, key=itemgetter(0))
	print bestmods[0][1].run([1,0,0,0,1,1])
	print bestmods[0][1].run([1,1,1,0,1,0])
	print bestmods[0][1].run([0,1,0,0,0,1])
	return generateAverages([M[1] for M in bestmods[len(bestmods)/2:]])
last = testing()
for k in range(500):
	last = testing(last)
print evModel(0,0,0,last).run([1,1,1,0,1,0])
print evModel(0,0,0,last).run([0,0,0,0,1,0])
print evModel(0,0,0,last).run([1,1,0,0,1,0])
print "BEST"
print best.run([1,1,0,0,1,0])
print best.run([0,0,0,0,1,0])
print best.run([1,1,1,0,1,0])
