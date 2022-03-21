#!/usr/bin/env python

#-----------------------------------------------------------------------
# runserver.py
# Author: Bryan Wang and Rishi Dange
#-----------------------------------------------------------------------

from sys import argv, exit, stderr
import argparse
from app import app

def main():

    parser = argparse.ArgumentParser(allow_abbrev = False,
        description = "The TigerBall application")
    parser.add_argument('port', type=int,
        help='the port at which the server should listen')
    parser.parse_args()

    if len(argv) != 2:
        print('usage: runserver.py [-h] port', file=stderr)
        exit(2)

    try:
        port = int(argv[1])
    except Exception:
        print('Port must be an integer.', file=stderr)
        exit(1)

    try:
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

if __name__ == '__main__':
    main()
