import time_capsule_handler.main as tch
#import testPlaypygame.twoDshizz as tpg
import random_functions.main as rf
#import ultimate_tick_tack_toe.game as uttt

path = "/media/hans/Torens_Time_Capsle/TODO"




rf.double_pendulum_simulation(
    screen_size=5,
    theta1_range=[rf.math.pi, -1 * rf.math.pi],
    theta2_range=[rf.math.pi, -1 * rf.math.pi]
)