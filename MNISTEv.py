import numpy as np
import random
from sklearn.datasets import load_digits
from operator import itemgetter
from mnist import MNIST
from evolution import evModel
from evolution import generateAverages
import math

best = evModel(6,3,6,activation=1)
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
			temp.append(max([np.tanh(image[c]*1.0),np.tanh(image[c+1]*1.0),np.tanh(image[c+27]*1.0),np.tanh(image[c+28]*1.0)]))
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
		models=[evModel(378,10,5,activation=1) for k in range(25)]
		for model in models:
			model.mutate(2,4)
	else:
		models=[evModel(378,10,5,template[k],activation=1) for k in range(len(template))]
	bestmods=[]
	outset=[]
	for model in models:
		model.mutate(.5,4)
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
			k+=(out[answer])*10
			del out[answer]
			k-=1-sum(out)
			print k
			c+=1
		bestmods.append((k,model))
		if k>bestcount:
			bestcount=k
			best=model
	if(len(set(outset))==1):
		print "genocide"
		crazyMod=evModel(378,10,5,activation=1)
		crazyMod.mutate(.05,50)
		return generateAverages([crazyMod])

	bestmods=sorted(bestmods, key=itemgetter(0))
	print bestmods
	return generateAverages([M[1] for M in bestmods[len(bestmods)/2:]])
seed = evModel(378,10,3,activation=1)
seed.mutate(.5,2)
last = testing()
while True:
	last = testing(last)
	print evModel(729,10,10,last,activation=1).run(images[0])
