#!/usr/bin/env python

def func(a):
    a[0] = 'new-value'      # 'a' references a mutable list
    a[1] = a[1] + 1         # changes a shared object

args = ['old-value', 99]

func(args)
print(args[0], args[1])     # output: new-value 100
func(args)
print(args[0], args[1])     # output: new-value 101

args[1] = args[1] + 20

func(args)
print(args[0], args[1])     # output: new-value 122
func(args)
print(args[0], args[1])     # output: new-value 123