" Neovim plugin to set keyboard RGB leds (using ckb-next) according to current editor mode and status.
"
" Mara Huldra 2021
" SPDX-License-Identifier: MIT
if !has('python3')
    finish
endif

if !exists("g:keyleds_pipe")
    finish
endif

" in .vimrc specify:
"     let g:keyleds_pipe="/tmp/ckbpipe001"

py3 << EOF

# TODO: wrap all the functions in a class instead of adding all these python globals (which will be global to the entire editor)

class Color:
    # input classes
    HIGHLIGHT = 'ffffffff'
    INSERT = '00ff00ff'
    VISUAL = 'ffff00ff'
    MOVEMENT = 'ff8000ff'
    REPLACE = 'ff0000ff'
    META = 'ff8080ff'
    COMMAND = 'ff00ffff'

    TOGGLE = ['000000c0', 'ffffffff']

# TODO: function keys are not part of 'all', this is kind of a hack
#   this is because they are set separately: not based on editor mode but on basis of settings (or other) toggles
class Keys:
    ALL = ['grave', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'minus', 'equal',
            'tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'lbrace', 'rbrace', 'bslash_iso',
            'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'colon', 'quote',
            'z', 'x', 'c', 'v', 'b', 'n', 'm', 'comma', 'dot', 'slash', 'space',
            'home', 'end', 'ins', 'del', 'pgup', 'pgdn', 'bspace']
    TO_INSERT = ['i','o','a','s','c','ins']
    TO_VISUAL = ['v']
    TO_REPLACE = ['r','grave']
    TO_CMD = [':']
    VISUAL_SELECTION = ['g','a','w','s','p','b']
    UNDO_REDO = ['u','period']
    MOVEMENT = ['h','l','k','j','b','w','e','0','space','home','end','page_up','page_down']
    DELETION = ['x','d','del']
    REGISTER = ['quote','y','p']
    SEARCH = ['forward_slash','n']
    FUNC = ['f1','f2','f3','f4','f5','f6','f7','f8','f9','f10','f11','f12']
    MODKEYS = ['lctrl','rctrl','lshift','rshift']

def keyboard_set(colors_in):
    ckb_pipe = vim.eval('g:keyleds_pipe')
    with open(ckb_pipe, 'w') as f:
        for (key, value) in colors_in.items():
            f.write('rgb ' + key + ':' + value + '\n')

def set_multi(d, keys, value):
    '''For every key in keys, set the value to value in dictionary d.'''
    for key in keys:
        d[key] = value

def vim_escape(s):
    '''Escape a Python string for VIM script.'''
    return "'" + s.replace("'", "''") + "'"

def get_register(reg):
    '''Get the contents of a VIM register as Python string, an empty string if the register has no value.'''
    return vim.eval("getreg(" + vim_escape(reg) + ")")

prev_scheme = None
def set_keyboard_colors(scheme):
    global prev_scheme
    if prev_scheme == scheme:
        return

    colors = {x: '00000000' for x in Keys.ALL}
    if scheme.startswith('i'):
        set_multi(colors, ['i'], Color.HIGHLIGHT)
    elif scheme.startswith('R'):
        set_multi(colors, ['r'], Color.HIGHLIGHT)
    elif scheme in {'v','V','\x16'}:
        set_multi(colors, Keys.VISUAL_SELECTION, Color.VISUAL)
        set_multi(colors, Keys.MOVEMENT, Color.MOVEMENT)
        set_multi(colors, ['v'], Color.HIGHLIGHT)
    elif scheme.startswith('c'):
        set_multi(colors, ['colon'], Color.HIGHLIGHT)
    elif scheme.startswith('n'):
        set_multi(colors, Keys.TO_INSERT, Color.INSERT)
        set_multi(colors, Keys.TO_VISUAL, Color.VISUAL)
        set_multi(colors, Keys.TO_REPLACE, Color.REPLACE)
        set_multi(colors, Keys.UNDO_REDO + Keys.DELETION + Keys.REGISTER, Color.META)
        set_multi(colors, Keys.SEARCH, Color.META)
        set_multi(colors, Keys.MODKEYS, Color.VISUAL)
        set_multi(colors, Keys.TO_CMD, Color.COMMAND)
        set_multi(colors, Keys.MOVEMENT, Color.MOVEMENT)
    elif scheme == 'registers':
        for k in Keys.ALL:
            if len(k) == 1:
                if get_register(k):
                    colors[k] = Color.HIGHLIGHT
    elif scheme == 'reset': # reset to default on exit
        set_multi(colors, Keys.FUNC, '00000000')

    keyboard_set(colors)
    prev_scheme = scheme

toggles = []
def set_toggle_color(ckbkey, setting):
    '''Set toggle key color based on current seting value.'''
    # TODO another, maybe more elegant way to get and set settings is through
    #     vim.current.buffer.options[setting]   (buffer-local and global-local options)
    #     vim.current.window.options[setting]   (window options)
    #     vim.options                           (global options)
    # this needs more work to distinguish at which level options exist, though
    color = Color.TOGGLE[int(vim.eval('&' + setting))]
    keyboard_set({ckbkey: color})

def update_all_toggles():
    '''Update all toggle leds to their current option setting.'''
    global toggles
    for (vimkey, ckbkey, setting) in toggles:
        set_toggle_color(ckbkey, setting)

def setup_toggle(vimkey, ckbkey, setting):
    global toggles
    vim.command('nnoremap ' + vimkey + ' :py3 do_toggle(' + vim_escape(ckbkey) + ', ' + vim_escape(setting) + ')<CR>')
    vim.command('inoremap ' + vimkey + ' \<C-O>:py3 do_toggle(' + vim_escape(ckbkey) + ', ' + vim_escape(setting) + ')<CR>')
    #set_toggle_color(ckbkey, setting)
    toggles.append((vimkey, ckbkey, setting))

def do_toggle(ckbkey, setting):
    '''Toggle setting `setting` and update its led.'''
    vim.command(':set ' + setting + '!')
    set_toggle_color(ckbkey, setting)
    vim.command(':set ' + setting + '?')

EOF

augroup KeyboardColorSwap
    autocmd!
    " reset on exit
    autocmd VimLeave * py3 set_keyboard_colors('reset')
    " make sure fX toggle leds are updated to current buffer's state
    autocmd BufEnter * py3 update_all_toggles()
augroup END

function! OpenRGBStatuslineFunc()
  py3 set_keyboard_colors(vim.eval('mode()'))
  return ''
endfunction

set statusline=%<%f\ %h%m%r%=%-14.(%l,%c%V%)\ %P
set statusline+=%{OpenRGBStatuslineFunc()}

py3 << EOF

# TODO: initalize this from a vim g:led_toggles
setup_toggle('<F1>', 'f1', 'hlsearch')
setup_toggle('<F3>', 'f3', 'wrap')
setup_toggle('<F4>', 'f4', 'list')
setup_toggle('<F9>', 'f9', 'hidden')
setup_toggle('<F10>', 'f10', 'scrollbind')
setup_toggle('<F11>', 'f11', 'ignorecase')
setup_toggle('<F12>', 'f12', 'paste')
# TODO: some way to do the non-trivial toggles too:
# need a way to pass custom "probe" and "set" functions
# nnoremap <F5> :call VEToggle()<CR>
# nnoremap <F6> :TagbarToggle<CR>
# nnoremap <F7> :call TabMode()<CR>
# nnoremap <F8> :NERDTreeToggle %:h<CR>

EOF

" Show register staus when using ", q and @
function <SID>ShowRegisters(arg)
  py3 set_keyboard_colors('registers')
  return a:arg
endfunction
nnoremap <expr> " <SID>ShowRegisters('"')
vnoremap <expr> " <SID>ShowRegisters('"')
nnoremap <expr> q <SID>ShowRegisters('q')
vnoremap <expr> q <SID>ShowRegisters('q')
nnoremap <expr> @ <SID>ShowRegisters('@')
vnoremap <expr> @ <SID>ShowRegisters('@')

