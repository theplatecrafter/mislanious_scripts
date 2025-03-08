import time_capsule_handler.main as tch
#import testPlaypygame.twoDshizz as tpg
import random_functions.main as rf
#import ultimate_tick_tack_toe.game as uttt

import numpy as np


rf.double_pendulum_chaos_grid((np.pi/3,np.pi/12*5),(np.pi/3,np.pi/12*5),60,[2],"outputs","DP_grid",printDeets=True,sim_height=50,sim_width=50)