OSC Address | Python method | Information
----------- | ------------- | -----------
`/Sequencer/Play` | `play()` | Make the sequencer play and read enabled sequnces 
`/Sequencer/Resume` | `resume()` | Make the sequencer play from where it stopped 
`/Sequencer/Stop` | `stop()` | Stop the sequencer 
`/Sequencer/Trigger` | `trig()` | Reset the sequencer's cursor on next beat : sequences restart from beginning 
`/Sequencer/Bpm` | `set_bpm(bpm)` | Set the sequencer's bpm
        - bpm: integer 
`/Sequencer/Sequence/Toggle` | `sequence_toggle(name, state)` | Toggle a sequence's state
        - name: string
        - state: integer (0/1) 
`/Sequencer/Sequence/Enable` | `sequence_enable(name)` | Enable a sequence
        - name: string 
`/Sequencer/Sequence/Disable` | `sequence_disable(name)` | Disable a sequence
        - name: string 
`/Sequencer/Scene/Play` | `scene_play(name)` | Start a scene (restart it if its already playing)
        - name: string 
`/Sequencer/Scene/Stop` | `scene_stop(name)` | Stop a scene
        - name: string 
`/Sequencer/Log` | `log(*message)` | Log something in the console
        - *message: anything 
`/Sequencer/DisableAll` | `disable_all()` | Disable all sequences and stop all scenes 
