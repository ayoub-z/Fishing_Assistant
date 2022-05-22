from bot import FishBot
from vision import Vision
from window_capture import WindowCapture

from time import sleep, time
from threading import Thread
import cv2 as cv

import numpy as np

def countdown():
    print("Fish bot starting in:")
    for i in reversed(range(1,4)):
        print(f"{i}..")
        sleep(1)
    
def detect_bobber(vision, threshold, fish_bot, size_percentage=100):
    while(fish_bot.fishing):
        start_time = time() 
        vision.find(size_percentage, threshold, fish_bot, debug_mode=True)

def start_bot(threshold, bobber):
    # enemy_frame = 'images/Enemy_frame.png'
    # addon_error = 'images/Addon_error.png'

    vision_bobber = Vision(bobber)
    vision_bobber2 = Vision(bobber)
    # vision_enemy = Vision(enemy_frame)
    # vision_error = Vision(addon_error)

    # countdown() # 3,2,1 countdown before starting1
    fish_bot = FishBot()
    
    t1 = Thread(target=fish_bot.start_fishing, args=(vision_bobber, threshold))
    t1.start()
    detect_bobber(vision_bobber2, threshold, fish_bot)    

if __name__ == "__main__":
    start_bot(threshold=0.6, bobber='images/wintergrasp.png')