import random as r

productNames = []
currentPrices = []
pastPrices = [[0]]
  
class user:
  def __init__(self,name:str) -> None:
    self.name = name
    self.bank = 0
    self.stocks = [len(productNames)]

  def buy(self,nameOrID,amount:int):
    if type(nameOrID) == str and nameOrID in productNames:
      nameOrID = productNames.index(nameOrID)
    elif nameOrID not in productNames:
      raise f"product {nameOrID} does not exist"
    else:
      raise f"product with id {nameOrID} does not exist"
    
    self.stocks[nameOrID] += amount
    self.bank -= currentPrices[nameOrID]*amount

  def sell(self,nameOrID,amount:int):
    if type(nameOrID) == str and nameOrID in productNames:
      nameOrID = productNames.index(nameOrID)
    elif nameOrID not in productNames:
      raise f"product {nameOrID} does not exist"
    else:
      raise f"product with id {nameOrID} does not exist"
    
    if amount > self.stocks[nameOrID]:
      amount = self.stocks[nameOrID]

    self.stocks[nameOrID] -= amount
    self.bank += currentPrices[nameOrID]*amount


###########

def addProduct(name:str = f"product #{len(stocks)+1}",basePrice:float = r.randrange(1,100)):
  """add a product to the stock market"""
  productNames.append(name)
  currentPrices.append(basePrice)
  if len(pastPrices) > 1:
    pastPrices.append([0])

def removeProduct(nameOrID):
  """removes a product from the stock market"""
  if type(nameOrID) == str and nameOrID in productNames:
      nameOrID = productNames.index(nameOrID)
  elif nameOrID not in productNames:
    raise f"product {nameOrID} does not exist"
  else:
    raise f"product with id {nameOrID} does not exist"

  currentPrices.pop(nameOrID)
  pastPrices.pop(nameOrID)
  productNames.pop(nameOrID)

def tick():
  for i in range(len(productNames)):
    pastPrices[i].append(currentPrices[i])
    currentPrices[i] *= r.random/2 - 0.5

def printMarket():
  for i in range(len(productNames)):
    print(f"{i+1}) {productNames[i]}")
    print(f"    price: ${currentPrices[i]}")
    print(f"           {currentPrices[i]/pastPrices[i][len(pastPrices[i]-1)]}%")



###############