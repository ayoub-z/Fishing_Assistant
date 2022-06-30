class Algorithm:

    def fish_on_line(confidence, last_confidences, bobber_movement_sensitivity):
        '''
        The algorithm that detects whether fish has been caught.
        When fish is caught, the bobber dips in the water. 
        When it dips, the confidence drops by a bit or is completely below the threshold.
        If we it's below threshold, we can't detect it. That's one way of concluding we have fish.
        The second way is to compare the current confidence with the past confidences, to look
        for an irregular big dip in the confidence.
        '''
        
        # if we can't locate the bobber anymore, then it most likely dipped in the water and we caught a fish
        if confidence == None: 
            return True
        
        # In these if statements, the average of the past confidences is calculated
        # If the current recorded confidence has dropped by more than 15% of the average confidence,
        # then that means the bobber most likely has dipped in the water.       
        if len(last_confidences) >= 1:
            n = len(last_confidences)
            n = 5 if n > 5 else n # we don't want more than 5 of the past confidences

            confidence_threshold = (sum(last_confidences[-n:]) / n) * bobber_movement_sensitivity 

            if confidence <= confidence_threshold:          
                return True