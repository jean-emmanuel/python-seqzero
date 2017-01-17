# OSC API

### `/Sequencer/Play `

Method : `play()`

Make the sequencer play and read enabled sequnces

### `/Sequencer/Resume `

Method : `resume()`

Make the sequencer play from where it stopped

### `/Sequencer/Stop `

Method : `stop()`

Stop the sequencer

### `/Sequencer/Trigger `

Method : `trig()`

Reset the sequencer's cursor on next beat : sequences restart from beginning

### `/Sequencer/Bpm bpm`

Method : `set_bpm(bpm)`

Set the sequencer's bpm
- bpm: integer

### `/Sequencer/Sequence/Toggle name state`

Method : `sequence_toggle(name, state)`

Toggle a sequence's state

Args:
name  (str): sequence's name
state (int): 0 or 1

### `/Sequencer/Sequence/Enable name`

Method : `sequence_enable(name)`

Enable a sequence

Args:
name  (str): sequence's name

### `/Sequencer/Sequence/Disable name`

Method : `sequence_disable(name)`

Disable a sequence

Args:
name (str): sequence's name
set to '*' to stop all

### `/Sequencer/Scene/Play name`

Method : `scene_play(name)`

Start a scene (restart it if its already playing)

Args:
name (str): scenes's name

### `/Sequencer/Scene/Stop name`

Method : `scene_stop(name)`

Stop a scene

Args:
name (str): scenes's name
set to '*' to stop all

### `/Sequencer/Log message`

Method : `log(message)`

Log something in the console

Args:
message: anything

### `/Sequencer/DisableAll `

Method : `disable_all()`

Disable all sequences and stop all scenes

