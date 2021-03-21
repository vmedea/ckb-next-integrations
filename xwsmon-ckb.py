#!/usr/bin/env python3
# Workspace switch monitor for ckb-next. This will highlight the key associated with the current workspace.
# This needs the "pipe" animation to be configured in the ckb-next GUI.
#
# Mara Huldra 2021 :: SPDX-License-Identifier: MIT
import argparse
import sys

import Xlib.display
from Xlib import X

from ckbpipe import CKBPipe

# Names of keys to highlight for workspaces.
DEFAULT_KEYS = [
    "g1", "g2", "g3", "g4", "g5", "g6"
]

# Color for inactive, active workspace key (RRGGBBAA).
DEFAULT_COLORS = ['00000000', 'ffffffff']

def highlight_current_workspace(ckb, window, atom):
    prop = window.get_property(atom, X.AnyPropertyType, 0, 1)
    if prop is None:
        print("<3>Failed to get current desktop number", file=sys.stderr)
        return
    if len(prop.value) != 1 or prop.bytes_after != 0 or prop.format != 32:
        print(f"<3>Unexpected number of items ({len(prop.value)}) or remaining bytes ({prop.bytes_after}) or format ({prop.format})", file=sys.stderr)
        return

    desktop_id = prop.value[0]
    print(f"<7>Switch to workspace {desktop_id} detected");

    try:
        ckb.set({key: DEFAULT_COLORS[desktop_id == i] for (i, key) in enumerate(DEFAULT_KEYS)})
    except IOError:
        print(f"<3>Error while opening or writing to pipe\n");

def parse_args():
    '''Parse command line arguments.'''
    parser = argparse.ArgumentParser(description='Workspace switch monitor for ckb-next')

    parser.add_argument('--ckb-pipe', '-c', required=True, help='The ckb-pipe-socket (/tmp/ckbpipeNNN')

    return parser.parse_args()

def main():
    args = parse_args()

    ckb = CKBPipe(args.ckb_pipe)
    display = Xlib.display.Display()
    atom = display.intern_atom('_NET_CURRENT_DESKTOP', True)
    window = display.screen().root

    highlight_current_workspace(ckb, window, atom)

    window.change_attributes(event_mask=X.PropertyChangeMask)

    while True:
        ev = display.next_event()
        if ev.type == X.PropertyNotify and ev.state == X.PropertyNewValue and ev.window == window and ev.atom == atom:
            highlight_current_workspace(ckb, window, atom)

if __name__ == '__main__':
    main()
