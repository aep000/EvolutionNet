import numpy as np
import random
from operator import itemgetter
class evModel:
	def __init__(self,inputSize, outputSize, maxSize, seed=None):
		self.outputSize=outputSize
		self.inputSize=inputSize
		if(seed==None):
			self.structure=[[[1]*inputSize]*inputSize,[0]*inputSize]*maxSize
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
					tempNodeOut.append(np.tanh(lastNodeOut[c]))
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
					tempNodeOut.append(out+1)
					c+=1
				lastNodeOut=tempNodeOut
				isnode=True
		#print lastNodeOut
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
		models1=[evModel(9,9,4) for k in range(200)]
		models2=[evModel(9,9,4) for k in range(200)]
	else:
		models1=[evModel(9,9,4,template[0]) for k in range(100)]
		models2=[evModel(9,9,4,template[1]) for k in range(100)]
	models = zip(models1,models2)
	bestmods1=[]
	bestmods2=[]
	for m1, m2 in models:
		m1.mutate(3,2)
		m2.mutate(3,2)
		best = ticktactoe(m1,m2)
		bestmods1.append([best[0],m1])
		bestmods2.append([best[1],m2])
	bestmods1=sorted(bestmods1, key=itemgetter(0))
	bestmods2=sorted(bestmods2, key=itemgetter(0))
	return [generateAverages([M[1] for M in bestmods1[len(bestmods1)/4:]]),generateAverages([M[1] for M in bestmods2[len(bestmods2)/4:]])]
	#return generateAverages(bestmods)
def gameover(check, board):
	if(board[0]==check and board[0]==board[1] and board[1]==board[2]):
		return True
	if(board[0]==check and board[0]==board[3] and board[3]==board[6]):
		return True
	if(board[0]==check and board[0]==board[4] and board[4]==board[8]):
		return True
	if(board[3]==check and board[3]==board[4] and board[3]==board[5]):
		return True
	if(board[6]==check and board[6]==board[7] and board[6]==board[8]):
		return True
	if(board[1]==check and board[1]==board[4] and board[4]==board[7]):
		return True
	if(board[2]==check and board[2]==board[5] and board[5]==board[8]):
		return True
	if(board[2]==check and board[2]==board[4] and board[6]==board[2]):
		return True
	return False
lastwinner=0
streak=1
def ticktactoe(player1= None ,player2=None):
	global lastwinner
	global streak
	if (player1==None):
		player1= evModel(9,9,8)
		player2=evModel(9,9,8)
		player1.mutate(2,2)
		player2.mutate(2,2)
	game = [0]*9
	turns = 0
	end = False
	winner = player1
	c=0
	while not end:
		p1move = player1.run(game)
		p1move = p1move.index(max(p1move))

		if(game[p1move]!=0):
			print "player failed"
			return [-100+c,10+c]
		else:
			print "move played"
			game[p1move] = 1
		if gameover(1,game):
			if (lastwinner ==1):
				streak+=1
			else:
				streak =1
				lastwinner=1
			print "WINNER 1"
			return [1000+(-100*c),(-5+c)*streak]
		p2move = player2.run(game)
		p2move = p2move.index(max(p2move))
		if(game[p2move]!=0):
			print "player failed"
			return [10+c,-10000+c]
		else:
			print "move played"
			game[p2move] = -1
		if gameover(-1,game):
			if (lastwinner ==-1):
				streak+=1
			else:
				streak =1
				lastwinner=-1
			print "WINNER 2"
			return [(-5+c)*streak,1000+(-100*c)]
		if(sum(game)==7):
			print "TIE"
			return [200,200]
		print game
		c+=1

def playticktactoe(player1= None ,):
	if (player1==None):
		player1= evModel(9,9,8)
		player2=evModel(9,9,8)
		player1.mutate(5,10)
		player2.mutate(5,10)
	game = [0]*9
	turns = 0
	end = False
	winner = player1

	c=0
	while not end:
		p1move = player1.run(game)
		p1move = p1move.index(max(p1move))

		if(game[p1move]!=0):
			print "player failed"
			return [-100+c,10+c]
		else:
			print "move played"
			game[p1move] = 1
		if gameover(1,game):
			print "WINNER 1"
			return [1000+(-100*c),-c*2]
		p2move = int(raw_input("play"))
		if(game[p2move]!=0):
			print "player failed"
			return [10+c,-100+c]
		else:
			print "move played"
			game[p2move] = -1
		if gameover(-1,game):
			print "WINNER 2"
			return [c*2,1000+(-100*c)]
		if(sum(game)==7):
			print "TIE"
			return [200,200]
		print game
		c+=1
last = testing()
for k in range(1000):
	last = testing(last)
playticktactoe(evModel(9,9,4,last[0]))
