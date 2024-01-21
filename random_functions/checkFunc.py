import main as m
import time as t

#timer begin
init = t.time()

pol = [[1,1],[1,0],[-1,5],[1,3]]
print(m.polyPrint(pol))

#timer stop, print time
print(f"Time: {(t.time()-init)*1000} ms")