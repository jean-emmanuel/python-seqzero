# seqzero

The minimalist headless osc sequencer that does the job

It is written in [python](https://www.youtube.com/watch?v=asUyK6JWt9U), you'll need to write some simple code to set it up.

## Concepts

### `sequencer`

- has a `bpm`
- is *step-by-step*
- play/stop `sequences`
- play/stop `scenes`
- is controllabe via osc
- is *not* real-time

### `sequences`

- are named
- are `lists` (`[]`) of steps, which can be
    - `messages` written as `lists`: `['/path', arg1, arg2]`
    - `lists` of `messages` to be sent at the same time: `[['/path_1', arg1], ['/path_2', arg2]]`
    - `False` or `None` for empty steps
    - `tuples` (`()`) of substeps that will divide the beat evenly

### `scenes`

- are named
- are threaded `python` scripts that are executed outside the `sequencer` loop
- take the `sequencer` object as argument and can access its methods, including some helper functions (ie to interpolate value, ), and a `timer` object which provides an accurate timing method.
- are defined in a separated module file which is provided to the sequencer
- can't run multiple times concurrently (playing a scene that is already playing makes it stop and start from the beginning)

## Requirements

- `python` 2.7+
- `python-liblo`

*Tested on gnu/linux only*

## Getting started

See [examples](examples/) (more docs to come...)

## OSC API

See [API](API.txt) (osc addresses are case-insensitive)

## Licence

[GNU/GPLv3](LICENSE)
