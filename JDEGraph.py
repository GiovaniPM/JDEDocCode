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

stack   = []
command = []
# tokens  = ['If',
#           'Else',
#           'End If',
#           'While',
#           'End While',
#           'Or',
#           'And',
#           'is equal to',
#           'is less than',
#           'is less than or equal',
#           'is greater than',
#           'is greater than or equal',
#           'is not equal to']
tokens  = ['If',
          'Else',
          'End If',
          'While',
          'End While']
ignore  = ['EVENTS',
          'Event Level Variables']

for line in filejde:
    str = line.strip()
    str = re.sub(r'[^0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"!#$%&()*+,-./:;<=>?@[\]^_`{|}~ \']','',str)
    if len(str) > 0 and str != "//" and str[0:1] != "!":
        if len(str) == 81 and str == '-' * 81:
            stack.append('==> Name')
        elif len(str) == 45 and str == '=' * 45:
            stack.append('==> Event')
        elif len(str) == 53 and str == '=' * 53:
            stack.append('==> Interface')
        elif len(str) == 40 and str == '-' * 40:
            stack.append('==> Variables')
        elif str in ignore:
            stack.pop()
        else:
            stack.append(str)

while len(stack) :
    command.append(stack.pop())

while len(command) :
    filegraph.write(command.pop()+"\n")

filegraph.close()
filejde.close()