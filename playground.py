import time_capsule_handler.main as tch
#import testPlaypygame.twoDshizz as tpg
import random_functions.main as rf
#import ultimate_tick_tack_toe.game as uttt


#tch.time_capsule_handler("/media/hans/Torens_Time_Capsle")
#exit()

n = 0
path = "/media/hans/Torens_Time_Capsle/7) 2024/other"


paths = [i for i in rf.get_all_file_paths(path) if rf.get_file_type(i) == "video"]
for i in paths:
    if rf.convert_video_format(i):
        n+=1
print(f"succesfull: {n}/{len(paths)}")
