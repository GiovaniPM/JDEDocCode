#!/usr/bin/env python

def func(a):
    a[0] = 'new-value'     # 'a' references a mutable list
    a[1] = a[1] + 1        # changes a shared object

args = ['old-value', 99]

func(args)

print(args[0], args[1])     # output: new-value 100s

func(args)

print(args[0], args[1])     # output: new-value 100s

func(args)

print(args[0], args[1])     # output: new-value 100s

func(args)

print(args[0], args[1])     # output: new-value 100s