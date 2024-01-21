import math

class Complex():
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
    return self

  def __init__(self,real:float,imaginary:float):
    self.Re = real
    self.Im = imaginary
    self.rTheta()

  def __str__(self):
    self.rTheta
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
      return Complex(self.Re+other.Re,self.Im+other.Im).rTheta()
    else:
      return Complex(self.Re+other,self.Im).rTheta()

  def __radd__(self,other):
    return Complex(self.Re+other,self.Im).rTheta()

  def __sub__(self,other):
    if type(other) == Complex:
      return Complex(self.Re-other.Re,self.Im-other.Im).rTheta()
    else:
      return Complex(self.Re-other,self.Im).rTheta()

  def __rsub__(self,other):
    return Complex(-1*(self.Re-other),-1*(self.Im)).rTheta()

  def __mul__(self,other):
    if type(other) == Complex:
      return Complex(self.Re*other.Re-self.Im*other.Im, self.Im*other.Re+self.Re*other.Im).rTheta()
    else:
      return Complex(self.Re*other,self.Im*other).rTheta()

  def __rmul__(self,other):
    return Complex(self.Re*other,self.Im*other).rTheta()

  def __truediv__(self,other):
    if type(other) == Complex:
      BDash = math.pow(other.Re,2) + math.pow(other.Im,2)
      ADash = self * Complex(other.Re, -1*other.Im)
      return Complex(ADash.Re/BDash, ADash.Im/BDash).rTheta()
    else:
      return Complex(self.Re/other,self.Im/other).rTheta()
  
  def __rtruediv__(self,other):
    BDash = math.pow(self.Re,2) + math.pow(self.Im,2)
    ADash = other * Complex(self.Re, -1*self.Im)
    return Complex(ADash.Re/BDash, ADash.Im/BDash).rTheta()

  def __pow__(self,other):
    if type(other) == Complex:
      x = (self.r**other.Im)*(math.e**(other.Re*self.theta))
      y = (self.r**other.Re)*(math.e**(-1*self.theta*other.Im))
      return Complex(y*math.cos(math.log(x)),y*math.sin(math.log(x))).rTheta()
    else:
      r = self.r**other
      theta = self.theta*other
      return Complex(r*math.cos(theta),r*math.sin(theta)).rTheta()

  def __rpow__(self,other):
    return (Complex(other,0)**self).rTheta()
  
  def __floordiv__(self,other):
    ans = self/other
    return Complex(math.floor(ans.Re),math.floor(ans.Im)).rTheta()
  
  def __rfloordiv__(self,other):
    ans = self/other
    return Complex(math.floor(ans.Re),math.floor(ans.Im)).rTheta()
  
  def __mod__(self,other):
    pass

class Poly():
  def __init__(self,*arg):
    p = [arg]

b = Complex(5,2)

b.Re = 3
print(b.Re)

complex(1,1)