#!/usr/bin/env python
import os.path
import re
import string
import sys
import unicodedata

namefilejde    = sys.argv[1]
namefilefgraph = os.path.splitext(sys.argv[1])[0]+".gv"
# namefilejde    = 'c:/Users/giovani_mesquita/projetos/JDEDocCode/N554308.txt'
# namefilefgraph = 'c:/Users/giovani_mesquita/projetos/JDEDocCode/N554308.gv'

if os.path.isfile(namefilefgraph):
    os.remove(namefilefgraph)
filejde   = open(namefilejde ,"r")
filegraph = open(namefilefgraph,"w+")

stack     = []
connects  = []
output    = []
qif       = []
qwhere    = []
values    = ['','','','',0,'',0]
valuesant = ['','','','',0,'',0]
tokens    = ['If',
            'Else',
            'End If',
            'While',
            'End While',
            'And',
            'Or']
ignore    = ['EVENTS',
            'Event Level Variables']
plsql     = ['Select',
             'Delete',
             'Insert',
             'Update',
             'FetchNext',
             'FetchSingle']
values[0] = ''        # node
values[1] = 'nodeini' # lastnode
values[2] = ''        # cmd
values[3] = ''        # lastcmd
values[4] = 1         # sequencial
values[5] = ''        # texto
values[6] = 0         # words

def mountvalues(node,lastnode,cmd,lastcmd,sequencial,texto,words):
    values[0] = node
    values[1] = lastnode
    values[2] = cmd
    values[3] = lastcmd
    values[4] = sequencial
    values[5] = texto
    values[6] = words

def formatline(line):
    lineformat = line.strip()
    return re.sub(r'[^0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"!#$%&()*+,-./:;<=>?@[\]^_`{|}~ \']','',lineformat)

def linecommand(line):
    word = line.partition(' ')[0]
    if word == 'End':
        word = word + ' ' + line.partition(' ')[2]
    return word

def restline(command,line):
    return line[len(command)+1:10000]

def preparestring(label):
    label = label.replace(r'"',r"'")
    label = label.replace(r'>',r"\>")
    label = label.replace(r'<',r"\<")
    return label

def connectnode(typenode,nodeanterior,node):
    if typenode == 'S':
        connects.append('    %s -> %s [fontname = "Arial", fontsize = 12, fontcolor="green", color="green:yellow:green", label="Sim"]' % (nodeanterior,node))
    elif typenode == 'N':
        connects.append('    %s -> %s [fontname = "Arial", fontsize = 12, fontcolor="red", color="red:yellow:red", label="Nao"]' % (nodeanterior,node))
    else:
        connects.append('    %s -> %s' % (nodeanterior,node))

def nodeinitial():
    filegraph.write('    nodeini [\n')
    filegraph.write('            shape=circle,\n')
    filegraph.write('            style="filled",\n')
    filegraph.write('            fillcolor="white:lightgreen",\n')
    filegraph.write('            label=""\n')
    filegraph.write('            ]\n')

def nodefinal():
    filegraph.write('    nodefin [\n')
    filegraph.write('            shape=circle,\n')
    filegraph.write('            style="filled",\n')
    filegraph.write('            fillcolor="white:#ee636e",\n')
    filegraph.write('            label=""\n')
    filegraph.write('            ]\n')

def nodeif(seq,label):
    label = preparestring(label)
    filegraph.write('    %s [\n' % (seq))
    filegraph.write('            fontname="Arial",\n')
    filegraph.write('            fontsize=6,\n')
    filegraph.write('            shape=record,\n')
    filegraph.write('            style="diagonals,filled",\n')
    filegraph.write('            fillcolor="white:#fbfbb1"\n')
    filegraph.write('            label="%s|{%s}"\n' % (seq,label))
    filegraph.write('            ]\n')

def nodeattrib(seq,label):
    label = preparestring(label)
    filegraph.write('    %s [\n' % (seq))
    filegraph.write('            fontname="Arial",\n')
    filegraph.write('            fontsize=6,\n')
    filegraph.write('            shape=record,\n')
    filegraph.write('            style="filled",\n')
    filegraph.write('            fillcolor="white:lightblue"\n')
    filegraph.write('            label="%s|{%s}"\n' % (seq,label))
    filegraph.write('            ]\n')

def printnode(args):
    if args[3] == 'If' and args[2] not in ['And','Or']:
        nodeif(args[0],args[5])
        args[1] = args[0]
        args[4] += 1

filegraph.write('digraph R {\n')

nodeinitial()

for line in filejde:
    if values[3] in ['If','Where'] and values[2] in ['And','Or']:
        values[3] = values[3]
    else:
        values[3] = values[2]

    lineatual = formatline(line)
    values[2] = linecommand(lineatual)

    printnode(values)

    values[6] = lineatual.count(' ')
    values[0] = 'node%s' % (str(values[4]).rjust(3, '0'))

    if len(lineatual) > 2 and lineatual[0:1] != "!":
        if len(lineatual) == 81 and lineatual == '-' * 81:
            sequence = str(values[4])
        elif len(lineatual) == 45 and lineatual == '=' * 45:    
            sequence = str(values[4])
        elif len(lineatual) == 53 and lineatual == '=' * 53:
            sequence = str(values[4])
        elif len(lineatual) == 40 and lineatual == '-' * 40:
            sequence = str(values[4])
        elif lineatual == '//':
            sequence = str(values[4])
        elif lineatual in ignore:
            sequence = str(values[4])
        elif values[2] in tokens:
            if values[2] in ['If']:
                values[5] = restline(values[2],lineatual)
                print(values)
            elif values[2] in ['Else']:
                values[5] = ''
                print(values)
            elif values[2] in ['And','Or']:
                values[5]  += r'\n' + lineatual
                print(values)
            elif values[2] in ['Enf If']:
                values[5] = ''
                print(values)
            else:
                values[5] = ''
                print(values)
        else:
            values[5] = ''
            print(values)

nodefinal()

filegraph.write('\n')

connectnode('','nodeini','node001')
connectnode('',values[1],'nodefin')

connects.reverse()
while len(connects) :
    filegraph.write(connects.pop()+"\n")

filegraph.write('}')

filegraph.close()
filejde.close()