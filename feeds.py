feeds = [
    'transport'
]

def transport(sequencer):
    return {
        'bpm': sequencer.bpm,
        'cursor': sequencer.cursor
    }
