import time_capsule_handler.main as tch
#import testPlaypygame.twoDshizz as tpg
import random_functions.main as rf
#import ultimate_tick_tack_toe.game as uttt



n = 0
path = rf.get_all_file_paths("/home/hans/Pictures/photos")
for i in path:
    if rf.get_file_type(i) == "video":
        if rf.convert_video_format(i):
            n+=1
print(f"succesfull: {n}/{len(path)}")