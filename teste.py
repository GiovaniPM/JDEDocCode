#!/usr/bin/env python

def func(a, b):
    a[0] = 'new-value'     # 'a' references a mutable list
    a[1] = a[1] + 1        # changes a shared object
    b    = b + 1

args = ['old-value', 99]
b    = 0

func(args, b)

print(args[0], args[1], b)     # output: new-value 100s