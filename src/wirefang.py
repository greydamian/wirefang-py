#! /usr/bin/env python

from __future__ import print_function

import sys
import os
import socket

__version__ = 'v1.0.0'
__authors__ = 'Damian Jason Lapidge <grey@greydamian.org>'
__license__ = '''Copyright (c) 2015 Damian Jason Lapidge

The contents of this file are subject to the terms and conditions defined 
within the file LICENSE.txt, located within this project's root directory.
'''

def print_usage():
    """Prints command usage information to stderr."""
    print('usage: wirefang-py <file> <interface>', file=sys.stderr)

def create_rawsock(iface):
    """Creates a new raw socket object.

    The socket sends/receives data at the link layer (TCP/IP model)/data-link 
    layer (OSI model).
    
    Args:
        iface: A string specifying the name of the network interface to which 
               the raw socket should be bound. For example "eth0".

    Returns:
        A socket object.
    """
    sock = socket.socket(socket.AF_PACKET, 
                         socket.SOCK_RAW, 
                         socket.htons(socket.SOCK_RAW))
    sock.bind((iface, socket.SOCK_RAW))
    return sock

def main(args=None):
    """Program entry point."""
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
        print('error: failure to open file (' + fpath + ')', file=sys.stderr)
        return 1 # exit failure

    try:
        buf = f.read()
    except:
        print('error: failure reading from file', file=sys.stderr)
        return 1 # exit failure
    f.close()

    try:
        sock.sendall(buf)
    except:
        print('error: failure writing packet to network', file=sys.stderr)
        return 1 # exit failure
    sock.close()

    return 0 # exit success

if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv))
    except KeyboardInterrupt:
        # handle SIGINT
        sys.exit(1) # exit failure
    except Exception:
        # handle all Exception, but not BaseException, subclasses
        print('error: unhandled exception', file=sys.stderr)
        sys.exit(1) # exit failure

