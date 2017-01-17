import re

source = open('../sequencer.py', 'r').read()

doc = '# OSC API\n\n'

def parse(m):
    global doc

    method  = m.group(4).replace('def ','').replace('self, ','').replace('self','').replace('):',')').replace('*','').strip()
    address = '/Sequencer' + str(eval(m.group(2).replace(')',',)') )[0]).strip() + ' ' + method[method.index('(')+1:method.index(')')].replace(',','')
    info    = m.group(5).strip().replace('        ','    ')

    doc += '-' * 80 + '\n'
    doc += 'Address: ' + address + '\n'
    doc += 'Method : ' + method  + '\n\n'
    doc += info + '\n\n'


re.sub('(@API)([^"\n]*)([^"\n]*)([^@"]*)"""([^"]*)"""', parse, source, flags=re.M)

file = open('../API.txt', 'w')
file.write(doc)
file.close()
