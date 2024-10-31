import time_capsule_handler.main as tch
#import testPlaypygame.twoDshizz as tpg
import random_functions.main as rf
#import ultimate_tick_tack_toe.game as uttt

path = "/media/hans/Torens_Time_Capsle/TODO"


n = 5
rf.multi_pendulum_simulation(n, [rf.math.pi/((i+1)*2) for i in range(n)], [0 for i in range(n)], [1 for i in range(n)], [1 for i in range(n)],"","simulation",9.81,5,0.01)