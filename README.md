ckb-next-integrations
---------------------

Plugins and daemons for keyboard RGB led functionality, through [ckb-next](https://github.com/ckb-next/ckb-next).

This repository currently contains the following integrations. All of them communicate with `ckb-next` through a FIFO created by the `pipe` animation, which are named `/tmp/ckbpipe???`. To use multiple integrations at the same time, it is best to create multiple pipe animations covering different keys, this will prevent them from stepping on each other's toes.

- `xwsmon-ckb.py`: Colorizes G1..G6 keys on Corsair led keyboard according to current X workspace.
- `music-player-events-ckb.py`: Colorize media keys according the current status of a media player conforming to the [Freedesktop MPRIS spec](https://specifications.freedesktop.org/mpris-spec/latest/).
- `keyleds-ckb.vim`: Neovim plugin to colorize keys according to current editor mode and status. 

Note: these have only been tested on Corsair K95 Platinum keyboards. They may or may not work on others.
