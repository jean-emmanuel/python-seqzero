# OSC API

### `/Sequencer/Play`

Method : `play()`

Make the sequencer play and read enabled sequnces

### `/Sequencer/Resume`

Method : `resume()`

Make the sequencer play from where it stopped

### `/Sequencer/Stop`

Method : `stop()`

Stop the sequencer

### `/Sequencer/Trigger`

Method : `trig()`

Reset the sequencer's cursor on next beat : sequences restart from beginning

### `/Sequencer/Bpm`

Method : `set_bpm(bpm)`

Set the sequencer's bpm
- bpm: integer

### `/Sequencer/Sequence/Toggle`

Method : `sequence_toggle(name, state)`

Toggle a sequence's state
- name: string
- state: integer (0/1)

### `/Sequencer/Sequence/Enable`

Method : `sequence_enable(name)`

Enable a sequence
- name: string

### `/Sequencer/Sequence/Disable`

Method : `sequence_disable(name)`

Disable a sequence
- name: string

### `/Sequencer/Scene/Play`

Method : `scene_play(name)`

Start a scene (restart it if its already playing)
- name: string

### `/Sequencer/Scene/Stop`

Method : `scene_stop(name)`

Stop a scene
- name: string

### `/Sequencer/Log`

Method : `log(*message)`

Log something in the console
- message: anything

### `/Sequencer/DisableAll`

Method : `disable_all()`

Disable all sequences and stop all scenes

