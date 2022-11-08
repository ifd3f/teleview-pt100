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
    Key('sym_' + urllib.parse.quote(k, safe=''), f'{k}   {s}', SIZE_1SYM, 1)
    for k, s in zip(SYMS1, SYMS2)]

fns = [
    Key(f'f{n}', f'F{n}', SIZE_1SYM, 1.25)
    for n in range(1, 8)
]

misc = [
    Key('dial', 'DIAL/DC', SIZE_TEXT, 1.25),
    Key('exit', 'NSCR/EXIT', SIZE_TEXT, 1.25),

    Key('esc', 'LOC/ESC', SIZE_TEXT, 1.25),
    Key('backspace', 'BSPACE', SIZE_1SYM, 1.25),

    Key('tab', 'TAB', SIZE_TEXT, 2),
    Key('clear', 'CLEAR', SIZE_TEXT, 2),

    Key('ctrl', 'CTRL', SIZE_TEXT, 1),
    Key('alock', 'ALOCK', SIZE_TEXT, 1),
    Key('return', 'RETURN', SIZE_TEXT, 2),  # temporary ansi-style

    Key('lshift', 'SHIFT', SIZE_TEXT, 2),
    Key('rshift', 'SHIFT', SIZE_TEXT, 2),
    Key('del', 'DEL', SIZE_TEXT, 2),

    Key('send', 'SEND', SIZE_TEXT, 1.25),
    Key('print', 'PRINT', SIZE_TEXT, 1.25),
    Key('space', '', SIZE_1SYM, 6.25),

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

procs = []

for k in all_keys:
    text_esc = k.text.replace('"', r'\"')
    cmd = ['openscad', '-o', f'{OUTDIR}/{k.name}.stl', '-D', f'key_length={k.u}', '-D',
           f'key_text="{text_esc}"', '-D', f'key_text_fontsize={k.font_size}', 'key.scad']
    print('Executing command', cmd)
    procs.append(Popen(cmd))

for p in procs:
    p.wait()

print()
print('Done!')

