#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : generate_hash.py
# Author             : Podalirius (@podalirius_)
# Date created       : 25 Feb 2022

import argon2
import argparse

def parseArgs():
    parser = argparse.ArgumentParser(description="Description message")
    parser.add_argument("text", help='Password to hash')
    return parser.parse_args()


if __name__ == '__main__':
    options = parseArgs()

    hash = argon2.PasswordHasher().hash(options.text)
    print(hash)


