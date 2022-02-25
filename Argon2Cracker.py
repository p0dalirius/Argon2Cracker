#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : Argon2Cracker.py
# Author             : Podalirius (@podalirius_)
# Date created       : 25 Feb 2022

import argon2
import argparse
import base64
import datetime
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor


def get_ctx_from_hash(hash):
    matched = re.search('\$(argon2(i)?(d)?)\$v=([0-9]+)\$([tpm=0-9,]+)\$([a-zA-Z0-9\+]+)\$([a-zA-Z0-9\+]+)', hash)
    if matched is not None:
        _, _, _, version, params, salt, hash = matched.groups()
        params = {p.split('=')[0]: int(p.split('=')[1]) for p in params.split(',')}
        salt = base64.b64decode(salt+"==")
        hash = base64.b64decode(hash+"==")
        ctx = argon2.PasswordHasher(time_cost=params['t'], memory_cost=params['m'], parallelism=params['p'], hash_len=len(hash), salt_len=len(salt))
        return ctx
    else:
        return None


def worker(ctx, hash, candidate, monitor_data):
    if not monitor_data["found"]:
        try:
            monitor_data["tries"] += 1
            ctx.verify(hash, candidate)
            monitor_data["found"] = True
            monitor_data["candidate"] = candidate
            return True
        except argon2.exceptions.VerifyMismatchError as e:
            return False


def monitor_thread(monitor_data):
    last_check, monitoring = 0, True
    while monitoring and not monitor_data["found"]:
        new_check = monitor_data["tries"]
        rate = (new_check - last_check)
        print("\r[%s] Status (%d/%d) %5.2f %% | Rate %d H/s        " % (
            datetime.datetime.now().strftime("%Y/%m/%d %Hh%Mm%Ss"),
            new_check, monitor_data["total"], (new_check/monitor_data["total"])*100,
            rate
        ), end="")
        last_check = new_check
        time.sleep(1)
        if rate == 0 and new_check != 0:
            monitoring = False

    if monitor_data["found"]:
        print("\n[>] Found: %-30s" % monitor_data["candidate"])
    else:
        print("")

def parseArgs():
    print("Argon2Cracker - v1.0 - by @podalirius_\n")

    parser = argparse.ArgumentParser(description="argon2 hash cracker")
    parser.add_argument("hash", default=None, help="argon2 hash")
    parser.add_argument("-t", "--threads", dest="threads", action="store", type=int, default=16, required=False, help="Number of threads (Default: 16)")
    parser.add_argument("-w", "--wordlist", dest="wordlist", action="store", type=str, default=5, required=True, help="Wordlist")
    parser.add_argument("-v", "--verbose", default=False, action="store_true", help='Verbose mode. (default: False)')

    return parser.parse_args()


if __name__ == '__main__':
    options = parseArgs()

    if options.verbose:
        print("[>] Loading wordlist ... ", end="")
        sys.stdout.flush()
    f = open(options.wordlist, 'r')
    wordlist = sorted([l.strip() for l in f.readlines()])
    f.close()
    if options.verbose:
        print("done. (%d candidates loaded)" % len(wordlist))
        sys.stdout.flush()

    ctx = get_ctx_from_hash(options.hash)

    monitor_data = {"found": False, "tries": 0, "candidate": "", "total": len(wordlist)}

    # Waits for all the threads to be completed
    with ThreadPoolExecutor(max_workers=min(options.threads, len(wordlist))+1) as tp:
        tp.submit(monitor_thread, monitor_data)
        for candidate in wordlist:
            tp.submit(worker, ctx, options.hash, candidate, monitor_data)

    if not monitor_data["found"]:
        print("[!] Hash could not be cracked from this wordlist.")
