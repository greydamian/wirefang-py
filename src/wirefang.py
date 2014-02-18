#! /usr/bin/env python

from __future__ import print_function

import sys    # argv
import os     # geteuid
import socket # socket

__version__ = 'v1.0.0'
__authors__ = 'Damian Jason Lapidge <grey@greydamian.org'
__license__ = '''Copyright (c) 2014 Damian Jason Lapidge

The contents of this file are subject to the terms and conditions defined 
within the file LICENSE.txt, located within this project's root directory.
'''

def print_usage():
    print('usage: wirefang-py <file> <interface>', file=sys.stderr)

def create_rawsock(iface):
    sock = socket.socket(socket.AF_PACKET, 
                         socket.SOCK_RAW, 
                         socket.htons(socket.SOCK_RAW))
    sock.bind((iface, socket.SOCK_RAW))
    return sock

def main(args):
    if os.geteuid() > 0:
        print('error: this program requires superuser privilages', 
              file=sys.stderr)
        return 1 # exit failure

    if len(args) < 3:
        print_usage()
        return 1 # exit failure

    fpath = args[len(args) - 2]
    iface = args[len(args) - 1]

    try:
        sock = create_rawsock(iface)
    except:
        print('error: failure to create network connection', file=sys.stderr)
        return 1 # exit failure

    try:
        f = open(fpath, 'rb')
    except:
        print('error: failure to open file (' + str(fpath) + ')', 
              file=sys.stderr)
        return 1 # exit failure

    buf = f.read()
    f.close()

    sock.sendall(buf)
    sock.close()

    return 0 # exit success

if __name__ == '__main__':
    sys.exit(main(sys.argv))
