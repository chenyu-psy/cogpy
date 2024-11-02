from psychopy.visual import TextStim, ImageStim, Rect
import random
import numpy as np
import warnings


class stimBoxes(object):
    ''' A class to arrange boxes in a circle, line, grid, or randomly and add text or image stimuli to the boxes

    Args:
        win: the window object from psychopy
        setsize: the number of boxes
        layout: the layout of the boxes. One of "circle", "line", "grid", "random", or "custom".
        **args: additional arguments for the layout and the boxes (see below)
        
    Description:
        The class can arrange the boxes in a circle, line, grid, or randomly.
        
        Layout-specific arguments:
        
        - Circle layout:
            - center (list, optional): The center of the circle. Defaults to [0, 0].
            - radius (float, optional): The radius of the circle. Defaults to 0.3.
            - oval (float, optional): The ovalness of the circle. Defaults to 1.
            - rotation (float, optional): The rotation of the circle in degrees. Defaults to 0.
        
        - Line layout:
            - center (list, optional): The center of the line. Defaults to [0, 0].
            - direction (str, optional): The direction of the line, either "horizontal" or "vertical". Defaults to "horizontal".
            - spacing (float, optional): The spacing between boxes. Defaults to 0.
        
        - Grid layout:
            - center (list, optional): The center of the grid. Defaults to [0, 0].
            - nrow (int): The number of rows in the grid. (Required)
            - ncol (int): The number of columns in the grid. (Required)
            - spacing (list, optional): The spacing between boxes in the grid. Defaults to [0, 0].
        
        - Random layout:
            - width (float, optional): The width of the area. Defaults to the window height.
            - height (float, optional): The height of the area. Defaults to the window height.
            - spacing (float, optional): The spacing between boxes. Defaults to 0.
        
        - Custom layout:
            - positions (dict): A dictionary of positions for each box. The keys are the names of the boxes, and the values are the positions of the boxes. (Required)
        
        Common box arguments:
            - width (float, optional): The width of each box. Defaults to 0.16.
            - height (float, optional): The height of each box. Defaults to the width.
            - lineColor (list, optional): The color of the box lines. Defaults to [-1, -1, -1].
            - lineWidth (int, optional): The width of the box lines. Defaults to 3.
            - units (str, optional): The units for the box dimensions. Must be "height".
    '''
    
    def __init__(self, win, setsize, layout = "line", **args):
        self.win = win
        self.setsize = setsize
        self.box_args = args
        self.winH = 1 # window height
        self.winW = win.windowedSize[0]/win.windowedSize[1]*self.winH # window width
        
        # set up default arguments
        self.box_args["width"] = self.box_args.get("width", 0.16)
        self.box_args["height"] = self.box_args.get("height", self.box_args["width"])
        self.box_args["lineColor"] = self.box_args.get("lineColor", [-1, -1, -1])
        self.box_args["lineWidth"] = self.box_args.get("lineWidth", 3)

        # Validate units and set them if correct
        if self.box_args.get("units", "height") != "height":
            raise ValueError("This class only supports height units")
        self.box_args["units"] = "height"
        
        # set up default arguments according to the layout
        layout_args = {}
        layout_args["center"] = args.pop("center", [0, 0])

        
        if layout == "circle":
            # set up default arguments
            layout_args["radius"] = args.pop("radius", 0.3)
            layout_args["oval"] = args.pop("oval", 1)
            layout_args["rotation"] = args.pop("rotation", 0)
            # arrange the boxes in a circle
            self.__arrange_circle(**layout_args)
            
        elif layout == "line":
            # set up default arguments
            layout_args["direction"] = args.pop("direction", "horizontal")
            layout_args["spacing"] = args.pop("spacing", 0)
            # arrange the boxes in a line
            self.__arrange_line(**layout_args)
            
        elif layout == "grid":
            # set up default arguments
            if "nrow" not in args or "ncol" not in args:
                raise ValueError("The number of rows and columns should be specified for the grid layout")
            else:
                layout_args["nrow"] = args.pop("nrow")
                layout_args["ncol"] = args.pop("ncol")
            layout_args["spacing"] = args.pop("spacing", [0,0])
            # arrange the boxes in a grid
            self.__arrange_grid(**layout_args)
            
        elif layout == "random":
            # set up default arguments
            layout_args["width"] = args.pop("width", self.winH)
            layout_args["height"] = args.pop("height", self.winH)
            layout_args["spacing"] = args.pop("spacing", 0)
            # arrange the boxes randomly
            self.__arrange_random(**layout_args)
            
        elif layout == "custom":
            # set up default arguments
            if "positions" not in args:
                raise ValueError("The positions should be specified for the custom layout")
            else:
                layout_args["positions"] = args.pop("positions")
            # arrange the boxes based on custom positions
            self.__arrange_custom(**layout_args)
        else:
            raise ValueError("The layout should be either circle, line, grid, random, or custom")


            
    def __arrange_circle(self, center = [0,0], radius=0.3, oval=1, rotation=0):
        '''Arrange the boxes in a circle

        Args:
            radius (float, optional): The radius of the circle. Defaults to 0.5.
            center (list, optional): The center of the circle. Defaults to [0,0].
            oval (int, optional): The ovalness of the circle. 
                A value larger than 1 will make the circle taller, 
                while a value smaller than 1 will make the circle wider. 
                The default value is 1.
            rotation (int, optional): The rotation of the circle.
                A positive value will rotate the circle clockwise,
                while a negative value will rotate the circle counterclockwise.
                The default value is 0.
        '''
        
        # check the input values
        if (radius < 0 or radius > 0.5):
            raise ValueError("The radius should be between 0 and 0.5")
        if (oval < 0):
            raise ValueError("The ovalness should be larger than 0")
        if (radius*oval > self.winH/2):
            raise ValueError("The ovalness is too large")
        
        # initialize the boxes
        self.boxes = {}
        
        n = self.setsize # number of boxes
        rot = rotation/180*np.pi # rotation in radian
        theta = 2*np.pi/n # angle between boxes
        for i in range(self.setsize):
            # calculate the position of the box
            x = radius*np.cos(-theta*i + rot) + center[0]
            y = radius*np.sin(-theta*i + rot)*oval + center[1]
            # set the position of the box
            self.boxes[f"P{i+1}"] = Rect(self.win, pos = [x, y], **self.box_args)
    
    def __arrange_line(self, center=[0,0], direction="horizontal", spacing:float=0):
        '''Arrange the boxes in a line

        Args:
            direction (str, optional): The direction of the line. 
                The default value is "horizontal".
            center (list, optional): The center of the line. Defaults to [0,0].
            spacing (float, optional): The spacing between boxes. Defaults to 0.
        '''
        n = self.setsize # number of boxes
        width = self.box_args["width"]
        height = self.box_args["height"]
        
        # initialize the boxes
        self.boxes = {}
        
        if direction == "horizontal":
            # check if the boxes are too wide
            if width*n + spacing*(n-1) > 2:
                raise ValueError("The boxes are too wide to fit in the window")
                
            # calculate the total width of the line and the leftmost x position
            lineW = width*n + spacing*(n-1)
            leftX = center[0] - lineW/2
        
            for i in range(n):
                x = leftX + (i + 0.5)*width + i*spacing
                self.boxes[f"P{i+1}"] = Rect(self.win, pos = [x, center[1]], **self.box_args)
                
        elif direction == "vertical":
            
            # check if the boxes are too tall
            if height*n + spacing*(n-1) > 2:
                raise ValueError("The boxes are too tall to fit in the window")
                
            # calculate the total height of the line and the bottommost y position
            lineH = height*n + spacing*(n-1)
            topY = center[1] + lineH/2

            for i in range(n):
                y = topY - (i + 0.5)*height - i*spacing
                self.boxes[f"P{i+1}"] = Rect(self.win, pos = [center[0], y], **self.box_args)
    
    def __arrange_grid(self, nrow:int, ncol:int, center=[0,0], spacing = [0,0]):
        '''Arrange the boxes in a grid

        Args:
            nrow (int): The number of rows in the grid.
            ncol (int): The number of columns in the grid.
            center (list, optional): The center of the grid. Defaults to [0,0].
            spacing (list, optional): The spacing between boxes in the grid. Defaults to [0,0].
        '''
        n = self.setsize # number of boxes
        width = self.box_args["width"]
        height = self.box_args["height"]
        
        # check if the grid is too small or too large
        if nrow*ncol < n:
            raise ValueError("The grid is too small to fit all the boxes")
        elif nrow*ncol > n:
            warnings.warn("There are empty spaces in the grid")
            
        # check if the boxes are too wide or too tall
        if width*ncol + spacing[0]*(ncol-1) > self.winW*0.9:
            raise ValueError("The boxes are too wide to fit in the window")

        if height*nrow + spacing[1]*(nrow-1) > self.winH*0.9:
            raise ValueError("The boxes are too tall to fit in the window")

            
        # Calculate the total width and height of the grid
        gridW = ncol * width + (ncol - 1) * spacing[0]
        gridH = nrow * height + (nrow - 1) * spacing[1]

        # Calculate offsets to center the grid at `center`
        leftX = center[0] - gridW / 2
        topY = center[1] + gridH / 2

        # Initialize the boxes
        self.boxes = {}

        for i in range(n):
            row = i // ncol
            col = i % ncol
            x = leftX + (col + 0.5) * width + col * spacing[0]
            y = topY - (row + 0.5) * height - row * spacing[1]
            self.boxes[f"P{i+1}"] = Rect(self.win, pos=[x, y], **self.box_args)
    
    def __arrange_random(self, width:float, height:float, spacing:float=0):
        '''Randomly arrange the boxes

        Args:
            width (float): The width of the area.
            height (float): The height of the area.
        '''
        
        # number of boxes
        n = self.setsize
        
        # the size of a cell
        cellWidth = self.box_args["width"] + spacing
        cellHeight = self.box_args["height"] + spacing
        
        # number of cells in the area
        nrow = int(height/cellHeight)
        ncol = int(width/cellWidth)
        
        # the width and height of the area
        areaW = ncol*cellWidth
        areaH = nrow*cellHeight
        
        # calculate the left and top position of the area
        leftX = -areaW/2
        topY = areaH/2
        
        # check if the area is too small
        if nrow*ncol < n:
            raise ValueError("The area is too small to fit all the boxes")
        
        # Generate all possible cell indices
        cells = [(i, j) for i in range(nrow) for j in range(ncol)]
        
        # Shuffle the list of cells to randomize the placement
        random.shuffle(cells)
        
        # Select the first n cells for placement
        selected_cells = cells[:n]
        
        # Initialize the boxes
        self.boxes = {}
        
        # Convert cell indices to actual positions
        for i in range(n):
            row = selected_cells[i][0]
            col = selected_cells[i][1]
            x = leftX + (col + 0.5)*cellWidth
            y = topY - (row + 0.5)*cellHeight
            self.boxes[f"P{i+1}"] = Rect(self.win, pos = [x, y], **self.box_args)
    
    def __arrange_custom(self, positions:dict):
        '''Arrange the boxes based on custom positions

        Args:
            positions (dict): A dictionary of positions for each box.
                The keys are the names of the boxes, and the values are the positions of the boxes.
        '''
        
        # number of boxes
        n = self.setsize
        
        # check if the number of positions matches the number of boxes
        if len(positions) != n:
            raise ValueError("The number of positions should match the number of boxes")
        
        # initialize the boxes
        self.boxes = {}
        
        # add the boxes to the layout
        for i in range(n):
            self.boxes[f"P{i+1}"] = Rect(self.win, positions[f"P{i+1}"], **self.box_args)
    
    def stim_text(self, text:list|dict, **args):
        '''Add text stimuli to the boxes

        Args:
            text (list|dict): The text stimuli to be added to the boxes.
                If a list is provided, the text will be added to the boxes in order.
                If a dictionary is provided, the text will be added to the boxes based on the keys.
        '''
        
        if "height" not in args: args["height"] = 0.16
        if "color" not in args: args["color"] = [-1,-1,-1]
        if args.get("units", "height") != "height":
            raise ValueError("This class only supports height units")
        else:
            args["units"] = "height"
            
        # check if the boxes are not initialized
        if not hasattr(self, "boxes"):
            raise ValueError("The boxes are not initialized")
        
        # initialize the text stimuli
        self.text = {}
        
        if isinstance(text, list):
            # check if the number of text stimuli matches the number of boxes
            if len(text) != len(self.boxes):
                raise ValueError("The number of text stimuli should match the number of boxes")
            # add text to the boxes
            for i, box in enumerate(self.boxes):
                self.text[box] = TextStim(self.win, text=text[i], pos=self.boxes[box].pos, **args)
        elif isinstance(text, dict):
            # add text to the boxes
            for box,content in text.items():
                self.text[box] = TextStim(self.win, text=content, pos=self.boxes[box].pos, **args)
    
    def stim_image(self, image:list|dict, scale = "max", **args):
        '''Add image stimuli to the boxes

        Args:
            image (list|dict): The image stimuli to be added to the boxes.
                If a list is provided, the images will be added to the boxes in order.
                If a dictionary is provided, the images will be added to the boxes based on the keys.
        ''' 
        
        if args.get("units", "height") != "height":
            raise ValueError("This class only supports height units")
        else:
            args["units"] = "height"
            
        # check if the boxes are not initialized
        if not hasattr(self, "boxes"):
            raise ValueError("The boxes are not initialized")
        
        # initialize the image stimuli
        self.images = {}
        
        if isinstance(image, list):
            # check if the number of image stimuli matches the number of boxes
            if len(image) != len(self.boxes):
                raise ValueError("The number of image stimuli should match the number of boxes")
            # add images to the boxes
            for i, box in enumerate(self.boxes):
                # create the image object
                self.images[box] = ImageStim(self.win, image=str(image[i]), pos=self.boxes[box].pos, **args)
                # resize the image
                if scale == "height":
                    ratio = self.images[box].size[1]/self.box_args["height"]
                elif scale == "width":
                    ratio = self.images[box].size[0]/self.box_args["width"]
                elif scale == "max":
                    ratioW = self.images[box].size[0]/self.box_args["width"]
                    ratioH = self.images[box].size[1]/self.box_args["height"]
                    ratio = np.max([ratioW, ratioH])
                else:
                    ratio = 1
                self.images[box].size = self.images[box].size/ratio
                    
        elif isinstance(image, dict):
            # add images to the boxes
            for box, content in image.items():
                self.images[box] = ImageStim(self.win, image=str(content), pos=self.boxes[box].pos, **args)
                # resize the image
                if scale == "height":
                    ratio = self.images[box].size[1]/self.box_args["height"]
                elif scale == "width":
                    ratio = self.images[box].size[0]/self.box_args["width"]
                elif scale == "max":
                    ratioW = self.images[box].size[0]/self.box_args["width"]
                    ratioH = self.images[box].size[1]/self.box_args["height"]
                    ratio = np.max([ratioW, ratioH])
                else:
                    ratio = 1
                self.images[box].size = self.images[box].size/ratio
    
    def stim_boxes(self, **args):
        '''Assign different properties to the boxes

        Args:
            **args: The properties to be assigned to the boxes. Each argument should be a list with the same length as the number of boxes.
        '''
        
        # Check if each argument is a list and has the same length as the number of boxes
        for arg in args:
            if not isinstance(args[arg], list):
                raise ValueError(f"{arg} should be a list")
            if len(args[arg]) != self.setsize:
                raise ValueError(f"The number of {arg} should match the number of boxes")
            
        # check if the boxes are not initialized
        if not hasattr(self, "boxes"):
            raise ValueError("The boxes are not initialized")
        
        # update the box arguments
        for arg in args:
            for i in range(self.setsize):
                self.boxes[f"P{i+1}"].__setattr__(arg, args[arg][i])

    
    def __draw_boxes(self):
        '''Draw the boxes and text stimuli
        '''
        
        for box in self.boxes:
            self.boxes[box].draw()
    
    def __draw_text(self):
        '''Draw the text stimuli
        '''
        
        if not hasattr(self, "text"):
            raise ValueError("The text stimuli are not initialized")
        
        for box in self.text:
            self.text[box].draw()
    
    def __draw_images(self):
        '''Draw the image stimuli
        '''
        
        if not hasattr(self, "images"):
            raise ValueError("The image stimuli are not initialized")
        
        for box in self.images:
            self.images[box].draw()
    
    def draw(self):
        '''Draw the boxes and stimuli
        '''
        
        if hasattr(self, "boxes"): self.__draw_boxes()
        if hasattr(self, "images"):self.__draw_images()
        if hasattr(self, "text"): self.__draw_text()
        