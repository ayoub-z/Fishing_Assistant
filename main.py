from bot import FishBot
from vision import Vision
from window_capture import WindowCapture

from time import sleep
from threading import Thread
import cv2 as cv

def countdown():
    print("Fish bot starting in:")
    for i in reversed(range(1,4)):
        print(f"{i}..")
        sleep(1)

def start_bot(threshold, bobber):
    # enemy_frame = 'images/Enemy_frame.png'
    # addon_error = 'images/Addon_error.png'

    vision_bobber = Vision(bobber)
    # vision_enemy = Vision(enemy_frame)
    # vision_error = Vision(addon_error)

    countdown() # 3,2,1 countdown before starting
    fish_bot = FishBot()
    
    t1 = Thread(target=fish_bot.start_fishing, args=(vision_bobber, threshold))
    t1.start()   

if __name__ == "__main__":
    start_bot(threshold=0.6, bobber='images/grizzly_hills_east.png')