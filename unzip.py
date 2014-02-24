#!/usr/bin/env python

from zipfile import ZipFile
from os import getcwd, chdir
from sys import argv
from os.path import abspath
from glob import glob
from collections import deque
from subprocess import call


def i_glob(pattern):
    """casei-insensitive glob. inspired by Geoffrey Irving"""
    lowerUpper = lambda c: "[{0}{1}]".format(c.lower(), c.upper())
    either = lambda c: lowerUpper(c) if c.isalpha() else c
    return glob("".join(map(either, pattern)))


def main(directory=".", verbose=False, tree=False):
    """bft of sub-directories, unzipping along the way"""

    chdir(directory)
    directory = getcwd()

    Q = deque([directory])
    while Q:
        d = Q.popleft()
        chdir(d)
        if verbose: print "in:", d
        for z in i_glob("*.zip"):
            if verbose: print "unzipping:", z
            ZipFile(z).extractall()
        for s in glob("*/"):
            Q.append(abspath(s))

    chdir(directory)
    if tree: call(["tree"])


if __name__ == "__main__":
    from argparse import ArgumentParser
    p = ArgumentParser()

    help = "starting directory"
    p.add_argument("starting_dir", nargs='?', help=help, default=".")

    help, action = "increase output verbosity", "store_true"
    p.add_argument("-v", "--verbose", help=help, action=action)

    help = "show directory tree"
    p.add_argument("-t", "--tree", help=help, action=action)

    args = p.parse_args()
    d, v, t = args.starting_dir, args.verbose, args.tree
    main(directory=d, verbose=v, tree=t)

