import random as r

def rand(gameState,first,which):
  if first:
    return [r.randint(1,9),r.randint(1,9)]
  
  output = r.randint(1,9)
  while gameState[which-1][output-1] != 0:
    output = r.randint(1,9)
  return output

