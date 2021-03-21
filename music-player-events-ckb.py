#!/usr/bin/env python3
# Mara Huldra & Kvaciral 2021
# SPDX-License-Identifier: MIT
import argparse
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
import sys

# media keys:
KEYS =               ['stop',      'prev',     'play',    'next']
# statuses:
BY_STATUS = {
    'Stopped':      ['ffffffff', '00000000', '00000000', '00000000'],
    'Playing':      ['00000000', '00000000', 'ffffffff', '00000000'],
    'Paused':       ['00000000', '00000000', '000000ff', '00000000'],
    'Player_Gone':  ['00000000', '00000000', '00000000', '00000000'],
}

def properties_changed(iface, args, _):
    global last_sender

    if 'PlaybackStatus' in args:
        print(args['PlaybackStatus'])
        colors = BY_STATUS[args['PlaybackStatus']]

        keyboard_set({key: color for (key, color) in zip(KEYS, colors)})

def name_owner_changed(name, old, new):
    media_player = "org.mpris.MediaPlayer2." + args.media_player

    if name == media_player and new == "":
        print('media player disappeared')
        colors = BY_STATUS['Player_Gone']
        keyboard_set({key: color for (key, color) in zip(KEYS, colors)})

def keyboard_set(colors_in):
    with open(args.ckb_pipe, 'w') as f:
        for (key, value) in colors_in.items():
            f.write('rgb ' + key + ':' + value + '\n')

def parse_args():
    '''Parse command line arguments.'''
    parser = argparse.ArgumentParser(description='Music player status display with ckb-next')

    parser.add_argument('--ckb-pipe', '-c', help='The ckb-pipe-hook (/tmp/ckbpipe...)')
    parser.add_argument('--media-player', '-p', help='The media player to be monitored')

    return parser.parse_args()

def main():
    global args 

    args = parse_args()

    DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()
    bus.add_signal_receiver(properties_changed,
        dbus_interface='org.freedesktop.DBus.Properties',
        signal_name='PropertiesChanged',
        arg0 = "org.mpris.MediaPlayer2.Player",
    )
    bus.add_signal_receiver(name_owner_changed,
        dbus_interface='org.freedesktop.DBus',
        signal_name='NameOwnerChanged',
        bus_name='org.freedesktop.DBus',
    )
    loop = GLib.MainLoop()
    loop.run()

if __name__ == '__main__':
    main()
