import xtrack as xt

import json
import numpy as np

fname = 'sler_1705_60_06_cw50_4b.json'

with open(fname, 'r') as fid:
    d = json.load(fid)

elements = {}

# drift
drifts = d['drift']
for nn, vv in drifts.items():
    assert len(vv.keys()) == 1
    elements[nn] = xt.Drift(length=vv['l'])

# bends
bends = d['bend']
bends_off = []
bends_on = []
for nn, vv in bends.items():
    if vv['angle'] == 0:
        bends_off.append(nn)
    else:
        bends_on.append(nn)

for nn in bends_off:
    vv = bends[nn]
    if 'l' in vv:
        elements[nn] = xt.Drift(length=vv['l'])
    else:
        elements[nn] = xt.Marker

for nn in bends_on:
    vv = bends[nn]

    length = vv['l']
    angle = vv['angle']
    h = angle / length
    k0 = h

    oo = []
    if 'rotate' in vv:
        assert vv['rotate'] == 90 or vv['rotate'] == -90
        oo.append(xt.SRotation(angle=-vv['rotate']))

    if 'e1' in vv:
        # assert vv['fringe'] == 1 # we put fringes everywhere (check what happens if fringe is not there)
        oo.append(xt.DipoleEdge(k=k0, e1=vv['e1']*angle,
                                hgap=1/6, #linear drop-off (see madx manual)
                                fint=vv['f1'],
                                side='entry'))

        oo.append(xt.Bend(k0=k0, h=h, length=length))

        oo.append(xt.DipoleEdge(k=k0, e1=vv['e1']*angle,
                                hgap=1/6, #linear drop-off (see madx manual)
                                fint=vv['f1'],
                                side='exit'))

    if 'rotate' in vv:
        oo.append(xt.SRotation(angle=vv['rotate']))

    elements[nn] = oo

for nn, vv in d['quad'].items():

    if 'rotate' in vv:
        assert np.abs(vv['rotate']) == 45
        # TODO: neglecting skew for not
        elements[nn] = xt.Drift(length=vv['l'])
    elements[nn] = xt.Quadrupole(length=vv['l'], k1=vv['k1'])
    # TODO: neglecting fringes for now

for nn, vv in d['mult'].items():
    # TODO neglecting multipoles for now
    elements[nn] = xt.Drift(length=vv.get('l', 0))

for nn, vv in d['oct'].items():
    assert 'l' not in vv
    # TODO neglecting octupoles for now
    elements[nn] = xt.Marker()

for nn, vv in d['cavi'].items():
    assert 'l' not in vv
    # TODO neglecting cavities for now
    elements[nn] = xt.Marker()




