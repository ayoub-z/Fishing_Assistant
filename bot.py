import pyautogui

import random
from time import time, sleep

class FishBot:
    fishing = True
    fishing_lure = True
    caught_fish = False
    last_position = None
    previous_confidences = []
    
    fish_count = 0
    failed_casts = 0
    failed_casts_limit = 10
    lure_duration = 600 # seconds
    lure_end_time = time()

    bobber_movement_sensitivity = 0.85

    def detect_bobber(self, threshold, vision, debug_mode):
        bobber_data = vision.find(self, 'fisher', threshold, size_percentage=100, debug_mode=debug_mode)       
        return bobber_data

    def cast_fishing_rod(self, key):
        if self.fishing == True:
            self.press_key('1') # '1' here indicates the button to be pressed to cast the rod
            print('Line is out, waiting for fish to bite..')

    def press_key(self, key_to_press):
        pyautogui.press(key_to_press)            

    def apply_lure(self, key):
        '''
        Applies fishing lure if the lure duration ended.
        This is done with a simple key press'''
        if time() >= self.lure_end_time:
            self.press_key(key)
            print("\nApplying fishing lure\n")
            sleep(2.3)
            
            self.lure_end_time += self.lure_duration
                

    def fish_caught(self, confidence, last_confidences):
        '''
        When fish is caught, the bobber dips or moves around. 
        When it dips, we either don't recognize it anymore or the confidence drops by a few percentages.
        So we check for a confidence of None or 
        a confidence that's quite a bit lower compared to the previous ones.
        '''
        
        # if we can't locate the bobber anymore, then it most likely dipped in the water and we caught a fish
        if confidence == None: 
            return True

        # In these if statements, the past 5, 3, or 1 confidences are summed up and divided by their amount
        # to get the average confidence. If the current recorded confidence is lower than this average confidence
        # multiplied by it's sensitivity (i.e. the threshold), then that means the bobber most likely has moved
        # significantly and we caught a fish.
        if len(last_confidences) >= 5:
            # the confidence_threshold is the average past couple confidences, times the bobber_movement_sensitivty percentage.
            # for example, the avg confidence is 1.0. If sensitivity is 0.85 (85%), then the threshold will be 0.85 * 1 = 0.85
            confidence_threshold = (sum(last_confidences[-5:-2]) / len(last_confidences[-5:-2]) * self.bobber_movement_sensitivity) 
            if confidence <= confidence_threshold:          
                return True

        elif len(last_confidences) >= 3:
            confidence_threshold = (sum(last_confidences[-3:-1]) / len(last_confidences[-3:-1]) * self.bobber_movement_sensitivity)
            if confidence <= confidence_threshold:      
                return True

        elif len(last_confidences) >= 1:        
            confidence_threshold = (sum(last_confidences) / len(last_confidences) * self.bobber_movement_sensitivity)
            if confidence <= confidence_threshold:
                return True

    def reel_in_fish(self):
        '''
        This function is called when a fish is caught and we need to click on the bobber to catch it.
        We use the last recorded position of the bobber as the coordinate to click on.
        '''

        # last_pos contains the last recorded x and y coordinates of the rectangle around the bobber.
        # in order to get the center of the bobber for our mouse to click on, we subtract 15 pixels 
        # from the x and 5 pixel from the y positions
        print(f"Fish on hook!")        
        pyautogui.moveTo((self.last_position[0] - 15), (self.last_position[1] - 5), duration=random.uniform(0.3, 0.5), tween=pyautogui.easeInOutQuad)
        pyautogui.click(button= "right")
        print(f"Fish caught so far: {self.fish_count}\n")

    def escape_feature(self):
        '''
        This function is called when the bot detects it's getting attacked by an enemy.
        Certain keypresses are then pressed to activate a macro that allows the character to fly away.
        A macro is simlpy an ingame feature that allows for a sequence of abilities. In this case,
        it's the ability for the player to turn invisible and the ability for it to turn into a bird.
        Following that we hold down the "space" and "w" keys to fly up and foward.

        '''
        print("Activating EMERGENCY ESCAPE")  
        # presses the 'g' key to turn character invisible and again to turn into flight form
        self.press_key('g')
        sleep(random.uniform(0.02, 0.05))
        self.press_key('g')
        sleep(random.uniform(0.02, 0.05))

        with pyautogui.hold('space'): # hold down 'space' key
            with pyautogui.hold('w'): # hold down 'w' key
                
                # slightly drag the mouse to the left, while holding the right mouse button.
                # this let's the character do a 180 degree turn as it flies away,
                # making it harder for enemy players to keep track of the character
                pyautogui.drag(2, 0, 0.12, button='right') 
                sleep(random.uniform(15, 20)) # sleep the program while it keeps flying away

    def shut_down(self):
        print("Shutting down...")
        self.fishing = False # setting the fishing state to False automatically stops the main while loop

    def wait_for_fish(self, threshold, vision_bobber, debug_mode):
        '''
        When the fishing rod is cast out, keep track of the bobber and wait for it to move.
        '''
        animation = "|/-\\" # loading animation 
        idx = 0
        failed_first_cast = True
        while(self.fishing):
            bobber_data = self.detect_bobber(threshold, vision_bobber, debug_mode)
            position, confidence = (None, None)

            print(animation[idx % len(animation)], end="\r") # print a loading animation
            idx += 1

            if bobber_data != None: # if we can locate the bobber and thus have bobber data
                position, confidence = bobber_data[:2] # save that data to these variables

            # if on the very first detection screenshot we were unable to locate the bobber,
            # it means something went wrong and we need to recast the fishing rod
            elif confidence == None and failed_first_cast == True:
                print("UH OH!!!. We can't locate the bobber :( \n\nTrying again..\n\n")
                break
            failed_first_cast = False

            # if we caught a fish
            if self.fish_caught(confidence, self.previous_confidences):
                self.caught_fish = True
                self.fish_count += 1  
                self.previous_confidences = []              
                break

            # if we didn't catch a fish, update the last position of the bobber and
            # update the "previous_confidences" list
            self.last_position = position
            self.previous_confidences.append(confidence) 

        # a "failed cast", meaning we didn't detect a bobber, 
        # only applies if it's on the very first screenshot after we casted out the fishing rod
        if failed_first_cast == True: 
            self.failed_casts += 1

        # if we were unable to detect a bobber more than x times in a row
        if self.failed_casts >= self.failed_casts_limit:
            print(f"Unable to detect bobber after {self.failed_casts_limit} consecutive tries")   
            self.shut_down() # shut down the bot


    def start_fishing(self, threshold, vision_bobber, bobber_movement_sensitivty, apply_lure, debug_mode=False):
        '''
        The main function that starts and handles the entire fishing proces.
        '''
        self.bobber_movement_sensitivty = bobber_movement_sensitivty

        while(self.fishing):
            # # small pauze before we start/after we caught fish
            sleep(random.uniform(0.3, 2))    
            self.caught_fish = False    
            if apply_lure:
                self.apply_lure('2') # the '2' key here is bound to applying the lure in-game

            self.cast_fishing_rod('1') # and the '1' to casting out the fishing line
            sleep(random.uniform(0.25, 3)) # wait for bobber to drop in water, before we try to detect it

            self.wait_for_fish(threshold, vision_bobber, debug_mode) # wait until a fish is caught
            if self.caught_fish:
                self.reel_in_fish()
                self.last_position = None # reset bobber position
                self.failed_casts = 0 # reset amount of continuous failed casts