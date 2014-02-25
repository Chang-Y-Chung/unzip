#!/usr/bin/env python

import os
from glob import glob
from collections import deque
from subprocess import call


def globi(pattern):
    """case-insensitive glob. inspired by Geoffrey Irving"""
    lowerUpper = lambda c: "[{0}{1}]".format(c.lower(), c.upper())
    either = lambda c: lowerUpper(c) if c.isalpha() else c
    return glob("".join(map(either, pattern)))

def main(directory=".", verbose=False):
    """bft of sub-directories, unzipping along the way"""

    os.chdir(directory)
    directory = os.getcwd()

    Q = deque([directory])
    while Q:
        d = Q.popleft()
        os.chdir(d)
        if verbose: print "in:", d
        for z in globi("*.zip"):
            if verbose: print "unzipping:", z
            call(["unzip", "-u", "-q", z])
        for s in glob("*/"):
            Q.append(os.path.abspath(s))

    os.chdir(directory)


if __name__ == "__main__":
    from argparse import ArgumentParser
    p = ArgumentParser()

    help = "starting directory"
    p.add_argument("starting_dir", nargs='?', help=help, default=".")

    help, action = "show directory and zip file names", "store_true"
    p.add_argument("-v", "--verbose", help=help, action=action)

    args = p.parse_args()
    main(directory=args.starting_dir, verbose=args.verbose)

