#!/usr/bin/env python3
# Mara Huldra & Kvaciral 2021
# SPDX-License-Identifier: MIT
import argparse
import math
import sys
import psutil
import time

from ckbpipe import CKBPipe

class Handler:
    def __init__(self, ckb):
        self.ckb = ckb

    def set_lightbar(self, color, memory_usage=100, threshold=0):
        urgency = math.ceil(abs(threshold - memory_usage) / ((100 - threshold) / 10))
        lightbar_scope = {}

        for bar_n in range(1,16):
            lightbar_scope["topbar" + str(bar_n)] = "00000000"

        for scope in range(urgency):
            lightbar_scope["topbar" + str(10 - scope)] = color          
            lightbar_scope["topbar" + str(10 + scope)] = color

        self.ckb.set(lightbar_scope)

def parse_args():
    '''Parse command line arguments.'''
    parser = argparse.ArgumentParser(description="Use K95's lightbar to warn user of system's memory usage if equal or greater than given threshold")

    parser.add_argument('--ckb-pipe', '-c', required=True, help='The ckb-pipe-socket (/tmp/ckbpipeNNN')
    parser.add_argument('--set-color', '-col', required=True, help='The warning-color')
    parser.add_argument('--set-threshold', '-t', type=int, default=75, help='The memory-usage threshold in percentage')

    return parser.parse_args()

def main():
    args = parse_args()
    ckb = CKBPipe(args.ckb_pipe)
    handler = Handler(ckb)
    color = args.set_color + "ff"
    threshold = args.set_threshold

    while True:
        memory_usage = psutil.virtual_memory()[2]

        if memory_usage >= threshold:
            handler.set_lightbar(color, memory_usage, threshold)
        else:
            handler.set_lightbar("00000000")

        time.sleep(5)

if __name__ == '__main__':
    main()
