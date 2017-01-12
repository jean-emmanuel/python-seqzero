from pyOSCseq import *


def scenes_list(sequencer, name):
	send = sequencer.parseOscArgs
	animate = sequencer.animate
	repeat = sequencer.repeat
	if name == 'a':
		animate(0,10,2,.1,send,['/testa'])

	if name == 'b':
		send(['/b','start'])
		sleep(1)
		send(['/b','mid'])
		sleep(1)
		send(['/b','end'])


m_seq = pyOSCseq(110, 3333, 'localhost:6666',scenes_list)


print "Launching the main sequencer"
# m_seq.play()
raw_input()
