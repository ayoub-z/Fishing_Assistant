from bot import FishBot
from vision import Vision

from time import sleep
from threading import Thread

def countdown():
    print("Fish bot starting in:")
    for i in reversed(range(1,4)):
        print(f"{i}..")
        sleep(1)

def detect_objects(vision_bobber, vision_enemy, fish_bot, threshold, size_percentage=100):
    while(fish_bot.fishing):
        vision_bobber.find(fish_bot, 'live feed', threshold, size_percentage, debug_mode=True)
        vision_enemy.find_enemy(fish_bot, threshold=0.95, size_percentage=100, debug_mode=False)

def activate_bot(threshold, bobber_image, enemy_frame_image, live_feed):
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

    # create a separate thread for the bot's fishing proces
    t1 = Thread(target=fish_bot.start_fishing, args=(threshold, vision_bobber))
    t1.start()

    # displays a live feed of what the bot sees. (runs on the main thread)
    if live_feed:
        detect_objects(vision_bobber, vision_enemy, fish_bot, threshold, 50)

if __name__ == "__main__":
    bobber_image = 'images/tiny_wg.png'
    enemy_frame_image = 'images/enemy_frame.png' # the enemy frame we're looking for on screen    
    threshold = 0.55
    live_feed = True

    # Setting this to TRUE will pauze the entire bot. 
    # The game will be monitored and the highest confidences will be printed out in the terminal.
    calculate_threshold = False 

    activate_bot(threshold, bobber_image, enemy_frame_image, live_feed)