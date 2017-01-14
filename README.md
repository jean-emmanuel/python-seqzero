# seqzero

The minimalist headless osc sequencer that does the job

It is written in [python](https://www.youtube.com/watch?v=asUyK6JWt9U), you'll need to write some simple code to set it up.

## Concepts

### `sequencer`

- has a `bpm`
- play/stop `sequences`
- play/stop `scenes`
- is controllabe via osc
- it is not real-time
- it compensates its own latency: it's not very accurate but its error dont grow

### `sequences`

- are `arrays` (`[]`) of steps `arrays`, whose items can be
    - `messages` written as `arrays`: `['/path', arg1, arg2]`
    - `arrays` of `messages` to be sent at the same time: `[['/path_1', arg1], ['/path_2', arg2]]`

### `scenes`

- are theaded `python` scripts that are executed outside the `sequencer` loop
- they take `sequencer` object as argument and can access its methods, including some helper functions (ie to interpolate value, )
- they are named
- they are defined in a separated module file which is provided to the sequencer


## Requirements

- `python` 2.7+
- `python-liblo`

## Getting started

See [examples](examples/) (more docs to come...)

## OSC API

```
OSC address                   expected args         explanation
===============================================================
/Sequencer/Play               None
/Sequencer/Stop               None
/Sequencer/Trigger            None
/Sequencer/Bpm                integer
/Sequencer/Sequence/Toggle    string integer        [sequence's name, 0/1 to disable/enable ]
/Sequencer/Sequence/Enable    string                sequence's name
/Sequencer/Sequence/Disable   string                sequence's name
/Sequencer/DisableAll         None
/Sequencer/Scene/Play         string                scene's name
/Sequencer/Scene/Stop         string                scene's name
/Sequencer/Debug              None
```
