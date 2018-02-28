from evolution import evModel
from evolution import generateAverages
model =evModel(3,2,[2,2])
print model.structure
model.mutate(1,2)
print model.run([0,1,0])
model1 =evModel(3,2,[2,2])
model1.mutate(1,2)
print generateAverages([model,model1])
