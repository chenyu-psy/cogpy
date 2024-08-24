# cogpy

This is a [psychopy](https://psychopy.org) plugin for cognitive psychology experiments. It is a wrapper around the PsychoPy library, offering user-friendly functions for creating experiments.

## Installation

```bash
pip install git+https://github.com/chenyu-psy/cogpy.git
```

## Arrange stimuli

`stimBoxes` is designed to arrange stimuli in specific positions. Currently, it supports three types of stimuli: `text`, `image`, and `shape (rect)`, as well as five types of layouts: `line`, `circle`, `grid`, `random`, and `custom`.

### Line

The `arrange_line` function organizes stimuli in a line, either vertically or horizontally, as specified by the `direction` parameter. The `spacing` parameter determines the distance between the stimuli.

```python

from cogpy import stimBoxes
from psychopy import core, visual

# open window
win = visual.Window(size=[1600,900],color=[1,1,1], fullscr=False)

circle_boxes = stimBoxes(win, setsize = 6, width = 0.16)
circle_boxes.arrange_line(spacing=0.05)
circle_boxes.stim_text(text = ['A','B','C','D','E','F'], height = 0.12, color="#bababa")

circle_boxes.draw()

win.flip()
core.wait(20)

```

### Circle

The `arrange_circle` function arranges stimuli in a circle. The `radius` parameter controls the radius of the circle, and the `rotation` parameter controls the rotation of the circle.

```python
from cogpy import stimBoxes
from psychopy import core, visual

# open window
win = visual.Window(size=[1600,900],color=[1,1,1], fullscr=False)

circle_boxes = stimBoxes(win, setsize = 6, width = 0.16)
circle_boxes.arrange_circle(radius = 0.3, rotation=120)
circle_boxes.stim_text(text = ['A','B','C','D','E','F'], height = 0.12, color="#bababa")

circle_boxes.draw()

win.flip()
core.wait(20)
```

### Grid

The `arrange_grid` function arranges stimuli in a grid. The `nrow` and `ncol` parameters control the number of rows and columns, respectively, and the `spH` and `spW` parameters control the horizontal and vertical spacing between stimuli.

```python
from cogpy import stimBoxes
from psychopy import core, visual

# open window
win = visual.Window(size=[1600,900],color=[1,1,1], fullscr=False)

circle_boxes = stimBoxes(win, setsize = 6, width = 0.16)
circle_boxes.arrange_grid(nrow=3, ncol=2, spH=0.05, spW=0.05)
circle_boxes.stim_text(text = ['A','B','C','D','E','F'], height = 0.12, color="#bababa")

circle_boxes.draw()

win.flip()
core.wait(20)
```

### Random

The `arrange_random` function arranges stimuli randomly. The `width` and `height` parameters control the width and height of the area in which the stimuli are placed, and the `spacing` parameter controls the minimum distance between stimuli.

```python
from cogpy import stimBoxes
from psychopy import core, visual

# open window
win = visual.Window(size=[1600,900],color=[1,1,1], fullscr=False)

circle_boxes = stimBoxes(win, setsize = 6, width = 0.05)
circle_boxes.arrange_random(width = 0.6, height = 0.6, spacing=0.01)
circle_boxes.stim_text(text = ['A','B','C','D','E','F'], height = 0.04, color="#bababa")

circle_boxes.draw()

win.flip()
core.wait(20)
```

### Custom

The `arrange_custom` function allows users to specify the positions of stimuli manually. The `positions` parameter should be a dictionary with the `Pi` (e.g., P1, P2, P3) as keys and the positions as values.

```python
from cogpy import stimBoxes
from psychopy import core, visual

# open window
win = visual.Window(size=[1600,900],color=[1,1,1], fullscr=False)

circle_boxes = stimBoxes(win, setsize = 6, width = 0.12)
circle_boxes.arrange_custom(positions = {
    'P1':[-0.3,0.3],
    'P2':[0.3,0.3],
    'P3':[-0.3,-0.3],
    'P4':[0.3,-0.3],
    'P5':[0,0.3],
    'P6':[0,-0.3]}
    )
circle_boxes.stim_text(text = ['A','B','C','D','E','F'], height = 0.08, color="#bababa")

circle_boxes.draw()
core.wait(20)
```