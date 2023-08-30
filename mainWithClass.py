import math

class Complex():
  def __init__(self,real:float,imaginary:float):
    self.Re = real
    self.Im = imaginary
    self.r = math.sqrt(pow(real,2)+pow(imaginary,2))
    if imaginary != 0:
      if imaginary > 0:
          self.theta =  math.acos(real/(math.sqrt(pow(real,2)+pow(imaginary,2))))
      else:
        self.theta =  2*math.pi-math.acos(real/(math.sqrt(pow(real,2)+pow(imaginary,2))))
    else:
      self.theta = 0
    self.thetaDEG = math.degrees(self.theta)

  def rTheta(self):
    self.r = math.sqrt(pow(self.Re,2)+pow(self.Im,2))
    if self.Im != 0:
      if self.Im > 0:
          self.theta =  math.acos(self.Re/(math.sqrt(pow(self.Re,2)+pow(self.Im,2))))
      else:
        self.theta =  2*math.pi-math.acos(self.Re/(math.sqrt(pow(self.Re,2)+pow(self.Im,2))))
    else:
      self.theta = 0
    self.thetaDEG = math.degrees(self.theta)

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
    if type(other) == Complex:
      return Complex(self.Re+other.Re,self.Im+other.Im)
    else:
      return Complex(self.Re+other,self.Im)
    

  def __radd__(self,other):
    return Complex(self.Re+other,self.Im)

  def __sub__(self,other):
    if type(other) == Complex:
      return Complex(self.Re-other.Re,self.Im-other.Im)
    else:
      return Complex(self.Re-other,self.Im)

  def __rsub__(self,other):
    return Complex(-1*(self.Re-other),-1*(self.Im))
  

  def __mul__(self,other):
    if type(other) == Complex:
      return Complex(self.Re*other.Re-self.Im*other.Im, self.Im*other.Re+self.Re*other.Im)
    else:
      return Complex(self.Re*other,self.Im*other)
  
  def __rmul__(self,other):
    return Complex(self.Re*other,self.Im*other)

  def __truediv__(self,other):
    if type(other) == Complex:
      BDash = math.pow(other.Re,2) + math.pow(other.Im,2)
      ADash = self * Complex(other.Re, -1*other.Im)
      return Complex(ADash.Re/BDash, ADash.Im/BDash)
    else:
      return Complex(self.Re/other,self.Im/other)
  
  def __rtruediv__(self,other):
    BDash = math.pow(self.Re,2) + math.pow(self.Im,2)
    ADash = other * Complex(self.Re, -1*self.Im)
    return Complex(ADash.Re/BDash, ADash.Im/BDash)
  
  def __pow__(self,other):
    if type(other) == Complex:
      x = (self.r**other.Im)*(math.e**(other.Re*self.theta))
      y = (self.r**other.Re)*(math.e**(-1*self.theta*other.Im))
      return Complex(y*math.cos(math.log(x)),y*math.sin(math.log(x)))
    else:
      r = self.r**other
      theta = self.theta*other
      return Complex(r*math.cos(theta),r*math.sin(theta))
    
  def __rpow__(self,other):
    return Complex(other,0)**self
  
  def __floordiv__(self,other):
    ans = self/other
    return Complex(math.floor(ans.Re),math.floor(ans.Im))
  
  def __rfloordiv__(self,other):
    ans = self/other
    return Complex(math.floor(ans.Re),math.floor(ans.Im))
  
  def __mod__(self,other):
    pass



a = 3
b = Complex(5,45)

print(a//b)