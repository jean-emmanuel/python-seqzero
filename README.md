# seqzero

The minimalist headless osc sequencer that does the job

It is written in [python](https://www.youtube.com/watch?v=asUyK6JWt9U), you'll need to write some simple code to set it up.

## Concepts

### `sequencer`

- has a `bpm`
- is *step-by-step*, with *substeps*
- loops through `sequences` of arbitrary lengths
- plays/stops `scenes`
- is controllabe via osc
- is *not* real-time (see `timer` below)

### `sequences`

- are named
- can be `enabled/disabled/toggled`
- can be added via osc using `JSON` notation
- are `lists` (`[]`) of steps, which can be
    - `messages`
    - `lists` of `messages` to be sent at the same time
    - `False` or `None` for empty steps
    - `tuples` (`()`) of substeps that will divide the beat evenly

### `messages`

- are `lists` (`[]`) of arguments
    - [optional] port `number` or target (`ip:port` string). If omitted, the sequencer's default target will be used)
    - osc `address` string (`/a/b/c`)
    - osc arguments

### `scenes`

- are named
- are threaded `python` scripts that are executed outside the `sequencer` loop
- take the `sequencer` object as argument and can access its methods, including some helper functions (ie to interpolate values), and a `timer` object which provides an accurate `wait` method.
- are defined in a separated module file which is provided to the sequencer
- can't run multiple times concurrently (playing a scene that is already playing makes it stop and start from the beginning)

### `timer`

The timer compensates for python's timing innaccuracy by measuring the time elasped between two calls to its `wait` method and substracting it from the 2'nd `wait`'s duration.

The sequencer's timing critical methods (`/play`, `/scene/play`) support an optional extra osc timestamp argument meant for compensating the network latency, it must be an osc timetag (osc type 't') as returned by liblo's `time()`.

Long story short: seqzero may be late, but will catch up on the first occasion.

## Requirements

- `python` 2.7+ / 3
- `python-liblo`

*Tested on gnu/linux only*

## Getting started

See [examples](examples/) (more docs to come...)

## OSC API

See [API](API.txt) (osc addresses are case-insensitive)

## Licence

[GNU/GPLv3](LICENSE)
