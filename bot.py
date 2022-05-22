import cv2 as cv
import pyautogui
from window_capture import WindowCapture
from vision import Vision

import random
from time import time, sleep

class FishBot:
    fishing = True

    def detect_bobber(self, threshold, vision, screenshot, debug_mode=False):
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
        bobber_data = vision.find(screenshot, threshold, debug_mode)
        if debug_mode:
            if bobber_data != None: # if target is located inside screenshot
                # draw green rectangle inside screenshot and display it
                output_image = vision.draw_rectangle(screenshot, bobber_data[0])
                cv.imshow('Fish_bot', output_image)
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
        return bobber_data

    def cast_fishing_rod(self, key):
        self.press_key('1') # '1' here indicates the button to be pressed to cast the rod
        sleep(0.25) # wait for bobber to be in water, before we 1try to detect it

    def detect_error(self, vision, screenshot):
        position = vision.find(screenshot, 0.6)

        if position != None: # if target is located inside screenshot
            print("Removing annoying addon error")
            self.press_key('esc')       

    def detect_enemy(self, vision, screenshot):
        position = vision.find(screenshot, 0.6)

        if position != None: # if target is located inside screenshot
            output_image = vision.draw_rectangle(screenshot, position[0])
            cv.imshow('Fish_bot', output_image)
            if cv.waitKey(1) == ord('q'): 
                cv.destroyAllWindows()
                print('done')
                quit()        
            print("ENEMY SPOTTED!!!")
            sleep(0.05)
            self.emergency_escape() # escape
            self.shut_down() # shut down program  
        else: # if target isn't located, display the normal screenshot
            cv.imshow('Fish_bot', screenshot)
            if cv.waitKey(1) == ord('q'): 
                cv.destroyAllWindows()
                print('done')
                quit()

    def press_key(self, key_to_press):
        pyautogui.press(key_to_press)            

    def apply_lure(self, key, lure_end_time=time()-600):
        if time() >= lure_end_time:
            sleep(0.1)
            self.press_key(key)
            print("Applying fishing lure")
            sleep(2.3)
            return True
        else:
            return False

    def fish_caught(self, confidence, last_confidences):
        '''
        When fish is caught, the bobber dips. 
        When bobber dips, we either completely don't recognize it anymore or the confidence drops.
        So we check for a confidence of None or 
        a confidence that's quite a bit lower compared to the previous ones.
        '''
        if confidence == None: # if we can't locate the bobber anymore
            print("Bobber below detect threshold")
            return True

        # if we have checked at least one screenshot before
        if len(last_confidences) >= 5:
            confidence_threshold = (sum(last_confidences[-5:-2]) / len(last_confidences[-5:-2]) * 0.90) # 90% of the avg of the previous confidences
            if confidence <= confidence_threshold:
                # print("confidence dropped from the average", (round((sum(last_confidences[-5:-2]) / len(last_confidences[-5:-2])),2 )),
                #     "to:", (round(confidence, 2)))            
                return True
        elif len(last_confidences) >= 3:
            confidence_threshold = (sum(last_confidences[-3:-1]) / len(last_confidences) * 0.90) # 90% of the avg of the previous confidences
            if confidence <= confidence_threshold:
                # print("confidence dropped from the average", (round((sum(last_confidences[-3:-1]) / len(last_confidences[-3:-1])),2 )),
                #     "to:", (round(confidence, 2)))            
                return True
        elif len(last_confidences) >= 1:        
            confidence_threshold = (sum(last_confidences) / len(last_confidences) * 0.90) # 90% of the avg of the previous confidences
            # if the current confidence is lower than the avg of the last confidences
            # i.e. avg confidence is 0.8, threshold (90%) becomes 0.72, but the confidence is actually 0.7
            # then that means the bobber dipped into the water and we most likely caught a fish
            if confidence <= confidence_threshold:
                # print("confidence dropped from the average", (round((sum(last_confidences) / len(last_confidences)),2 )),
                #     "to:", (round(confidence, 2)))
                return True

    def reel_in_fish(self, last_pos):
        try:
            # last_pos contains the x and y coordinates of the bobber
            # we subtract 15 pixels from the x and add 20 pixel to the y position,
            # in order to get the center of the bobber for our mouse to click on
            pyautogui.moveTo((last_pos[0] - 15), (last_pos[1] + 30), duration=random.uniform(0.3, 0.5), tween=pyautogui.easeInOutQuad)
            pyautogui.click(button= "right")
        except: # in case the coordinates are None
            pass

    def emergency_escape(self):
        '''
        Presses keypresses to activate certain abilities that allow the
        character to fly away.
        '''
        print("Activating EMERGENCY ESCAPE")
        self.press_key('f6') # presses the 'F6' key to turn character invisible
        sleep(0.1)
        self.press_key('f6') # second press allows character to fly
        sleep(0.1)

        pyautogui.keyDown("space") # hold down the 'space' to fly up for x seconds
        sleep(random.uniform(5, 8)) 
        pyautogui.keyUp("space")

        pyautogui.keyDown("d") # hold down the 'd' turn right for x amount of time
        sleep(random.uniform(0.3, 1)) 
        pyautogui.keyUp("d")

        pyautogui.keyDown("w") # hold down the 'w' key to fly forward for x amount of time
        sleep(random.uniform(5, 8)) 
        pyautogui.keyUp("w")     

    def shut_down(self):      
        cv.destroyAllWindows()
        print("Shutting down...")
        quit()   

    def start_fishing(self, vision_bobber, threshold):
        stop_program = False
        previous_confidences = []
        last_position = None

        failed_casts = 0
        fish_count = 0
        fishing_lure = True
        lure_duration = 600 # seconds
        lure_end_time = time() 

        win_to_capture = WindowCapture('World of Warcraft')
        while(self.fishing):
                # small pauze before we start/after we caught fish
                sleep(random.uniform(0.3, 1)) 
                first_cast = True           

                # if apply_lure('2', lure_end_time):
                #     lure_end_time += lure_duration
                self.cast_fishing_rod('1')

                print('Line is out, waiting for fish to bite..')
                animation = "|/-\\" # loading animation 
                idx = 0
                while(self.fishing):
                    screenshot = win_to_capture.get_screenshot()
                    data_bobber = self.detect_bobber(threshold, vision_bobber, screenshot)

                    print(animation[idx % len(animation)], end="\r") # print a loading animation
                    idx += 1     

                    if data_bobber != None: # if we can locate the bobber's
                        position, confidence = data_bobber 
                    else:
                        position, confidence = (None, None)
                        if first_cast == True: # if on the very first cast we were unable to locate the bobber
                            print("UH OH!!!. We can't locate the bobber :( \n\nTrying again..\n\n")
                            break

                    print(animation[idx % len(animation)], end="\r") # print a loading animation
                    idx += 1     

                    # confidence = vision_bobber.bobber_confidence
                    # position = vision_bobber.bobber_position


                    # if on the very first cast we were unable to locate the bobber
                    if confidence == None and first_cast == True:
                        print("UH OH!!!. We can't locate the bobber :( \n\nTrying again..\n\n")
                        break

                    first_cast = False
                    if self.fish_caught(confidence, previous_confidences):
                        previous_confidences = []
                        break
                    last_position = position
                    previous_confidences.append(confidence)
        
                if failed_casts >= 10: # if we were unable to detect a bobber 10 times in a row
                    print("Unable to detect bobber after 10 consecutive tries")
                    self.shut_down() # shut down the program
                    
                if first_cast == True: # a "failed cast", meaning we didn't detect bobber, only applies if it's the very first cast
                    failed_casts += 1
                    continue    

                fish_count += 1
                self.reel_in_fish(last_position)
                print(f"Fish on hook! \nFish caught so far: {fish_count}\n")

                last_position = None
                failed_casts = 0