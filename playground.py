import time_capsule_handler.main as tch
#import testPlaypygame.twoDshizz as tpg
import random_functions.main as rf
#import ultimate_tick_tack_toe.game as uttt


media_files = [i for i in rf.get_all_file_paths("/mnt/e/7) 2024/2024-7-14 羽田空港で鬼ごっこ") if rf.get_file_type(i) == "image"]

tch.create_interactive_media_map(media_files, 'my_interactive_media_map.html')