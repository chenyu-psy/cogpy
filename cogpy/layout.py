from psychopy.visual import TextStim, ImageStim, Rect
import random
import numpy as np
import warnings


class stimBoxes(object):
    
    def __init__(self, win, setsize, **args):
        self.win = win
        self.setsize = setsize
        self.box_args = args
        self.winH = 1 # window height
        self.winW = win.windowedSize[0]/win.windowedSize[1]*self.winH # window width
        
        # set up default arguments
        if "width" not in args: args["width"] = 0.16
        if "height" not in args: args["height"] = args["width"]
        if "lineColor" not in args: args["lineColor"] = [-1,-1,-1]
        if "lineWidth" not in args: args["lineWidth"] = 3
        if args.get("units", "height") != "height":
            raise ValueError("This class only supports height units")
        else:
            args["units"] = "height"

            
    def arrange_circle(self, cent = [0,0], radius=0.3, oval=1, rotation=0):
        '''Arrange the boxes in a circle

        Args:
            radius (float, optional): The radius of the circle. Defaults to 0.5.
            cent (list, optional): The center of the circle. Defaults to [0,0].
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
            x = radius*np.cos(-theta*i + rot) + cent[0]
            y = radius*np.sin(-theta*i + rot)*oval + cent[1]
            # set the position of the box
            self.boxes[f"P{i+1}"] = Rect(self.win, pos = [x, y], **self.box_args)
    
    def arrange_line(self, cent=[0,0], direction="horizontal", spacing:float=0):
        '''Arrange the boxes in a line

        Args:
            direction (str, optional): The direction of the line. 
                The default value is "horizontal".
            cent (list, optional): The center of the line. Defaults to [0,0].
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
            
            # the spacing between boxes
            if spacing is None:
                spacing = np.min((self.winW*0.9 - width*n) / (n-1),width)
                
            # calculate the total width of the line and the leftmost x position
            lineW = width*n + spacing*(n-1)
            leftX = cent[0] - lineW/2
        
            for i in range(n):
                x = leftX + (i + 0.5)*width + i*spacing
                self.boxes[f"P{i+1}"] = Rect(self.win, pos = [x, cent[1]], **self.box_args)
                
        elif direction == "vertical":
            
            # check if the boxes are too tall
            if height*n + spacing*(n-1) > 2:
                raise ValueError("The boxes are too tall to fit in the window")
            
            # the spacing between boxes
            if spacing is None:
                spacing = np.min((self.winH*0.9 - height*n) / (n-1), height)
                
            # calculate the total height of the line and the bottommost y position
            lineH = height*n + spacing*(n-1)
            topY = cent[1] + lineH/2

            for i in range(n):
                y = topY - (i + 0.5)*height - i*spacing
                self.boxes[f"P{i+1}"] = Rect(self.win, pos = [cent[0], y], **self.box_args)
    
    def arrange_grid(self, nrow:int, ncol:int, cent=[0,0], spW:float|None=None, spH:float|None=None):
        '''Arrange the boxes in a grid

        Args:
            nrow (int): The number of rows in the grid.
            ncol (int): The number of columns in the grid.
            cent (list, optional): The center of the grid. Defaults to [0,0].
            spacing (float, optional): The spacing between boxes. Defaults to None.
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
        if spW is not None:
            if width*ncol + spW*(ncol-1) > self.winW*0.9:
                raise ValueError("The boxes are too wide to fit in the window")
        else:
            spW = np.min((self.winW*0.9 - width*ncol) / (ncol-1), width)
            
        if spH is not None:
            if height*nrow + spH*(nrow-1) > self.winH*0.9:
                raise ValueError("The boxes are too tall to fit in the window")
        else:
            spH = np.min((self.winH*0.9 - height*nrow) / (nrow-1), height)
            
        # Calculate the total width and height of the grid
        gridW = ncol * width + (ncol - 1) * spW
        gridH = nrow * height + (nrow - 1) * spH

        # Calculate offsets to center the grid at `cent`
        leftX = cent[0] - gridW / 2
        topY = cent[1] + gridH / 2

        # Initialize the boxes
        self.boxes = {}

        for i in range(n):
            row = i // ncol
            col = i % ncol
            x = leftX + (col + 0.5) * width + col * spW
            y = topY - (row + 0.5) * height - row * spH
            self.boxes[f"P{i+1}"] = Rect(self.win, pos=[x, y], **self.box_args)
    
    def arrange_random(self, width:float, height:float, spacing:float=0):
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
    
    def arrange_custom(self, positions:dict):
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
            for box in self.boxes:
                self.text[box] = TextStim(self.win, text=text[box], pos=self.boxes[box].pos, **args)
    
    def stim_image(self, image:list|dict, **args):
        '''Add image stimuli to the boxes

        Args:
            image (list|dict): The image stimuli to be added to the boxes.
                If a list is provided, the images will be added to the boxes in order.
                If a dictionary is provided, the images will be added to the boxes based on the keys.
        '''
            
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
                self.images[box] = ImageStim(self.win, image=str(image[i]), pos=self.boxes[box].pos, **args)
        elif isinstance(image, dict):
            # add images to the boxes
            for box in self.boxes:
                self.images[box] = ImageStim(self.win, image=str(image[box]), pos=self.boxes[box].pos, **args)
    
    def stim_color(self, color:list|dict):
        '''Add color stimuli to the boxes

        Args:
            color (list|dict): The color stimuli to be added to the boxes.
                If a list is provided, the colors will be added to the boxes in order.
                If a dictionary is provided, the colors will be added to the boxes based on the keys.
        '''
            
        # check if the boxes are not initialized
        if not hasattr(self, "boxes"):
            raise ValueError("The boxes are not initialized")
        
        if isinstance(color, list):
            # check if the number of color stimuli matches the number of boxes
            if len(color) != len(self.boxes):
                raise ValueError("The number of color stimuli should match the number of boxes")
            # add colors to the boxes
            for i, box in enumerate(self.boxes):
                self.boxes[box].fillColor = color[i]
        elif isinstance(color, dict):
            # add colors to the boxes
            for box in self.boxes:
                self.boxes[box].fillColor = color[i]
    
    def draw_boxes(self):
        '''Draw the boxes and text stimuli
        '''
        
        for box in self.boxes:
            self.boxes[box].draw()
    
    def draw_text(self):
        '''Draw the text stimuli
        '''
        
        if not hasattr(self, "text"):
            raise ValueError("The text stimuli are not initialized")
        
        for box in self.text:
            self.text[box].draw()
    
    def draw_images(self):
        '''Draw the image stimuli
        '''
        
        if not hasattr(self, "images"):
            raise ValueError("The image stimuli are not initialized")
        
        for box in self.images:
            self.images[box].draw()
    
    def draw(self):
        '''Draw the boxes and stimuli
        '''
        
        if hasattr(self, "boxes"): self.draw_boxes()
        if hasattr(self, "text"): self.draw_text()
        if hasattr(self, "images"):self.draw_images()