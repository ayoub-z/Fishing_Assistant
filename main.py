import cv2 as cv
import numpy as np
import os
from time import time, sleep
from window_capture import WindowCapture
from vision import Vision
import pyautogui
import random

def draw_rectangle(threshold):
    '''
    FUNCTION:
    This function takes a screenshot of the main window, then tries 
    to find your target (fishing bobber in this case) inside that screen shot.
    Finally it draws a green rectangle around that bobber and returns
    the exact position of where the bobber was found.

    PARAMETER:
    parameter is the confidence threshold of how strict we want 
    the found object to be similar to our target.
    if you put 0.99, you basically want an exact copy of your target,
    and a 0.3 means it only needs to resemble it around 30%. 
    you don't want it too low, otherwise it will recognize other 
    areas of the window as the target.
    0.67 worked for me.
    '''
    screenshot = win_to_capture.get_screenshot()
    position = vision_bobber.find(screenshot, threshold, 'rectangles')

    if position != None: # if target is located inside screenshot
        # draw green rectangle inside screenshot and display it
        output_image = vision_bobber.draw_rectangle(screenshot, position[0])
        cv.imshow('Fish_bot', screenshot)
        if cv.waitKey(1) == ord('q'): 
            cv.destroyAllWindows()
            print('done')
            quit()
    else: # if target isn't located, display the normal screenshot
        cv.imshow('Fish_bot', screenshot)
        if cv.waitKey(1) == ord('q'): 
            cv.destroyAllWindows()
            print('done')
            quit()
    return position
        
def cast_rod(key_to_press):
    pyautogui.press(key_to_press)            

def fish_caught(confidence, last_confidences):
    '''
    When fish is caught, the bobber dips. 
    When bobber dips, we either completely don't recognize it anymore or the confidence drops.
    So we check for a confidence of None or 
    a confidence that's quite a bit lower compared to the previous ones.
    '''
    if confidence == None: # if we can't locate the bobber anymore
        return True

    # if we have checked at least one screenshot before
    if len(last_confidences) >= 1:
        confidence_threshold = (sum(last_confidences) / len(last_confidences) * 0.9) # 90% of the avg of the previous confidences

        # if the current confidence is lower than the avg of the last confidences
        # i.e. avg confidence is 0.8, threshold (90%) becomes 0.72, but the confidence is actually 0.7
        # then that means the bobber dipped into the water and we most likely caught a fish
        if confidence < confidence_threshold:
            # print("confidence dropped from the average", (round((sum(last_confidences) / len(last_confidences)),2 )),
            #     "to:", (round(confidence, 2)))
            return True

def reel_in_fish(last_pos):
    try:
        # last_pos contains the x and y coordinates of the bobber
        # we subtract 15 pixels from the x and add 20 pixel to the y position,
        # in order to get the center of the bobber for our mouse to click on
        pyautogui.moveTo((last_pos[0] - 15), (last_pos[1] + 20), duration=random.uniform(0.3, 0.5), tween=pyautogui.easeInOutQuad)
        pyautogui.click(button= "right")
    except: # in case the coordinates are None
        pass

bobber = 'images/bobber_dragonblight.png'

win_to_capture = WindowCapture('World of Warcraft')
vision_bobber = Vision(bobber)

# default threshold
threshold = 0.6

# if bobber == 'images/bobber_dragonblight.png':
#     threshold = 0.7
if bobber == 'images/grizzly_hills_east.png':
    threshold = 0.621
if bobber == 'images/bobber_stormwind.png':
    threshold = 0.64   



fish_count = 0
previous_confidences = []
last_position = None
print("Threshold: ", threshold)
while(True):
    # sleep for a bit to have time to cast out fishing line
    # and sleep at the start before every cast to let old fishing bobber disappear. 
    # with some randomness to show some human like behavior
    # sleep(random.uniform(3, 4.5)) 
    sleep(random.uniform(0.3, 1)) 

    cast_rod('1') # '1' here indicates the button to be pressed to cast the rod
    sleep((0.25)) # wait for bobber to be in water, before we 1try to detect it

    print('Line is out, waiting for fish to bite..')
    animation = "|/-\\" # loading animation 
    idx = 0
    while(True): # wait until we catch fish
        # draw rectangle around target
        # and return position and confidence of target
        loop_time = time()
        data = draw_rectangle(threshold)
        
        print(animation[idx % len(animation)], end="\r") # print a loading animation
        idx += 1     

        # print('FPS {}'.format(1 / (time() - loop_time)))
        if data != None:
            position, confidence = data
        else:
            position, confidence = (None, None)

        if fish_caught(confidence, previous_confidences):
            previous_confidences = []
            break
        last_position = position
        previous_confidences.append(confidence)

    fish_count += 1
    print(f"Fish on hook! \nFish caught so far: {fish_count}\n")
    reel_in_fish(last_position)
    last_position = None