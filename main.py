import math


### Number theory stuff ###
def checkPrime(n: int) -> bool:
  """Checks if n is a prime number or not"""

  if n <= 1:
    return False

  if n == 2 or n == 3:
    return True

  if n % 2 == 0 or n % 3 == 0:
    return False

  for i in range(5, int(math.sqrt(n))+1, 6):
    if n % i == 0 or n % (i + 2) == 0:
      return False

  return True

def factorTree(n:int) -> list:
  """returns the factor tree in a list form (smallest to largest)"""
  tree = []
  while n > 1:
    for i in range(2,int(n)+1):
      if n%i == 0:
        tree.append(i)
        n /= i
        break
  return tree

def factors(n:int) -> list:
  """returns all factors of n in a list (smallest to largest)"""
  list = factorTree(n)
  list.insert(0,1)
  factorD = []
  for i in list:
    for j in list:
      factorD.append(i*j)
  return rangePick(rmSame(factorD),1,n)


### Calculations ###
def root(base: float, root: float) -> float:
  """takes the root of base"""
  return math.pow(base, 1/root)


### Complex Numbers ###
def CompAdd(A: list, B: list) -> list:
  """does (A[0] + A[1]*i) + (B[0] + B[1]*i) outputs as [(Real part),(imaginary part)]. All values must be float or int"""
  return [A[0] + B[0], A[1] + B[1]]


def CompSub(A: list, B: list) -> list:
  """does (A[0] + A[1]*i) - (B[0] + B[1]*i) outputs as [(Real part),(imaginary part)]. All values must be float or int"""
  return [A[0] - B[0], A[1] - B[1]]


def CompMul(A: list, B: list) -> list:
  """does (A[0] + A[1]*i) * (B[0] + B[1]*i) outputs as [(Real part),(imaginary part)]. All values must be float or int"""
  return [A[0]*B[0]-A[1]*B[1], A[1]*B[0]+A[0]*B[1]]


def CompDev(A: list, B: list) -> list:
  """does (A[0] + A[1]*i) / (B[0] + B[1]*i) outputs as [(Real part),(imaginary part)]. All values must be float or int"""
  BDash = math.pow(B[0],2) + math.pow(B[1],2)
  ADash = CompMul(A, [B[0], -1*B[1]])
  return [ADash[0]/BDash, ADash[1]/BDash]


def CompConj(A: list) -> list:
  """returns the conjugate of A[0] + A[1]*i outputs as [(Real part),(imaginary part)]. All values must be float or int"""
  return [A[0], -1*A[1]]

def Re(A:list) -> float:
  """returns the real part of the complex number A[0] + A[1]*i"""
  return A[0]

def Im(A:list) -> float:
  """returns the imaginary part of the complex number A[0] + A[1]*i"""
  return A[1]


### Conversions ###
def Polar2Cart(r: float, theta: float, mode: str = "RAD") -> list:
  """converts polar coordinate <r,theta> to cartigean coordinate (x,y) as a list [x,y]. Optional Argument "mode" can either be "RAD" for if theta is in radians, or "DEG" if it is in degrees. Default is "RAD"."""
  if mode == "DEG":
    theta = math.radians(theta)
  return [r*math.cos(theta), r*math.sin(theta)]


def Cart2Polar(x: float, y: float, mode: str = "RAD") -> list:
  """converts cartigean coordinate (x,y) to polar coordinate <r,theta> as a list [r,theta]. Optional Argument "mode" can either be "RAD" for if you want theta to be in radians, or "DEG" for degrees. Default is "RAD"."""
  if mode == "DEG":
    if y >= 0:
      return [math.sqrt(pow(x,2)+pow(y,2)), math.degrees(math.acos(x/(math.sqrt(pow(x,2)+pow(y,2)))))]
    else:
      return [math.sqrt(pow(x,2)+pow(y,2)), math.degrees(2*math.pi-math.acos(x/(math.sqrt(pow(x,2)+pow(y,2)))))]
  else:
    if y >= 0:
      return [math.sqrt(pow(x,2)+pow(y,2)), math.acos(x/(math.sqrt(pow(x,2)+pow(y,2))))]
    else:
      return [math.sqrt(pow(x,2)+pow(y,2)), 2*math.pi-math.acos(x/(math.sqrt(pow(x,2)+pow(y,2))))]



### others ###
def rmSame(x:list) -> list:
  """removes any duplicated values"""
  y = []
  for i in x:
    if i not in y:
      y.append(i)
  return y

def rangePick(list:list,min:float,max:float = "inf") -> list:
  """returns numbers in list that are bigger than min (included), smaller than max (included). leave max blank for infinity"""
  output = []
  if max == "inf":
    for i in list:
      if i >= min:
        output.append(i)
  else:
    for i in list:
      if (i >= min) and (i <= max):
        output.append(i)
  return output

def str2list(str:str,divider:str) -> list:
  """returns a string list made out of a string, where each element is distuingished with a divider (one letter). The divider is not included in the list"""
  output = [""]
  for i in str:
    if i == divider:
      output.append("")
    else:
      output[len(output)-1] += i
  if str[len(str)-1] == divider:
    output.pop()
  return output

