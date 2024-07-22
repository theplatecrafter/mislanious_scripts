import time_capsule_handler.main as tch
#import testPlaypygame.twoDshizz as tpg
import random_functions.main as rf
#import ultimate_tick_tack_toe.game as uttt

file_list = rf.getRandomFiles([
    tch.TimeCapsulePWDLinux["other"]
],["image","video","audio"],10)

for i in file_list:
    rf.open_on_web(i)
