import time_capsule_handler.main as tch
#import testPlaypygame.twoDshizz as tpg
import random_functions.main as rf
#import ultimate_tick_tack_toe.game as uttt

path = "/media/hans/Torens_Time_Capsle/TODO"




n = 2
rf.pendulum_simulation(n, [-rf.math.pi/2,-rf.math.pi/2], [0 for i in range(n)], [0.1,1], [1 for i in range(n)],"output","simulation",9.81,50,0.01)