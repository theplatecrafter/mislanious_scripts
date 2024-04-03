import game as g
import random as r
import math as m

## [<1:input(from outside) or 2:node(internal)>,<which input/node>,<3:output(to outside) or 2:node>,<which output/node>,<weight>]
## if WeightSize set to 4, then the range is -4.0 to +4.0 included
## last list in 2dNeuralNetwork array is [NumberOfNodes,NumberOfInput,NumberOfOutput,WeightSize,WeightDataSize]

defaultWeightDataSize = 4
defaultWeightSize = 4

def randomNetwork(NumberOfNodes:int,NumberOfInput:int,NumberOfOutput:int,NumberOfConnections:int,WeightSize:float = defaultWeightSize,WeightDataSize:int = defaultWeightDataSize):
  out = [[]]
  for i in range(NumberOfConnections):
    out[-1].append(r.randint(1,2))
    if out[-1][-1] == 1:
      out[-1].append(r.randint(0,NumberOfInput-1))
    else:
      out[-1].append(r.randint(0,NumberOfNodes-1))
    out[-1].append(r.randint(2,3))
    if out[-1][-1] == 3:
      out[-1].append(r.randint(0,NumberOfOutput-1))
    else:
      out[-1].append(r.randint(0,NumberOfNodes-1))
    out[-1].append(r.randint(0,m.pow(10,WeightDataSize)-1))
    out.append([])
  out.pop()
  
  out.append([NumberOfNodes,NumberOfInput,NumberOfOutput,WeightSize,WeightDataSize])
  return out  

def visualizeNetwork(twoDneuralNetwork:list):
  NumberOfNodes = twoDneuralNetwork[-1][0]
  NumberOfInput = twoDneuralNetwork[-1][1]
  NumberOfOutput = twoDneuralNetwork[-1][2]
  WeightSize = twoDneuralNetwork[-1][3]
  WeightDataSize = twoDneuralNetwork[-1][4]
  print(f"{NumberOfNodes} nodes, {NumberOfInput} inputs, {NumberOfOutput} outputs, {len(twoDneuralNetwork)-1} connections, weight: {WeightSize*-1} to +{WeightSize}, with weight data size of {WeightDataSize}, ranging weight from 0 to {m.pow(10,WeightDataSize)-1}")
  for i in range(len(twoDneuralNetwork)-1):
    print(f"connection #{i+1} connects ",end="")
    if twoDneuralNetwork[i][0] == 1:
      print(f"input #{twoDneuralNetwork[i][1]+1} and ",end="")
    else:
      print(f"node #{twoDneuralNetwork[i][1]+1} and ",end="")
    if twoDneuralNetwork[i][2] == 3:
      print(f"output #{twoDneuralNetwork[i][3]+1} with a weight of ",end="")
    else:
      print(f"node #{twoDneuralNetwork[i][3]+1} with a weight of ",end="")
    print(f"{int(((twoDneuralNetwork[i][4]/(m.pow(10,WeightDataSize)-1)-0.5)*2*WeightSize)*1000)/1000}")  ## data weight to actuall weight

def lookForInputOf(twoDneuralNetwork:list,type:int,which:int):
  out = []
  for a in range(len(twoDneuralNetwork)-1):
    if twoDneuralNetwork[a][0] == type and twoDneuralNetwork[a][1] == which:
      out.append(a)
  return out

def runNetwork(twoDneuralNetwork:list,inputArray:list):
  NumberOfNodes = twoDneuralNetwork[-1][0]
  NumberOfInput = twoDneuralNetwork[-1][1]
  NumberOfOutput = twoDneuralNetwork[-1][2]
  WeightSize = twoDneuralNetwork[-1][3]
  WeightDataSize = twoDneuralNetwork[-1][4]
  if NumberOfInput != len(inputArray):
    print("warning: input array length does not match the criteria for this neural network")
    if NumberOfInput > len(inputArray):
      while NumberOfInput != len(inputArray):
        inputArray.append(0)
    else:
      inputArray = inputArray[:NumberOfInput]
  output = []
  for i in range(NumberOfOutput):
    output.append(0)
  
  for i in range(NumberOfInput):
    conncetedNodesOrOutputs = lookForInputOf(twoDneuralNetwork,1,i)
    for j in conncetedNodesOrOutputs:
      if twoDneuralNetwork[j][2] == 3:
        
  
  
  

for i in range(1000):
  network = randomNetwork(r.randint(1,255),r.randint(1,255),r.randint(1,255),r.randint(1,255),r.random()*10,r.randint(1,10))
  visualizeNetwork(network)