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
        The key names can be found in this structure in ckb-next's source code:
        https://github.com/ckb-next/ckb-next/blob/master/src/gui/keymap.cpp#L16
        '''
        with open(self.filename, 'w') as f:
            for (key, value) in colors_in.items():
                f.write('rgb ' + key + ':' + value + '\n')
