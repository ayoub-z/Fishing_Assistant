from bot import FishBot
from vision import Vision

from time import sleep
from threading import Thread

def countdown():
    print("Fish bot starting in:")
    for i in reversed(range(1,4)):
        print(f"{i}..")
        sleep(1)

def detect_objects(vision_bobber, vision_enemy, fish_bot, threshold, escape_feature, calculate_best_threshold=False, size_percentage=50):
    while(fish_bot.fishing):
        vision_bobber.find(fish_bot, 'live feed', threshold, size_percentage, debug_mode=True, calculate_best_threshold=calculate_best_threshold)
        if escape_feature:
            vision_enemy.find_enemy(fish_bot, threshold=0.95, size_percentage=100, debug_mode=False)

def activate_bot(bobber_image, enemy_frame_image, threshold, bobber_movement_sensitivty,
                 escape_feature, runtime, apply_lure, live_feed, calculate_best_threshold):
    '''
    The main function that activates the bot.
    threshold: the threshold of how much the found object needs to match the template object
    bobber_image: a cropped image file showing just the fishing bobber
    live_feed: a boolean on whether to display the bot's vision
    '''

    # initialize the vision classes with the image they need to find
    vision_bobber = Vision(bobber_image) 
    vision_enemy = Vision(enemy_frame_image)

    countdown() # 3,2,1 sec countdown before starting

    # initialize the bot
    fish_bot = FishBot()

    if not calculate_best_threshold:
        # create a separate thread for the bot's fishing proces
        t1 = Thread(target=fish_bot.start_fishing, args=(threshold, vision_bobber, bobber_movement_sensitivty, runtime, apply_lure))
        t1.start()

    # displays a live feed of what the bot sees. (runs on the main thread)
    if live_feed:
        detect_objects(vision_bobber, vision_enemy, fish_bot, threshold, escape_feature, 
                       calculate_best_threshold, size_percentage=50)

if __name__ == "__main__":
    bobber_image = 'images/tiny_wg.png'
    enemy_frame_image = 'images/enemy_frame.png' # the enemy frame we're looking for on screen    

    # this is the sensitivty for detecting bobber movement. 
    # the higher it is, the less bobber movement is required to assume that we've caught a fish.
    # it is recommended to keep this at 0.85
    bobber_movement_sensitivty = 0.85
    threshold = 0.4 # threshold of how accurately the detected bobber needs to resemble the bobber_image template    
    runtime = 20 # bot runtime in minutes

    escape_feature = True # allows the bot to detect and escape from enemies
    apply_lure = True
    live_feed = True # shows the live feed of what the bot can see

    # setting this to TRUE pauses the entire bot. 
    # the game will be monitored and the best threshold will be recommended. 
    # the threshold should generally be between 0.4 and 0.8
    calculate_best_threshold = False 

    activate_bot(bobber_image, enemy_frame_image, threshold, bobber_movement_sensitivty,
                 escape_feature, runtime, apply_lure, live_feed, calculate_best_threshold)