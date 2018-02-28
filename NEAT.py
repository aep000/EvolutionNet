import numpy as np
import random as random
class network:
    def __init__(self, newConnectionChance, newNodeChance, inputs, outputs,activate,weightChangeChance, weightChangeRange, structure=None):
        self.MiddleNodes=[node([],staticOut=True)]*inputs
        self.cChance=newConnectionChance
        self.nChance=newNodeChance
        self.wChance=weightChangeChance
        self.wRange=weightChangeRange
        self.outputs = [node([])]*outputs
        if(structure!=None):
            c=0
            for k in structure:
                if c<len(structure)-outputs:
                    self.MiddleNodes.append(node([]))
                c+=1
            c=0
            for k in structure:
                for v in k:
                    if c<len(structure)-outputs:
                        self.MiddleNodes[c].addInput([v[0],v[1]])
                    else:
                        self.outputs[c].addInput([v[0],v[1]])
                c+=1
    def mutate():
        pass





class node:
    def __init__(self, inputNodes, function=0, staticOut=False, network):
        self.inputIndex=inputNodes
        self.inNodes=[[network.MiddleNodes[n[0]],n[1]] for n in inputNodes]
        self.activate=function
        self.staticOut=staticOut
        self.staticVal=0
    def addInput(n):
        self.inNodes.apped([network.MiddleNodes[n[0]],n[1]])
    def setStaticVal(n):
        self.staticVal=n
    def mutate(chance,range):
        for node in self.inNodes:
            change =0
            if (random.randint(0,frequency)==0):
                change = random.uniform(-rate,rate)
            node[1]+=change
    def run():
        if self.staticOut:
            return self.staticVal
        else:
            out=0
            for node in self.inNodes:
                out+= (node[0].run())*node[1]
            if self.activate=0:
                if(out<0):
                    return 0
                if(out>=0):
                    return out
            elif self.activate=1:
                return np.tanh(out)
            else:
                return 1.0 / (1 + math.exp(-out))
