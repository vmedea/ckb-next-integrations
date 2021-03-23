# Mara Huldra 2021 :: SPDX-License-Identifier: MIT

# All leds (with their x and y coordinate) of a Corsair K95 Platinum (US layout) keyboard.
ALL_LEDS = {
    'topbar1': (4, -3), # TOPBAR1
    'topbar2': (19, -3), # TOPBAR2
    'topbar3': (34, -3), # TOPBAR3
    'topbar4': (49, -3), # TOPBAR4
    'topbar5': (64, -3), # TOPBAR5
    'topbar6': (79, -3), # TOPBAR6
    'topbar7': (94, -3), # TOPBAR7
    'topbar8': (109, -3), # TOPBAR8
    'topbar9': (124, -3), # TOPBAR9
    'topbar10': (139, -3), # TOPBAR10
    'topbar11': (154, -3), # TOPBAR11
    'topbar12': (169, -3), # TOPBAR12
    'topbar13': (184, -3), # TOPBAR13
    'topbar14': (199, -3), # TOPBAR14
    'topbar15': (214, -3), # TOPBAR15
    'topbar16': (229, -3), # TOPBAR16
    'topbar17': (244, -3), # TOPBAR17
    'topbar18': (259, -3), # TOPBAR18
    'topbar19': (274, -3), # TOPBAR19

    'profswitch': (44, 7), # Profile Switch
    'light': (55, 7), # Brightness
    'lock': (66, 7), # Windows Lock
    'mute': (242, 7), # Mute

    'g1': (2, 20), # G1
    'esc': (18, 20), # Esc
    'f1': (38, 20), # F1
    'f2': (50, 20), # F2
    'f3': (62, 20), # F3
    'f4': (74, 20), # F4
    'f5': (94, 20), # F5
    'f6': (106, 20), # F6
    'f7': (118, 20), # F7
    'f8': (130, 20), # F8
    'f9': (150, 20), # F9
    'f10': (162, 20), # F10
    'f11': (174, 20), # F11
    'f12': (186, 20), # F12
    'prtscn': (202, 20), # Print Screen SysRq
    'scroll': (214, 20), # Scroll Lock
    'pause': (226, 20), # Pause Break
    'stop': (242, 20), # Stop
    'prev': (253, 20), # Previous
    'play': (265, 20), # Play/Pause
    'next': (276, 20), # Next

    'g2': (2, 32), # G2

    'grave': (18, 33), # `
    '1': (30, 33), # 1
    '2': (42, 33), # 2
    '3': (54, 33), # 3
    '4': (66, 33), # 4
    '5': (78, 33), # 5
    '6': (90, 33), # 6
    '7': (102, 33), # 7
    '8': (114, 33), # 8
    '9': (126, 33), # 9
    '0': (138, 33), # 0
    'minus': (150, 33), # -
    'equal': (162, 33), # =
    'bspace': (180, 33), # Backspace
    'ins': (202, 33), # Insert
    'home': (214, 33), # Home
    'pgup': (226, 33), # Page Up
    'numlock': (241, 33), # Num Lock
    'numslash': (253, 33), # NumPad /
    'numstar': (265, 33), # NumPad *
    'numminus': (277, 33), # NumPad -

    'g3': (2, 44), # G3

    'tab': (21, 45), # Tab
    'q': (36, 45), # Q
    'w': (48, 45), # W
    'e': (60, 45), # E
    'r': (72, 45), # R
    't': (84, 45), # T
    'y': (96, 45), # Y
    'u': (108, 45), # U
    'i': (120, 45), # I
    'o': (132, 45), # O
    'p': (144, 45), # P
    'lbrace': (156, 45), # [
    'rbrace': (168, 45), # ]
    'bslash': (183, 45), # \
    'del': (202, 45), # Delete
    'end': (214, 45), # End
    'pgdn': (226, 45), # Page Down
    'num7': (241, 45), # NumPad 7
    'num8': (253, 45), # NumPad 8
    'num9': (265, 45), # NumPad 9

    'numplus': (277, 51), # NumPad +

    'g4': (2, 56), # G4

    'caps': (22, 57), # Caps Lock
    'a': (39, 57), # A
    's': (51, 57), # S
    'd': (63, 57), # D
    'f': (75, 57), # F
    'g': (87, 57), # G
    'h': (99, 57), # H
    'j': (111, 57), # J
    'k': (123, 57), # K
    'l': (135, 57), # L
    'colon': (147, 57), # ;
    'quote': (159, 57), # '
    'enter': (179, 57), # Enter
    'num4': (241, 57), # NumPad 4
    'num5': (253, 57), # NumPad 5
    'num6': (265, 57), # NumPad 6

    'g5': (2, 68), # G5

    'lshift': (25, 69), # Left Shift
    'z': (45, 69), # Z
    'x': (57, 69), # X
    'c': (69, 69), # C
    'v': (81, 69), # V
    'b': (93, 69), # B
    'n': (105, 69), # N
    'm': (117, 69), # M
    'comma': (129, 69), # ,
    'dot': (141, 69), # .
    'slash': (153, 69), # /
    'rshift': (176, 69), # Right Shift
    'up': (214, 69), # Up
    'num1': (241, 69), # NumPad 1
    'num2': (253, 69), # NumPad 2
    'num3': (265, 69), # NumPad 3

    'numenter': (277, 75), # NumPad Enter

    'g6': (2, 80), # G6

    'lctrl': (20, 81), # Left Ctrl
    'lwin': (34, 81), # Left Super
    'lalt': (47, 81), # Left Alt
    'space': (96, 81), # Space
    'ralt': (145, 81), # Right Alt
    'rwin': (158, 81), # Right Super
    'rmenu': (170, 81), # Menu
    'rctrl': (184, 81), # Right Ctrl
    'left': (202, 81), # Left
    'down': (214, 81), # Down
    'right': (226, 81), # Right
    'num0': (247, 81), # NumPad 0
    'numdot': (265, 81), # NumPad .
}

class CKBPipe:
    '''Interface to ckb-next 'pipe' animation.'''
    def __init__(self, filename):
        '''
        Create a new CKBPipe instance for connecting to the specified filename. This does not actually create a connection yet.
        '''
        self.filename = filename

    def set(self, colors_in):
        '''
        Set colors for keys. Pass a dictionary of `'keyname': 'RRGGBBAA'`.
        See ALL_LEDS for the key names that can be used.
        '''
        with open(self.filename, 'w') as f:
            for (key, value) in colors_in.items():
                f.write('rgb ' + key + ':' + value + '\n')
