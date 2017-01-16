import re

source = open('../sequencer.py', 'r').read()

doc = '# OSC API\n\n'

def parse(m):
    global doc

    method  = m.group(4).replace('def ','').replace('self, ','').replace('self','').replace('):',')').replace('*','').strip()
    address = '/Sequencer' + str(eval(m.group(2).replace(')',',)') )[0]).strip() + ' ' + method[method.index('(')+1:method.index(')')].replace(',','')
    info    = m.group(5).strip().replace('    ','')

    doc += '### `%s`\n\n' % address
    doc += 'Method : `%s`\n\n' % method
    doc += '%s\n\n' % info


re.sub('(@API)([^"\n]*)([^"\n]*)([^"]*)"""([^"]*)"""', parse, source, flags=re.M)

file = open('../API.md', 'w')
file.write(doc)
file.close()
