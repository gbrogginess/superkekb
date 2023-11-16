import json
fname = 'sler_1705_60_06_cw50_4b.plain.sad'
fname = 'sler_1707_80_1_simple.sad'

with open(fname, 'r') as f:
    content = f.read()

content = content.lower() # make it lower case

while ' =' in content:
    content = content.replace(' =', '=')

while '= ' in content:
    content = content.replace('= ', '=')

while '  ' in content:
    content = content.replace('  ', ' ')

content = content.replace('deg', '')

sections = content.split(';')
out = {}
for ss in sections:
    ss_py = ss
    ss_py = ss_py.strip()

    if len(ss_py) == 0:
        continue

    ss_command = ss_py.split()[0]
    if ss_command in ('drift', 'bend', 'quad', 'oct', 'mult', 'sol', 'cavi',
                'mark', 'moni', 'beambeam', 'apert'):
        ss_py = ss_py.replace('(', 'dict(').replace(')', '),')
        ss_py = ss_py.replace(ss_command, 'dict(')
        lines = ss_py.split('\n')
        for il, ll in enumerate(lines):
            tokens = ll.split(' ')
            for it, tt in enumerate(tokens):
                if '=' in tt:
                    tokens[it] = tt + ','
            lines[il] = ' '.join(tokens)
        ss_py = '\n'.join(lines)
        ss_py ='dict(\n' + ss_py + '\n)'
        while ',,' in ss_py:
            ss_py = ss_py.replace(',,', ',')

        ss_py += ')'

        out[ss_command] = eval(ss_py)

    if ss_command == 'line':
        ele_str = ss.split('=')[-1]
        ele_str = ele_str.replace('(', '')
        ele_str = ele_str.replace(')', '')
        ele_str.replace('\n', ' ')
        ele_str_list = []
        for ee in ele_str.split():
            if len(ee) > 0:
                ele_str_list.append(ee)

        out['line'] = ele_str_list

# save as json
with open(fname.replace('.plain.sad', '') + '.json', 'w') as f:
    json.dump(out, f, indent=2)