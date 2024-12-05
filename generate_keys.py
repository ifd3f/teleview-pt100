#!/usr/bin/env python3

import os
import errno
import urllib.parse
from pprint import pprint
from typing import NamedTuple
from subprocess import Popen


OUTDIR = 'out'
SIZE_1SYM = 6
SIZE_TEXT = 3


class Key(NamedTuple):
    name: str
    text: str
    font_size: float
    u: int


alpha = [
    Key(f'alph_{c}', c, SIZE_1SYM, 1)
    for c in 'QWERTYUIOPASDFGHJKLZXCVBNM'
]

SYMS1 = r"""`1234567890-=[]\;',./"""
SYMS2 = r"""~!@#$%^&*()_+{}|:"<>?"""
syms = [
    Key('sym_' + urllib.parse.quote(k, safe=''), f'{k}{s}', SIZE_1SYM, 1)
    for k, s in zip(SYMS1, SYMS2)]

fns = [
    Key(f'f{n}', f'F{n}', SIZE_1SYM, 1.25)
    for n in range(1, 8)
]

misc = [
    Key('misc_dial', 'DIAL/DC', SIZE_TEXT, 1.25),
    Key('misc_exit', 'EXIT', SIZE_TEXT, 1.25),

    Key('misc_esc', 'LOC/ESC', SIZE_TEXT, 1.25),
    Key('misc_backspace', 'BSPACE', SIZE_TEXT, 1.25),

    Key('misc_tab', 'TAB', SIZE_TEXT, 1.75),
    Key('misc_clear', 'CLEAR', SIZE_TEXT, 2),

    Key('misc_ctrl', 'CTRL', SIZE_TEXT, 1),
    Key('misc_alock', 'ALOCK', SIZE_TEXT, 1),
    Key('misc_return', 'RETURN', SIZE_TEXT, 2),  # temporary ansi-style

    Key('misc_lshift', 'SHIFT', SIZE_TEXT, 2),
    Key('misc_rshift', 'SHIFT', SIZE_TEXT, 2),
    Key('misc_del', 'DEL', SIZE_TEXT, 2),

    Key('misc_send', 'SEND', SIZE_TEXT, 1.25),
    Key('misc_print', 'PRINT', SIZE_TEXT, 1.25),
    Key('misc_space', '', SIZE_1SYM, 6.25),

    Key('arrow_u', '↑', SIZE_1SYM, 1),
    Key('arrow_d', '↓', SIZE_1SYM, 1),
    Key('arrow_l', '←', SIZE_1SYM, 1),
    Key('arrow_r', '→', SIZE_1SYM, 1),
]

all_keys = alpha + syms + fns + misc
pprint(all_keys)


try:
    os.makedirs(OUTDIR)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

cmds = []

for k in all_keys:
    text_esc = ''.join([f'\\x{ord(c):02x}' for c in k.text])
    base = [
        'openscad',
       '-D', f'key_length={k.u}',
       '-D', f'key_text="{text_esc}"',
       '-D', f'key_text_fontsize={k.font_size}',
       'key.scad'
   ]

    kcp = ['-D', 'output_keycap=true', '-D', 'output_label=false']
    lcp = ['-D', 'output_keycap=false', '-D', 'output_label=true']

    cmds.append(base + kcp + ['-o', f'{OUTDIR}/{k.name}_label.stl'])
    cmds.append(base + kcp + ['-o', f'{OUTDIR}/{k.name}_keycap.stl']) 

for c in cmds:
    print(' '.join(map(repr, c)))


procs = []
for c in cmds:
    procs.append(Popen(c))


for p in procs:
    p.wait()


print()
print(f'Finished executing {len(all_keys)} commands!')
print('merging')

