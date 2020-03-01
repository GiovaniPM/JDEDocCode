#!/usr/bin/env python
import os.path
import re
import string
import sys
import unicodedata

namefilejde    = sys.argv[1]
namefilefgraph = os.path.splitext(sys.argv[1])[0]+".gv"

if os.path.isfile(namefilefgraph):
    os.remove(namefilefgraph)
filejde   = open(namefilejde ,"r")
filegraph = open(namefilefgraph,"w+")

stack  = []
output = []
tokens = ['If',
          'Else',
          'End If',
          'While',
          'End While',
          'Or',
          'And',
          'is equal to',
          'is less than',
          'is less than or equal',
          'is greater than',
          'is greater than or equal',
          'is not equal to']

for line in filejde:
    str = line.strip()
    str = re.sub(r'[^0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"!#$%&()*+,-./:;<=>?@[\]^_`{|}~ ]','',str)
    if len(str) > 0 and str != "//" and str[0:1] != "!":
        if len(str) == 81 and str == '-' * 81:
            stack.append('==> BSFN name')
        elif len(str) == 45 and str == '=' * 45:
            stack.append('==> Event name')
        elif len(str) == 53 and str == '=' * 53:
            stack.append('==> DS name')
        elif len(str) == 40 and str == '-' * 40:
            stack.append('==> Variables name')
        elif str in ['EVENTS', 'Event Level Variables']:
            stack.pop()
        else:
            stack.append(str)

while len(stack) :
    output.append(stack.pop())

while len(output) :
    filegraph.write(output.pop()+"\n")

filegraph.close()
filejde.close()