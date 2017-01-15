## 01 Timeshift

Attempt to mesure the cumulated error of the sequencer.
Since python's timing is not very accurate, the sequencer's timers tries to compensate its own error.

Expected result: an error between 0 and ~±1ms that doesn't grow

## 02 Metronom

Requires `python-pyo` to run.

Audio metronom; Run another one concurrently and check if it stays in sync...
