import time_capsule_handler.main as tch
#import testPlaypygame.twoDshizz as tpg
import random_functions.main as rf
#import ultimate_tick_tack_toe.game as uttt

path = "/media/hans/Torens_Time_Capsle/TODO"


print(rf.count_elements([rf.get_image_metadata(i)["Camera Model"] for i in [j for j in rf.get_all_file_paths(path) if rf.get_file_type(j) == "image"]]))

exit()

for file in [i for i in rf.getRandomFiles(rf.get_all_file_paths(path),"image",100) if rf.get_image_metadata(i)["Camera Model"] != "NIKON D90"]:
    rf.open_on_web(file)

exit()

tch.time_capsule_handler("/media/hans/Torens_Time_Capsle")
exit()