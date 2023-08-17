import main as m
import time as t

#timer begin
init = t.time()

print(m.root(1,4))

#timer stop, print time
print(f"Time: {(t.time()-init)*1000} ms")