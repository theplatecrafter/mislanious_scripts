import math

class Complex():
  def __init__(self,real:float,imaginary:float):
    self.Re = real
    self.Im = imaginary

  def __str__(self):
    if self.Re == 0:
      if self.Im == -1:
        return "-i"
      elif self.Im == 1:
        return "i"
      elif self.Im == 0:
        return str(self.Im)
      else:
        return str(self.Im) + "i"
    else:
      if self.Im < 0:
        if self.Im == -1:
          return str(self.Re) + "  - i"
        else:
          return str(self.Re) + " - " + str(abs(self.Im)) + "i"
      elif self.Im == 0:
        return str(self.Re)
      else:
        if self.Im == 1:
          return str(self.Re) + " + i"
        else:
          return str(self.Re) + " + " + str(self.Im) + "i"

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
    
    


a = Complex(1,1)
b = Complex(2,0)

print(a/b)