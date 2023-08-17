import main as m
import time as t

#timer begin
init = t.time()

print(m.polyPrint([-123,123,2,-324,32,3]))

#timer stop, print time
print(f"Time: {(t.time()-init)*1000} ms")