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
        self.button_args = {} if button_args is None else button_args
        
        if resp_type not in ["key", "button", "mouse"]:
            raise ValueError("Invalid response type")
        
        if Path(content).exists():
            self.__display_image()
        else:
            self.__display_text()
    
    def __display_image(self):
        
         # create the image object
        image = visual.ImageStim(self.win, image=str(self.content), units='norm', **self.args)

        # adapt the image size to the window size
        if self.adaptive:
            scale = max(image.size/2)
            if scale > 1:
                image.size  = image.size/scale

        image.draw() # draw the image
        
        if self.resp_type == "key":
            self.__key_response()
        elif self.resp_type == "button":
            self.__button_response()
        elif self.resp_type == "mouse":
            self.__mouse_response()
    
    def __display_text(self):
        
        self.args["wrapWidth"] = self.args.get("wrapWidth", 1.6)
        self.args["color"] = self.args.get("color", [-1,-1,-1])
        self.args["height"] = self.args.get("height", 0.1)
        
        # create the text object
        text = visual.TextStim(self.win, text=self.content, **self.args)
        
        text.draw()
        
        if self.resp_type == "key":
            self.__key_response()
        elif self.resp_type == "button":
            self.__button_response()
        elif self.resp_type == "mouse":
            self.__mouse_response()
        
    def __key_response(self):
        
        self.win.flip()
        core.wait(self.resp_start) # wait for 0.5 second to avoid accidental touch
        event.clearEvents() # clear events
        
        start_time = core.getTime() # start timing
        
        event.waitKeys(maxWait=self.duration,keyList=self.choice)
        
        self.rt = core.getTime() - start_time
    
    def __button_response(self):
        
        width = 0.05
        self.button_args["width"] = self.button_args.get("width", (len(self.choice) + 1) * 0.5 * width)
        self.button_args["height"] = self.button_args.get("height", width)
        self.button_args["lineWidth"] = self.button_args.get("lineWidth", 2)
        self.button_args["fillColor"] = self.button_args.get("fillColor", "#669CD1")
        
        # correct the choices
        if self.choice is None:
            raise ValueError("You must provide at least one button")
        elif isinstance(self.choice, str):
            self.button = stimBoxes(self.win, setsize = 1, layout="line", center = [0, -0.45], **self.button_args)
            self.button.stim_text(text = [self.choice], height = width*0.8, color=[-1,-1,-1])
        else:
            raise ValueError("if the response type is button, the choices must be string")
            
        
        # get the start time of the trial
        start_time = core.getTime() 
        
        # Present stimulation but prohibit response
        self.button.draw()
        self.win.flip()
        core.wait(self.resp_start) # wait for 0.5 second to avoid accidental touch
        event.clearEvents() # clear events

        # initialize the loop
        loop = True
        mouse = event.Mouse()
        
        # Present stimulation and allow response
        while loop:
            
            for button in self.button.boxes:
                
                if mouse.isPressedIn(self.button.boxes[button], buttons=[0]):
                    self.rt = core.getTime() - start_time
                    
                    loop = False# initialize the loop
                
            # check if the time is over
            if core.getTime() - start_time > self.duration:
                loop = False
    
    def __mouse_response(self):
        
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
                manipulation = self.__display_image(content)
            else:
                manipulation = self.__display_text(content)
            
            page += manipulation
                
    def __display_image(self, image):
        
         # create the image object
        image = visual.ImageStim(self.win, image=str(image), units='norm', **self.image_args)

        # adapt the image size to the window size
        if self.adaptive:
            scale = max(image.size/2)
            if scale > 1:
                image.size  = image.size/scale

        image.draw() # draw the image
        
        if self.resp_type == "key":
            response = self.__key_response()
        elif self.resp_type == "button":
            response = self.__button_response()
        
        manipulation = 1 if response in ["right","Next"] else -1
        
        return manipulation
    
    def __display_text(self, text):
        
        if "wrapWidth" not in self.text_args: self.text_args["wrapWidth"] = 1.6
        if "color" not in self.text_args: self.text_args["color"] = [-1,-1,-1]
        if "height" not in self.text_args: self.text_args["height"] = 0.1
        
        # create the text object
        text = visual.TextStim(self.win, text=text, **self.text_args)
        
        text.draw()
        
        if self.resp_type == "key":
            response = self.__key_response()
        elif self.resp_type == "button":
            response = self.__button_response()
        
        manipulation = 1 if response in ["right","Next"] else -1
        
        return manipulation
    
    def __key_response(self):
        
        self.win.flip()
        core.wait(self.resp_start) # wait for 0.5 second to avoid accidental touch
        event.clearEvents() # clear events
        
        response = event.waitKeys(maxWait=self.duration,keyList=["left","right"])
        
        return response[0]
    
    def __button_response(self):
        
        width = 0.05
        if "width" not in self.button_args: self.button_args["width"] = (len("previous") + 1) * 0.5 * width
        if "height" not in self.button_args: self.button_args["height"] = width
        if "lineWidth" not in self.button_args: self.button_args["lineWidth"] = 2
        if "fillColor" not in self.button_args: self.button_args["fillColor"] = "#669CD1"
        
        # correct the choices
        self.buttons = stimBoxes(self.win, setsize = 2, layout="line", center = [0, -0.45], **self.button_args)
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
    


    
def instr_input(win, question, choice='enter', allowEmpty = True, duration = float('inf'), **args):
    ''' Display a screen to ask the participant to input the information.

    Args:
        win (object): the window object of the experiment.
        question (str): the question to ask the participant.
        resp_type (str, optional): the type of response. It can be "key" or "button". Defaults to "key".
        choice (str | None, optional): _description_. Defaults to None.
        allowEmpty (bool, optional): whether the participant can leave the input empty. Defaults to True.
        duration (float, optional): the maximum duration of the instruction. Defaults to float('inf').

    Raises:
        ValueError: Invalid response type
    '''
    
    args['units'] = args.get('units', 'norm')
    args['height'] = args.get('height', 0.15)
    args['color'] = args.get('color', [-1,-1,-1])
    
    ques_args = args.copy()
    ques_args['pos'] = ques_args.get('pos', [0,0.5])
    
    ans_args = args.copy()
    ans_args['pos'] = [0,0]
    
    tip_args = args.copy()
    tip_args['pos'] = [0,-0.7]
    tip_args['height'] = 0.08
    
    keyNames = {
        'return': 'Enter',
        'space': 'Space',
        'backspace': 'Backspace'
    }
    
    question_text = visual.TextStim(win, text=question, **ques_args)
    question_text.wrapWidth = 1.8
    answer_text = visual.TextStim(win, text='', **ans_args)
    tip_text = visual.TextStim(win, text=f"Press the '{keyNames[choice]}' key to continue", **tip_args)
    tip_text.wrapWidth = 1.8
    
    # result
    result = None
    
    # display the question and answer
    question_text.draw()
    answer_text.draw()
    tip_text.draw()
    win.flip()
    
    loop = True
    start_time = core.getTime()
    
    while loop:
        
        if core.getTime() - start_time > duration:
            loop = False
        
        for key in event.getKeys():
            
            if key == 'backspace':
                answer_text.text = answer_text.text[:-1]
            elif key == choice:
                if not allowEmpty and answer_text.text == '':
                    continue
                else:
                    result = answer_text.text
                    loop = False
            elif key in [chr(i) for i in range(97,123)]+[str(i) for i in range(11)]:
                answer_text.text += key.upper()
            
        question_text.draw()
        answer_text.draw()
        tip_text.draw()
        win.flip()
    
    return result
