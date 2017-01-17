feeds = [
    'transport',
    'sequences',
    'scenes'
]

def transport(sequencer):
    return {
        'bpm': sequencer.bpm,
        'cursor': sequencer.cursor,
        'playing': sequencer.playing
    }

def sequences(sequencer):
    data = {}

    for name in sequencer.sequences:
        data[name] = {
            'steps': sequencer.sequences[name].steps,
            'playing': sequencer.sequences[name].playing
        }

    return data

def scenes(sequencer):
    data = {}

    for name in sequencer.scenes_list_names:
        data[name] = {
            'playing': name in sequencer.scenes and sequencer.scenes[name].is_alive()
        }

    return data
