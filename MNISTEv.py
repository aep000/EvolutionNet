import numpy as np
import random
from sklearn.datasets import load_digits
from operator import itemgetter
from mnist import MNIST
import math
class evModel:
	def __init__(self,inputSize, outputSize, maxSize, seed=None):
		self.outputSize=outputSize
		self.inputSize=inputSize
		if(seed==None):
			self.structure=[[[1]*inputSize]*inputSize]*maxSize
			#print self.structure
			self.structure.append([[0]*outputSize]*inputSize)
		else:
			self.structure=seed
	def mutate(self,rate,frequency):
		outStructure=[]
		for row in self.structure:
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
			self.structure=outStructure
	def run(self,inputs):
		lastNodeOut=inputs
		for row in self.structure:
			tempNodeOut=[]
			c=0
			while(c<len(row[0])):
				out=0
				for vertex in row:
					#print lastNodeOut
					out+=vertex[c]*lastNodeOut[c]
				tempNodeOut.append(1 / (1 + math.exp(-out)))
				c+=1
			lastNodeOut=tempNodeOut
		print lastNodeOut
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
	print models
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
def genomicBreed(models,scores,genSize, scoreIncreasing=True):
	scoreProb= []
	total = sum(scores)
	for score in scores:
		if(not scoreIncreasing):
			scoreProb.append(1-(score/total))
		else:
			scoreProb.append(score/total)
	nextGen=[]
	print scoreProb
	for c in xrange(genSize):
		individual=[]
		r1=0
		for k1 in models[0].structure:
			row=[]
			r2=0
			for k2 in k1:
				row2=[]
				r3=0
				for k3 in k2:
					row2.append(models[np.random.choice(len(models), 1, p=scoreProb)[0]].structure[r1][r2][r3])
					r3+=1
				row.append(row2)
				r2+=1
			individual.append(row)
			r1+=1
		nextGen.append(individual)
	return nextGen

best = evModel(6,3,6)
bestcount = 0
import operator
mndata = MNIST('MNIST')
images, labels = mndata.load_training()
newimages = []
for image in images[:200]:
	temp =[]
	c=0
	while c< 729:
		if(c>27 and c%27==0):
			c+=27	
		if(c+27<729):
			temp.append(max([np.tanh(image[c]),np.tanh(image[c+1]),np.tanh(image[c+27]),np.tanh(image[c+28])]))
		c+=1
	newimages.append(temp)
images=newimages
print "++++++++++"
print len(images[0])
def testing(template=None):
	global images
	global labels
	global bestcount
	global best
	if(template==None):
		models=[evModel(378,10,5) for k in range(25)]
		for model in models:
			model.mutate(.05,80)
	else:
		models=[evModel(378,10,5,template[k]) for k in range(len(template-1))]
	bestmods=[]
	outset=[]
	for model in models:
		model.mutate(.05,1000)
		c=0
		k=0
		seed =[random.randint(0,125) for z in range(100)]
		tests = [images[seed[z]] for z in range(8)]
		answers = [labels[seed[z]] for z in range(8)]
		outs=[]
		for test, answer in zip(tests, answers):
			print c
			out = model.run(test)
			aindex, value = max(enumerate(out), key=operator.itemgetter(1))
			print str(aindex)+"|"+str(answer)
			outs.append(aindex)
			k+=out[answer]*10
			del out[answer]
			k-=sum(out)
			print k
			c+=1
		bestmods.append((k,model))
		if k>bestcount:
			bestcount=k
			best=model
	if(len(set(outset))==1):
		print "genocide"
		crazyMod=evModel(378,10,5)
		crazyMod.mutate(.05,50)
		return generateAverages([crazyMod])
		
	bestmods=sorted(bestmods, key=itemgetter(0))
	return genomicBreed([M[1] for M in bestmods],[1/M[0] for M in bestmods],1)
seed = evModel(378,10,3)
seed.mutate(.05,50)
last = testing()
while True:
	last = testing(last)
	print evModel(729,10,10,last).run(images[0])

