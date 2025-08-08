import time_capsule_handler.main as tch
#import testPlaypygame.twoDshizz as tpg
import random_functions.main as rf
#import ultimate_tick_tack_toe.game as uttt

import numpy as np


<<<<<<< HEAD
#tch.time_capsule_handler("/mnt/f")

=======

parent_dir = "/mnt/f/0) Other/3) Other Shortcuts/Family pics"

lnks = [i for i in rf.get_all_file_paths(parent_dir) if rf.os.path.splitext(i)[1] == ".lnk"]
for lnk in lnks:
    rf.lnkToRelativeShortcut(lnk,False)
>>>>>>> 3613ca8ba1bf07f346e1767bc28e943db39d1152
