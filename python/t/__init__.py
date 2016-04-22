#!/usr/bin/env python2

from __future__ import print_function

import os, subprocess, sys

CMD = './obfuscator'
CIRCUIT_PATH = 'circuits'

yellow = '\x1b[33m'
black = '\x1b[0m'
failure_str = '\t\x1b[31mTest Failed\x1b[0m'
success_str = '\t\x1b[32mTest Succeeded\x1b[0m'

schemedict = {
    'SZ': '--sahai-zhandry',
    'Z': '--zimmerman',
}

def print_test(s):
    print('%s%s%s' % (yellow, s, black))

def run(lst):
    print('%s' % ' '.join(lst))
    return subprocess.call(lst)

def test_circuits(scheme, mlm):
    print_test('Testing all circuits for scheme %s' % scheme)
    lst = [CMD, "obf", "--test-all", CIRCUIT_PATH, "--secparam", "8",
           "--mlm", mlm]
    lst.append(schemedict[scheme])
    return run(lst)

def test_load(scheme, mlm):
    print_test('Testing load for scheme %s' % scheme)
    if scheme == 'Z':
        circuit = 'add.acirc'
        eval = '0'
    else:
        circuit = 'and.circ'
        eval = '00'
    path = os.path.join(CIRCUIT_PATH, circuit)
    lst = [CMD, "obf", "--test", path, "--secparam", "8", "--mlm", mlm]
    lst.append(schemedict[scheme])
    r = run(lst)
    if r:
        return r
    lst = [CMD, "obf", "--load-obf", path + ".obf.8", "--mlm", mlm, "--eval", eval]
    lst.append(schemedict[scheme])
    return run(lst)

def test(f, *args):
    if f(*args):
        print(failure_str)
    else:
        print(success_str)

def test_all():
    test(test_load, "SZ", "CLT")
    # test(test_load, "Z", "CLT")
    test(test_load, "SZ", "GGH")
    test(test_circuits, "SZ", "CLT")
    # test(test_circuits, "Z", "CLT")
    test(test_circuits, "SZ", "GGH")

try:
    test_all()
except KeyboardInterrupt:
    pass