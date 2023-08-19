import main as m
import time as t

#timer begin
init = t.time()

pol = [1,1,-1,1]
print("roots for the equation " + m.polyPrint(pol) + " are...")
for i in m.rootsDK(pol):
  
  print(f"{m.compPrint(i)} value of f(x) = {m.compPrint(m.CompPoly(i,pol))}")

#timer stop, print time
print(f"Time: {(t.time()-init)*1000} ms")