import json
fname = 'sler_1705_60_06_cw50_4b.plain.sad'

with open(fname, 'r') as f:
    content = f.read()

content = content.lower() # make it lower case

new_lines = []
for il, ll in enumerate(content.split('\n')):
    lll = ll.strip() # remove leading and trailing spaces
    if lll.startswith('momentum'):
        continue
    if lll.startswith('fshift'):
        continue
    if lll.startswith('line'):
        break
    new_lines.append(lll)

content = '\n'.join(new_lines)

if content[0] == ';':
    content = content[1:] # remove first ';'

content = content.split('line')[0] # remove everything after 'line'

content = content.replace('(', 'dict(').replace(')', '),')
content = content.replace('deg', '')
content = content.replace(';', '),')

while ' =' in content:
    content = content.replace(' =', '=')

while '= ' in content:
    content = content.replace('= ', '=')

while '  ' in content:
    content = content.replace('  ', ' ')

lines = content.split('\n')
for il, ll in enumerate(lines):
    tokens = ll.split(' ')
    for it, tt in enumerate(tokens):
        if '=' in tt:
            tokens[it] = tt + ','
    lines[il] = ' '.join(tokens)
content = '\n'.join(lines)
content ='dict(\n' + content + '\n)'

for command in ('drift', 'bend', 'quad', 'oct', 'mult', 'sol', 'cavi',
                'mark', 'moni', 'beambeam', 'apert'):
    content = content.replace(command, f'{command}=dict(')

while ',,' in content:
    content = content.replace(',,', ',')

with open(fname.replace('.plain.sad', '.py'), 'w') as f:
    f.write(content)

d = eval(content)

# save as json
with open(fname.replace('.plain.sad', '.json'), 'w') as f:
    json.dump(d, f, indent=2)