# cogpy

This is a [psychopy](https://psychopy.org) plugin for cognitive psychology experiments. It is a wrapper around the PsychoPy library, offering user-friendly functions for creating experiments.

## Installation

```bash
pip install git+https://github.com/chenyu-psy/cogpy.git
```

## Arrange stimuli

`stimBoxes` is designed to arrange stimuli in specific positions. Currently, it supports three types of stimuli: `text`, `image`, and `shape (rect)`, as well as five types of layouts: `line`, `circle`, `grid`, `random`, and `custom`.

1. `circle`: arranges stimuli in a circle. The `radius` parameter controls the radius of the circle, and the `rotation` parameter controls the rotation of the circle.
2. `line`: organizes stimuli in a line, either vertically or horizontally, as specified by the `direction` parameter. The `spacing` parameter determines the distance between the stimuli.
3. `grid`: arranges stimuli in a grid. The `nrow` and `ncol` parameters control the number of rows and columns, respectively, and the `spH` and `spW` parameters control the horizontal and vertical spacing between stimuli.
4. `random`: places stimuli randomly within a specified area. The `width` and `height` parameters control the width and height of the area, and the `spacing` parameter controls the minimum distance between stimuli.
5. `custom`: allows users to specify the positions of stimuli manually. The `positions` parameter should be a dictionary with the `Pi` (e.g., P1, P2, P3) as keys and the positions as values.


```python

# %% Import libraries
import cogpy as cp
from psychopy import core, visual

# open window
win = visual.Window(size=[1600,900],color=[1,1,1], fullscr=False)

circle_boxes = cp.stimBoxes(
    win, setsize = 6, 
    layout="circle", radius = 0.3, rotation=120,
    # layout="line", spacing=0.1,
    # layout="grid", nrow=3, ncol=2, spH=0.05, spW=0.05,
    # layout="random", width = 0.6, height = 0.6, spacing=0.01,
    width = 0.2, lineColor=[-1,-1,-1], fillColor = [1,1,1])

circle_boxes.stim_text(text = ['A','B','C','D','E','F'], height = 0.08, color=[-1,-1,-1])

circle_boxes.draw()

win.flip()
core.wait(20)

```

## Trial

`trial` is a class that helps to present stimuli and collect responses. It supports both keyboard and button responses.

```python
# %% Import libraries
import cogpy as cp
from psychopy import core, visual

# open window
win = visual.Window(size=[1600,900],color=[1,1,1], fullscr=False)

circle_boxes = cp.stimBoxes(
    win, setsize = 6, 
    layout="circle", radius = 0.3, rotation=120,
    width = 0.2, lineColor=[-1,-1,-1], fillColor = [1,1,1])
circle_boxes.stim_text(text = ['A','B','C','D','E','F'], height = 0.08, color="#bababa")

test_trial = trial(
    win, 
    stimuli = [circle_boxes], 
    resp_type = "key", 
    choices = ['space'], 
    # resp_type = "button", 
    # choices = ['hello', 'world'], 
    resp_start = 3, 
    resp_end_trial = True, 
    duration = 20)

test_trial.run()
results = test_trial.get_response()
print(results)

```

## Intructions

There are three functions that you can used to simplify the process of creating instructions: `instr_brief`, `instr_loop`, and `instr_input`.

### instr_brief

`instr_brief` is used to present a brief instruction. It supports both text and image instructions.

```python

# %% Import libraries
import cogpy as cp
from psychopy import core, visual

# open window
win = visual.Window(size=[1600,900],color=[1,1,1], fullscr=False)

instr_brief(win, text = "This is a brief instruction.")

```

### instr_loop

`instr_loop` is used to present a loop of instructions. Participants can either press the arrow keys or the buttons on the screen to navigate to the next or previous instructions. It supports both text and image instructions.

```python

# %% Import libraries
import cogpy as cp
from psychopy import core, visual

# open window
win = visual.Window(size=[1600,900],color=[1,1,1], fullscr=False)

instr_loop(
    win, 
    contents = [
        "This is the first instruction.", 
        "This is the second instruction."], 
    resp_type = "button")

```

### instr_input

`instr_input` is used to present an instruction that requires participants to input a response.

```python

# %% Import libraries
import cogpy as cp
from psychopy import core, visual

# open window
win = visual.Window(size=[1600,900],color=[1,1,1], fullscr=False)

cp.instr_input(
    win, 
    question = "Please enter your participant ID", 
    choice='return', 
    duration=10)

```
