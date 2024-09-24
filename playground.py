import time_capsule_handler.main as tch
#import testPlaypygame.twoDshizz as tpg
import random_functions.main as rf
#import ultimate_tick_tack_toe.game as uttt


tch.time_capsule_handler("/media/hans/Torens_Time_Capsle")
exit()

n = 0
path = [i for i in rf.get_all_file_paths("/home/hans/Pictures/photos") if rf.get_file_type(i) == "video"]
for i in path:
    if rf.convert_video_format(i):
        n+=1
print(f"succesfull: {n}/{len(path)}")
