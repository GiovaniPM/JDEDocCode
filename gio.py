#!/usr/bin/env python
import os.path
import re
import string
import sys
import unicodedata
import os

#python.exe JDEGraph.py gio.txt d

comandos   = [ 'If', 'Else', 'EndIf', 'EndWhile', 'For', 'While', 'EndFor' ]
atribuicao = [ 'VA', 'BF', 'FI', 'RI' ]
sqls       = [ 'Select', 'Insert', 'Update', 'Delete', 'Fetch', 'FetchNext', 'FetchSingle', 'Close' ]

def classificaToken(token1, token2, eFim):
    sqlcomando = token1.split('.')
    token2 = token2.lstrip(' ').rstrip(' ')
    if token1 in comandos:
        token2 = token2.lstrip('!#!').rstrip('!#!')
        token2 = token2.replace(' !#! ','\n')
        if token2 != '':
            print(token2)
        print('comando: ' + token1)
        token1 = ''
        token2 = ''
    elif len(sqlcomando) > 1 and sqlcomando[1] in sqls:
        token2 = token2.lstrip('!#!').rstrip('!#!')
        token2 = token2.replace(' !#! ','\n')
        if token2 != '':
            print(token2)
        print('sql....: ' + token1)
        token1 = ''
        token2 = ''
    elif eFim == True:
        print(token2)
    #else:
    #    print(token2)

    return token1, token2

def processa(param1, param2, param3):
    if re.match(r'[^ ]', param1):
        param2 += param1
    else:
        sqlcomando = param2.split('.')
        if param2 in comandos:
            param3 = ''
        elif len(sqlcomando) > 1 and sqlcomando[1] in sqls:
            param3 = ''
        else:
            param3 += ' ' + param2
            param2 = ''
    return param2, param3

namefilejde    = sys.argv[1]
namefilefgraph = os.path.splitext(sys.argv[1])[0]+".gv"
#namefilejde    = './temp.txt'
#namefilefgraph = './temp.gv'

if len(sys.argv) == 3:
    modo = sys.argv[2]
else:
    modo = ''

if os.path.isfile(namefilefgraph):
    os.remove(namefilefgraph)

filejde   = open(namefilejde ,"r")
filegraph = open(namefilefgraph,"w+")

workcode = ''

# Transformo num unico string
for line in filejde:
    line = line.rstrip('\n').lstrip(' ').rstrip(' ')
    line = re.sub(r'[^0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"!#$%&()*+,-./:;<=>?@[\]^>" ]','',line)
    if line[0:1] != '!' and line[0:2] != '//' and len(line) > 0:
        if workcode == '':
            workcode += line
        else:
            workcode += ' !#! ' + line

frase    = ''
palavra  = ''
workcode = re.sub(r'End If'   ,'EndIf'   ,workcode)
workcode = re.sub(r'End For'  ,'EndFor'  ,workcode)
workcode = re.sub(r'End While','EndWhile',workcode)

#print(workcode)

while len(workcode) > 0:
    caracter = workcode[0:1]
    workcode = workcode[1:]

    palavra, frase = processa(caracter, palavra, frase)

    #print(palavra)

    palavra, frase = classificaToken(palavra, frase, False)

palavra, frase = classificaToken(palavra, frase, True)

filegraph.close()
filejde.close()