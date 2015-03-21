#!/usr/bin/env python3

import argparse
from sys import exit
from urllib.request import urlopen
from urllib.error import URLError

def get_urls(fname):
    with open(fname) as f:
        for l in f.readlines():
            l = l.strip()
            if l.startswith('#'):
                continue
            if not l:
                continue
            yield l

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('--host', help='host to check', default='diax.overviewer.org')
    p.add_argument('-f', '--file', help='url file to use', default='urls.txt')
    p.add_argument('-l', '--length', help='length to use for names', type=int, default=60)
    args = p.parse_args()

    prefix = 'http://' + args.host

    found = 0
    notfound = 0
    for url in get_urls(args.file):
        name = url
        if args.length and len(name) > args.length:
            name = name[:args.length - 3] + '...'

        print(name, end=': ')
        try:
            f = urlopen(prefix + url)
            if f.status in {200}:
                print('\033[92mok\033[0m')
                found += 1
            else:
                print('\033[91mNOT FOUND ({0})\033[0m'.format(f.status))
                notfound += 1
            f.close()
        except URLError:
            print('\033[91mNOT FOUND\033[0m')
            notfound += 1

    print()
    if notfound:
        print('{0} of {1} urls found (\033[91m{2} missing\033[0m)'.format(found, found + notfound, notfound))
        exit(1)
    else:
        print('\033[92m{0} of {1}\033[0m urls found'.format(found, found + notfound))
        exit(0)
