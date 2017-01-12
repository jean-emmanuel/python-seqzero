def a(sequencer):
    sequencer.send('/scenes/a', 1)
    # wait 3 beats
    sequencer.wait(3)
    sequencer.send('/scenes/a', 2)

def b(sequencer):
    sequencer.animate('/scenes/b', start=1, end=10, duration=1)
