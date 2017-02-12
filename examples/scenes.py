def a(sequencer, timer):
    sequencer.send('/scenes/a', 1)
    # wait 3 beats
    timer.wait(3)
    sequencer.send('/scenes/a', 2)

def b(sequencer, timer):
    sequencer.animate('/scenes/b', start=1, end=10, duration=1)
    sequencer.animate('/scenes/c', start=1, end=10, duration=1)
