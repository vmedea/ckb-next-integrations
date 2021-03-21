#!/usr/bin/env python3
# Mara Huldra & Kvaciral 2021
# SPDX-License-Identifier: MIT
import argparse
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
import sys

from ckbpipe import CKBPipe

# media keys:
KEYS =               ['stop',      'prev',     'play',    'next']
# statuses:
BY_STATUS = {
    'Stopped':      ['ffffffff', '00000000', '00000000', '00000000'],
    'Playing':      ['00000000', '00000000', 'ffffffff', '00000000'],
    'Paused':       ['00000000', '00000000', '000000ff', '00000000'],
    'Player_Gone':  ['00000000', '00000000', '00000000', '00000000'],
}

class Handler:
    def __init__(self, ckb, media_player):
        self.media_player = "org.mpris.MediaPlayer2." + media_player
        self.ckb = ckb

    def _set_status(self, status):
        colors = BY_STATUS[status]
        self.ckb.set({key: color for (key, color) in zip(KEYS, colors)})

    def properties_changed(self, iface, changed, invalidated):
        if 'PlaybackStatus' in changed:
            print(f"<7>New playback status: {changed['PlaybackStatus']}", file=sys.stderr)
            self._set_status(changed['PlaybackStatus'])

    def name_owner_changed(self, name, old, new):
        if name == self.media_player and new == "":
            print("<7>Media player disappeared", file=sys.stderr)
            self._set_status('Player_Gone')

def parse_args():
    '''Parse command line arguments.'''
    parser = argparse.ArgumentParser(description='Music player status display with ckb-next')

    parser.add_argument('--ckb-pipe', '-c', required=True, help='The ckb-pipe-socket (/tmp/ckbpipeNNN')
    parser.add_argument('--media-player', '-p', required=True, help='The media player to be monitored')

    return parser.parse_args()

def main():
    args = parse_args()
    ckb = CKBPipe(args.ckb_pipe)
    handler = Handler(ckb, args.media_player)

    DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()
    bus.add_signal_receiver(handler.properties_changed,
        dbus_interface='org.freedesktop.DBus.Properties',
        signal_name='PropertiesChanged',
        arg0 = "org.mpris.MediaPlayer2.Player",
    )
    bus.add_signal_receiver(handler.name_owner_changed,
        dbus_interface='org.freedesktop.DBus',
        signal_name='NameOwnerChanged',
        bus_name='org.freedesktop.DBus',
    )
    loop = GLib.MainLoop()
    loop.run()

if __name__ == '__main__':
    main()
