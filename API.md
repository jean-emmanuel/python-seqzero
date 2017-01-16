OSC Address | Python method | Information
----------- | ------------- | -----------
`/Sequencer/Play` | `play()` | Make the sequencer play and read enabled sequnces 
`/Sequencer/Resume` | `resume()` | Make the sequencer play from where is stopped 
`/Sequencer/Stop` | `stop()` | Stop the sequencer 
`/Sequencer/Trigger` | `trig()` | Reset the sequencer's cursor on next beat : sequences restart from beginning 
`/Sequencer/Bpm` | `set_bpm(bpm)` | Set the sequencer's bpm 
`/Sequencer/Sequence/Toggle` | `sequence_toggle(name, state)` | Toggle a sequence's state 
`/Sequencer/Sequence/Enable` | `sequence_enable(name)` | Enable a sequence 
`/Sequencer/Sequence/Disable` | `sequence_disable(name)` | Disable a sequence 
`/Sequencer/Scene/Play` | `scene_play(name)` | Start a scene (restart it if its already playing) 
`/Sequencer/Scene/Stop` | `scene_stop(name)` | Stop a scene 
`/Sequencer/Log` | `log(*message)` | Log something in the console 
`/Sequencer/DisableAll` | `disable_all()` | Disable all sequences and stop all scenes 
