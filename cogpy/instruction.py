from psychopy import core, visual, event
from .layout import stimBoxes
from pathlib import Path


class instr_brief(object):
    '''Instruction class for brief instruction
    
    Args:
        win (Any): the window object from psychopy
        content (str): the content of the instruction. It can be a text or an image
        resp_type (str): the type of response. It can be "key", "button", or "mouse"
        choice (str or list): the choice of the response. 
            If the resp_type is "key", then it should be a list of keys. 
            If the resp_type is "button", then it should be a list of strings. 
            If the resp_type is "mouse", then it should be None
        adaptive (bool): whether the image should be adaptive to the window size
        resp_start (float): the time to wait before the response can be made
        duration (float): the maximum duration of the instruction
        **args: additional arguments for the text or image object
    '''
    
    def __init__(self, win, content:str, resp_type = "key", choice=None, adaptive=True, resp_start = 0.5, duration = float('inf'), button_args=None, **args):
        
        self.win = win
        self.content = content
        self.resp_type = resp_type
        self.choice = choice
        self.resp_start = resp_start
        self.duration = duration
        self.adaptive = adaptive
        self.args = args
        self.button_args = button_args
        
        if resp_type not in ["key", "button", "mouse"]:
            raise ValueError("Invalid response type")
        
        if Path(content).exists():
            print("Displaying image")
            self.display_image()
        else:
            print("Displaying text")
            self.display_text()
    
    def display_image(self):
        
         # create the image object
        image = visual.ImageStim(self.win, image=str(self.content), units='norm', **self.args)

        # adapt the image size to the window size
        if self.adaptive:
            scale = max(image.size/2)
            if scale > 1:
                image.size  = image.size/scale

        image.draw() # draw the image
        
        if self.resp_type == "key":
            self.key_response()
        elif self.resp_type == "button":
            self.button_response()
        elif self.resp_type == "mouse":
            self.mouse_response()
    
    def display_text(self):
        
        if "wrapWidth" not in self.args: self.args["wrapWidth"] = 1.6
        if "color" not in self.args: self.args["color"] = [-1,-1,-1]
        if "height" not in self.args: self.args["height"] = 0.1
        
        # create the text object
        text = visual.TextStim(self.win, text=self.content, **self.args)
        
        text.draw()
        
        if self.resp_type == "key":
            self.key_response()
        elif self.resp_type == "button":
            self.button_response()
        elif self.resp_type == "mouse":
            self.mouse_response()
        
    def key_response(self):
        
        self.win.flip()
        core.wait(self.resp_start) # wait for 0.5 second to avoid accidental touch
        event.clearEvents() # clear events
        
        start_time = core.getTime() # start timing
        
        event.waitKeys(maxWait=self.duration,keyList=self.choice)
        
        self.rt = core.getTime() - start_time
    
    def button_response(self):
        
        width = 0.05
        if "width" not in self.button_args: self.button_args["width"] = (len(self.choice) + 1) * 0.5 * width
        if "height" not in self.button_args: self.button_args["height"] = width
        if "lineWidth" not in self.button_args: self.button_args["lineWidth"] = 2
        if "fillColor" not in self.button_args: self.button_args["fillColor"] = "#669CD1"
        
        # correct the choices
        if self.choice is None:
            raise ValueError("You must provide at least one button")
        elif isinstance(self.choice, str):
            self.buttons = stimBoxes(self.win, setsize = 1, **self.button_args)
            self.buttons.arrange_line(cent = [0, -0.45], spacing=width*0.5)
            self.buttons.stim_text(text = [self.choice], height = width*0.8, color=[-1,-1,-1])
        else:
            raise ValueError("if the response type is button, the choices must be string")
            
        
        # get the start time of the trial
        start_time = core.getTime() 
        
        # Present stimulation but prohibit response
        self.buttons.draw()
        self.win.flip()
        core.wait(self.resp_start) # wait for 0.5 second to avoid accidental touch
        event.clearEvents() # clear events

        # initialize the loop
        loop = True
        mouse = event.Mouse()
        
        # Present stimulation and allow response
        while loop:
            
            for button in self.buttons.boxes:
                
                if mouse.isPressedIn(self.buttons.boxes[button], buttons=[0]):
                    self.rt = core.getTime() - start_time
                    
                    loop = False# initialize the loop
                
            # check if the time is over
            if core.getTime() - start_time > self.duration:
                loop = False
    
    def mouse_response(self):
        
        self.win.flip()
        core.wait(self.resp_start) # wait for 0.5 second to avoid accidental touch
        event.clearEvents() # clear events
            
        start_time = core.getTime() # start timing
        mouse = event.Mouse() # initialize mouse

        # wait for mouse click or until max duration
        while (core.getTime() - start_time) <= self.duration:

            # if left mouse button is pressed, then break the loop
            if mouse.getPressed()[0]:
                self.rt = core.getTime() - start_time
                break
        
        
    def get_rt(self):
        return self.rt

class instr_loop(object):
    
    def __init__(self, win, contents:list, resp_type = "key", adaptive=True, resp_start = 0.5, duration = float('inf'), button_args={}, text_args={}, image_args={}):
        
        self.win = win
        self.contents = contents
        self.resp_type = resp_type
        self.resp_start = resp_start
        self.duration = duration
        self.adaptive = adaptive
        self.button_args = button_args
        self.text_args = text_args
        self.image_args = image_args
        
        if resp_type not in ["key", "button"]:
            raise ValueError("Invalid response type")
        
        page = 0
        while page < len(contents):
            
            content = contents[page]
            
            if Path(content).exists():
                manipulation = self.display_image(content)
            else:
                manipulation = self.display_text(content)
            
            page += manipulation
                
    def display_image(self, image):
        
         # create the image object
        image = visual.ImageStim(self.win, image=str(image), units='norm', **self.image_args)

        # adapt the image size to the window size
        if self.adaptive:
            scale = max(image.size/2)
            if scale > 1:
                image.size  = image.size/scale

        image.draw() # draw the image
        
        if self.resp_type == "key":
            response = self.key_response()
        elif self.resp_type == "button":
            response = self.button_response()
        
        manipulation = 1 if response in ["right","Next"] else -1
        
        return manipulation
    
    def display_text(self, text):
        
        if "wrapWidth" not in self.text_args: self.text_args["wrapWidth"] = 1.6
        if "color" not in self.text_args: self.text_args["color"] = [-1,-1,-1]
        if "height" not in self.text_args: self.text_args["height"] = 0.1
        
        # create the text object
        text = visual.TextStim(self.win, text=text, **self.text_args)
        
        text.draw()
        
        if self.resp_type == "key":
            response = self.key_response()
        elif self.resp_type == "button":
            response = self.button_response()
        
        manipulation = 1 if response in ["right","Next"] else -1
        
        return manipulation
    
    def key_response(self):
        
        self.win.flip()
        core.wait(self.resp_start) # wait for 0.5 second to avoid accidental touch
        event.clearEvents() # clear events
        
        response = event.waitKeys(maxWait=self.duration,keyList=["left","right"])
        
        return response[0]
    
    def button_response(self):
        
        width = 0.05
        if "width" not in self.button_args: self.button_args["width"] = (len("previous") + 1) * 0.5 * width
        if "height" not in self.button_args: self.button_args["height"] = width
        if "lineWidth" not in self.button_args: self.button_args["lineWidth"] = 2
        if "fillColor" not in self.button_args: self.button_args["fillColor"] = "#669CD1"
        
        # correct the choices
        self.buttons = stimBoxes(self.win, setsize = 2, **self.button_args)
        self.buttons.arrange_line(cent = [0, -0.45], spacing=width*0.5)
        self.buttons.stim_text(text = ["Previous","Next"], height = width*0.8, color=[-1,-1,-1])

            
        # get the start time of the trial
        start_time = core.getTime() 
        
        # Present stimulation but prohibit response
        self.buttons.draw()
        self.win.flip()
        core.wait(self.resp_start) # wait for 0.5 second to avoid accidental touch
        event.clearEvents() # clear events

        # initialize the loop
        loop = True
        mouse = event.Mouse()
        
        # Present stimulation and allow response
        while loop:
            
            for button in self.buttons.boxes:
                
                if mouse.isPressedIn(self.buttons.boxes[button], buttons=[0]):
                    response = self.buttons.text[button].text
                    loop = False # initialize the loop
                
            # check if the time is over
            if core.getTime() - start_time > self.duration:
                loop = False
        
        return response