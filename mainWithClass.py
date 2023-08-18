import math

class Complex():
  def __init__(self,real:float,imaginary:float):
    self.Re = real
    self.Im = imaginary

  def __str__(self):
    if self.Re != 0:
      if self.Im < 0:
        return f"{self.Re} - {abs(self.Im)} i"
      elif self.Im == 0:
        return str(self.Re)
      elif self.Im > 0:
        if self.Im == 1:
          return f"{self.Re} + i"
        else:
          return f"{self.Re} + {self.Im} * i"
    else:
      if self.Im == 0:
        return "0"
      else:
        return str(self.Im)

  def __add__(self,other):
    return Complex(self.Re+other.Re,self.Im+other.Im)
  
  def __sub__(self,other):
    return Complex(self.Re-other.Re,self.Im-other.Im)
  
  def __mul__(self,other):
    return Complex(self.Re*other.Re-self.Im*other.Im, self.Im*other.Re+self.Re*other.Im)
  
  def __truediv__(self,other):
    BDash = math.pow(other.Re,2) + math.pow(other.Im,2)
    ADash = self * Complex(other.Re, -1*other.Im)
    return Complex(ADash.Re/BDash, ADash.Im/BDash)
  
  def __pow__(self,other:float):
    base = Cart2Polar(base[0],base[1])
    return Polar2Cart(math.pow(base[0],power),base[1]*power)


a = Complex(1,1)
b = Complex(2,0)

print(a/b)