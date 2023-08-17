import main as m
import time as t

#timer begin
init = t.time()

print(m.Cart2Polar(1,1,"DEG"))

#timer stop, print time
print(f"Time: {(t.time()-init)*1000} ms")