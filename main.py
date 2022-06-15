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

def detect_objects(vision_bobber, vision_enemy, fish_bot, threshold, size_percentage=100):
    while(fish_bot.fishing):
        vision_bobber.find(fish_bot, 'live feed', threshold, size_percentage, debug_mode=True)
        vision_enemy.find_enemy(fish_bot, threshold=0.9, size_percentage=100, debug_mode=False)

def start_bot(threshold, bobber, live_feed):
    enemy_frame = 'images/Enemy_frame.png'

    vision_bobber = Vision(bobber)
    vision_enemy = Vision(enemy_frame)

    countdown() # 3,2,1 countdown before starting
    fish_bot = FishBot()
    
    t1 = Thread(target=fish_bot.start_fishing, args=(threshold, vision_bobber, False))
    t1.start()

    if live_feed:
        detect_objects(vision_bobber, vision_enemy, fish_bot, threshold, 50)

if __name__ == "__main__":
    start_bot(threshold=0.55, bobber='images/wintergrasp_evening4.png', live_feed=True)