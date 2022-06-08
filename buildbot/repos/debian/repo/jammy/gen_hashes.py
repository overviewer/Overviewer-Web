#!/usr/bin/env python3

import sys
import time
import os.path
import hashlib

args = sys.argv[1:]

date = time.strftime("%a, %d %b %Y %H:%M:%S UTC", time.gmtime())
print("Date: {}".format(date))

def do_hashes(cls):
    for arg in args:
        with open(arg, 'rb') as f:
            hash = cls(f.read()).hexdigest()
        size = os.path.getsize(arg)
        print(" {} {:>16} {}".format(hash, size, arg))

print("MD5Sum:")
do_hashes(hashlib.md5)
print("SHA1:")
do_hashes(hashlib.sha1)
print("SHA256:")
do_hashes(hashlib.sha256)
print("SHA512:")
do_hashes(hashlib.sha512)
