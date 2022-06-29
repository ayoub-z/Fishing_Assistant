import cv2 as cv
from window_capture import WindowCapture

class Vision:

    # properties
    bobber_img = None
    bobber_w = 0
    bobber_h = 0
    method = None
    recorded_confidences = []

    def __init__(self, bobber_img_path, method=cv.TM_CCOEFF_NORMED):
        # load the image we're trying to match
        # https://docs.opencv.org/4.2.0/d4/da8/group__imgcodecs.html
        self.bobber_img = cv.imread(bobber_img_path, cv.IMREAD_UNCHANGED)
        self.bobber_img = self.bobber_img[...,:3]

        # save the dimensions of the bobber image
        self.bobber_w = self.bobber_img.shape[1]
        self.bobber_h = self.bobber_img.shape[0]

        # 6 methods to choose from:
        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        # TM_CCOEFF_NORMED works very well, so that is what we'll use.
        self.method = method
 
    def display_image(self, fish_bot, threshold, size_percentage, cropped_image, max_val, max_loc, window_name):
        '''
        This function is purely to display the bot's vision, for debugging purposes.
        A smaller window pops up displaying what the bot can see.
        '''
        if max_val >= threshold: # if the fishing bobber is detected
            x, y = max_loc 

            # determine the center position of the rectangle around the fishing bobber          
            center_x = x + int(self.bobber_w/2)
            center_y = y + int(self.bobber_h/2)

            output_image = self.draw_rectangle(cropped_image, (center_x, center_y)) # draw rectangle around the bobber
            if size_percentage != 100: # if we want to resize the displayed image
                output_image = self.resize_image(output_image, size_percentage) # resize it
            cv.imshow(window_name, output_image) # display the result
            cv.setWindowProperty(window_name, cv.WND_PROP_TOPMOST, 1)
            if cv.waitKey(1) == ord('q'): 
                cv.destroyAllWindows()
                fish_bot.fishing = False
                print('done')
                quit()
        else: # if no bobber is detected
            if size_percentage != 100:
                cropped_image = self.resize_image(cropped_image, size_percentage)
            cv.imshow(window_name, cropped_image) # display the normal image
            cv.setWindowProperty(window_name, cv.WND_PROP_TOPMOST, 1)
            if cv.waitKey(1) == ord('q'): 
                cv.destroyAllWindows()
                fish_bot.fishing = False
                print('done')
                quit()

    def find(self, fish_bot, window_name, threshold, size_percentage=100, find_enemy=False, debug_mode=False, calculate_best_threshold=False):
        win_to_capture = WindowCapture('World of Warcraft')
        w = win_to_capture.w # window height
        h = win_to_capture.h # window width
        screenshot = win_to_capture.get_screenshot()

        # we want the middle square of the window, not the full window. since that's where the fishing bobber will be
        # and since it's better for performance to not analyse the entire window.   
        # The middle box area starts after around a 6th of the window's height, all the way down to the middle of the window. 
        # the width starts after around a 6th of the window's width and is all the way till 5/6th of the entire width

        # for the screenshot's height/width positions, we won't be using exact numbers, but an estimation
        # by calculating the estimated area. this allows for the program to run on any resolution screen.
        #                        startpoint h : endpoint h,   startpoint w : endpoint w
        cropped_image = screenshot[int(h / 6) : int(h - h / 2), int(w / 6) : int(w - w / 6)]

        # the cropped image would be the square box of the full window, as shown below
        # make sure the fishing bobber is within that area
        #  ________________________________
        # |     ______________________     |
        # |    |     Fishing area     |    |
        # |    |______________________|    |
        # |                                |
        # |          Full window           |
        # |________________________________|

        # for the enemy frame detection it's not possible to calculate it. 
        # thus we'll be using exact coordinates that are manually found.
        if find_enemy:
            # Calibrated for a 2560/1440 resolution screen
            # cropped_image = screenshot[182:220, 561:600]
            # Calibrated for a 1920/1080 resolution screen
            cropped_image = screenshot[143:180, 423:460]

        # This is an example of where the enemy frame would be for our specific in-game UI
        #  ________________________________
        # |         ___                    |
        # |        |___|                   |
        # |        #Enemy frame            |
        # |                                |
        # |                                |
        # |________________________________|

        result = cv.matchTemplate(cropped_image, self.bobber_img, self.method)
        # get the best match position
        _, max_val, _, max_loc = cv.minMaxLoc(result)
        if debug_mode:
            self.display_image(fish_bot, threshold, size_percentage, cropped_image, max_val, max_loc, window_name)

        if calculate_best_threshold:
            self.recorded_confidences.append(max_val)
            if len(self.recorded_confidences) > 25:
                print(f"Recommended threshold: {round(max(self.recorded_confidences) + 0.03, 2)}")
                fish_bot.fishing = False

        # if confidence of how likely we've detected bobber, is higher than the threshold,
        # it means we've found the bobber!
        if max_val >= threshold: 
            x, y = max_loc # x,y coordinates of where bobber is found

            # determine the center position.
            # add half of the bobber's width/height, to get the very center position.
            # we also add a 6th of the window's width/height to get the actual position inside the window
            center_x = x + int(self.bobber_w/2) + (w/6) 
            center_y = y + int(self.bobber_h/2) + (h/6)
            return ((center_x, center_y), max_val, cropped_image)

    def find_enemy(self, fish_bot, threshold=0.5, size_percentage=100, find_enemy=True, debug_mode=False):
        find_enemy = self.find(fish_bot, 'enemy_detector', threshold, size_percentage, find_enemy, debug_mode)
        if find_enemy != None:
            cv.destroyAllWindows()
            print("ENEMY SPOTTED")
            fish_bot.fishing = False
            fish_bot.escape_feature()
            quit()

    def draw_rectangle(self, haystack_img, rectangle):
        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        top_left = (rectangle[0] - int(self.bobber_w/2), rectangle[1] - int(self.bobber_h/2))
        bottom_right = (top_left[0] + self.bobber_w, top_left[1] + self.bobber_h)

        # draw the box around the found object
        cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, 
                    lineType=line_type, thickness=2)
        return haystack_img

    def resize_image(self, image, size_percentage):
        # size_percentage is percent of original size

        width = int(image.shape[1] * size_percentage / 100)
        height = int(image.shape[0] * size_percentage / 100)
        dim = (width, height)

        # resize image
        image = cv.resize(image, dim, interpolation = cv.INTER_AREA)
        return image