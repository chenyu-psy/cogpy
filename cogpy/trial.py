"""
This function is inspired by jsPsych, in which you can manipulate the presentation of stimuli and collect responses.
"""

from psychopy import core, event
from .layout import stimBoxes
import numpy as np

class trial(object):
    ''' Display stimuli and collect responses

        Args:
            win (object): the window object from psychopy
            stimuli (list): a list of stimuli objects
            resp_type (str, optional): the type of response. Defaults to "key".
            choices (list | object | None, optional): the choices for the response. Defaults to None.
            resp_start (int, optional): the time before the response is allowed. Defaults to 0.
            resp_end_trial (bool, optional): whether the trial ends after the response. Defaults to True.
            duration (float, optional): the maximum duration of the trial. Defaults to float('inf').
            post_trial_gap (float, optional): the time after the trial. Defaults to 0.

        Raises:
            ValueError: The response type is not recognized
        '''
    
    def __init__(self, win, stimuli:list, resp_type = "key", choices:list|object|None=None, resp_start=0, resp_end_trial=True, duration=float('inf'), post_trial_gap=0, quit_key="escape"):
        
        self.win = win
        self.stimuli = stimuli
        self.resp_type = resp_type
        self.choices = choices
        self.quit_key = quit_key
        self.resp_start = resp_start
        self.resp_end_trial = resp_end_trial
        self.duration = duration
        self.post_trial_gap = post_trial_gap
        self.response = None
        self.rt = None
        
        
        if resp_type not in ["key", "button"]:
            raise ValueError("The response type is not recognized")
    
    def __key_response(self):
        
        # correct the choices
        if self.choices is None:
            self.choices = []
        
        # get the start time of the trial
        start_time = core.getTime() 
        
        # Present stimulation but prohibit response  
        for stim in self.stimuli:
            stim.draw()

        self.win.flip()
        core.wait(self.resp_start)
        
        # initialize the loop and mouse
        loop = True
        
        # Present stimulation and allow response
        while loop:
            
            # get the response
            keys = event.getKeys()
            
            # check if the quit key is pressed
            if self.quit_key in keys:
                self.win.close()
                core.quit()
            
            # check if the response is correct
            if self.response is None and set(keys).intersection(self.choices):
                self.response = keys
                self.rt = core.getTime() - start_time
                
                if self.resp_end_trial:
                    loop = False
                        
            # check if the time is over
            if core.getTime() - start_time > self.duration:
                loop = False

    
    def __button_response(self):
        
        # correct the choices
        if self.choices is None:
            raise ValueError("You must provide at least one button")
        elif isinstance(self.choices, object):
            self.buttons = self.choices
        elif isinstance(self.choices, str):
            raise ValueError("if the response type is button, the choices must be either a list of strings or stimBoxes")
        elif all(isinstance(x, str) for x in self.choices):
            width = 0.08
            boxW = (np.max([len(e) for e in self.choices]) + 2) * 0.5 * width
            self.buttons = stimBoxes(
                self.win, setsize = len(self.choices), layout="line", 
                center = [0, -0.4], spacing=width*0.5, 
                width = boxW, height = width)
            self.buttons.stim_text(text = self.choices, height = width*0.8, color=[-1,-1,-1])
        else:
            raise ValueError("if the response type is button, the choices must be either a list of strings or stimBoxes")
            
        
        # get the start time of the trial
        start_time = core.getTime() 
        
        # Present stimulation but prohibit response
        for stim in self.stimuli:
            stim.draw()
        self.buttons.draw()
        self.win.flip()
        core.wait(self.resp_start)

        # initialize the loop
        loop = True
        mouse = event.Mouse()
        
        # Present stimulation and allow response
        while loop:
            
            # check if the quit key is pressed
            if self.quit_key in event.getKeys():
                self.win.close()
                core.quit()
            
            for button in self.buttons.boxes:
                
                if mouse.isPressedIn(self.buttons.boxes[button], buttons=[0]):
                    try:
                        self.response = self.buttons.text[button].text
                    except:
                        self.response = self.buttons.images[button].image
                    self.rt = core.getTime() - start_time
                    
                    if self.resp_end_trial:
                        loop = False# initialize the loop
                
            # check if the time is over
            if core.getTime() - start_time > self.duration:
                loop = False
    
    def run(self):
        
        if self.resp_type == "key":
            self.__key_response()
        elif self.resp_type == "button":
            self.__button_response()
        
        if self.post_trial_gap > 0:
            self.win.flip()
            core.wait(self.post_trial_gap)
    
    def update_stimuli(self, win, stimuli:list):
        ''' Update the stimuli

        Args:
            win (Any): the window object from psychopy
            stimuli (list): a list of stimuli objects
        '''
        
        self.win = win
        self.stimuli = stimuli
        
        # reset the response
        self.response = None
        self.rt = None
    
    def get_response(self):
        ''' Get the response

        Returns:
            dict: the response and the response time
        '''
        return {
            "response":self.response,
            "rt":self.rt
        }