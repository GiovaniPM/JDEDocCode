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

stack      = []
connects   = []
output     = []
qif        = []
qwhere     = []
tokens     = ['If',
             'Else',
             'End If',
             'While',
             'End While',
             'End',
             'And',
             'Or']
ignore     = ['EVENTS',
             'Event Level Variables']
plsql      = ['Select',
              'Delete',
              'Insert',
              'Update',
              'FetchNext',
              'FetchSingle']
sequencial = 0
seqnamelst = 'nodeini'
mountline  = ''
lastcmd    = ''

def preparestring(label):
    label = label.replace(r'"',r"'")
    label = label.replace(r'>',r"\>")
    label = label.replace(r'<',r"\<")
    return label

def lastnode(sequence,command,mountline):
    if command in ['If']:
        nodeif(sequence, mountline)
        connects.append('    %s -> %s [fontname = "Arial", fontsize = 12, fontcolor="green", color="green:yellow:green", label="Sim"]' % (seqnamelst,seqname))
        return(seqname)
    elif command in ['Where']:
        nodeif(sequence, mountline)
        connects.append('    %s -> %s' % (seqnamelst,seqname))
        return(seqname)
    elif command in ['Else']:
        connects.append('    %s -> %s [fontname = "Arial", fontsize = 12, fontcolor="red", color="red:yellow:red", label="Nao"]' % (qif.pop(),seqname))
        return(seqname)
    elif command in ['End Where']:
        connects.append('    %s -> %s' % (qwhere.pop(),seqname))
        return(seqname)
    else:
        nodeattrib(sequence, mountline)
        connects.append('    %s -> %s' % (seqnamelst,seqname))
        return(seqname)
    print('---> ' + command + ' - ' + mountline + '|' + seqnamelst + ' -> ' + seqname)
    return(seqnamelst)

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
    filegraph.write('    node%s [\n' % (seq))
    filegraph.write('            fontname="Arial",\n')
    filegraph.write('            fontsize=6,\n')
    filegraph.write('            shape=record,\n')
    filegraph.write('            style="diagonals,filled",\n')
    filegraph.write('            fillcolor="white:#fbfbb1"\n')
    filegraph.write('            label="%s|{%s}"\n' % (seq,label))
    filegraph.write('            ]\n')

def nodeattrib(seq,label):
    label = preparestring(label)
    filegraph.write('    node%s [\n' % (seq))
    filegraph.write('            fontname="Arial",\n')
    filegraph.write('            fontsize=6,\n')
    filegraph.write('            shape=record,\n')
    filegraph.write('            style="filled",\n')
    filegraph.write('            fillcolor="white:lightblue"\n')
    filegraph.write('            label="%s|{%s}"\n' % (seq,label))
    filegraph.write('            ]\n')

filegraph.write('digraph R {\n')

nodeinitial()

for line in filejde:
    lineformat = line.strip()
    lineformat = re.sub(r'[^0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"!#$%&()*+,-./:;<=>?@[\]^_`{|}~ \']','',lineformat)
    command    = lineformat.partition(' ')[0]
    if command == 'End':
        command    = command + ' ' + lineformat.partition(' ')[2]
    words      = lineformat.count(' ')
    restline   = lineformat[len(command)+1:10000]
    sequence   = str(sequencial)
    sequence   = sequence.rjust(3, '0')
    seqname    = 'node%s' % (sequence)

    if len(lineformat) > 0 and lineformat != "//" and lineformat[0:1] != "!":
        if len(lineformat) == 81 and lineformat == '-' * 81:
            # stack.append('==> Name')
            words = words
        elif len(lineformat) == 45 and lineformat == '=' * 45:
            # stack.append('==> Event')
            words = words
        elif len(lineformat) == 53 and lineformat == '=' * 53:
            # stack.append('==> Interface')
            words = words
        elif len(lineformat) == 40 and lineformat == '-' * 40:
            # stack.append('==> Variables')
            words = words
        elif len(lineformat) == 2 and lineformat == '//':
            # stack.append('==> Espace')
            words = words
        elif lineformat in ignore:
            # stack.pop()
            words = words
        elif command not in tokens:
            if lastcmd in tokens:
                seqnamelst = lastnode(sequence,lastcmd,mountline)
                sequencial += 1
                mountline  =  restline
                lastcmd    =  ''
            else:
                mountline  += r'\n' + command + r' ' + restline
                lastcmd    =  ''
        elif command in tokens:
            print('|' + lastcmd.ljust(6, ' ') + ' -> ' + command.ljust(6, ' '))
            if command in ['If']:
                qif.append(seqname)
                seqnamelst = lastnode(sequence,lastcmd,mountline)
                sequencial += 1
                mountline  =  restline
                lastcmd    =  command
            elif command in ['Where']:
                qwhere.append(seqname)
                seqnamelst = lastnode(sequence,lastcmd,mountline)
                sequencial += 1
                mountline  =  restline
                lastcmd    =  command
            elif command in ['Else']:
                seqnamelst = lastnode(sequence,lastcmd,mountline)
                mountline  =  ''
                lastcmd    =  command
            elif command in ['And','Or']:
                mountline  += r'\n' + command + r' ' + restline
            else:
                seqnamelst = lastnode(sequence,lastcmd,mountline)
                sequencial += 1
                mountline = ''
                lastcmd   = ''
        elif words < 1:
            # stack.append(lineformat)
            words = words
        # else:
        #     stack.append(lineformat)

# while len(stack) :
#     output.append(stack.pop())

# while len(output) :
#     filegraph.write(output.pop()+"\n")

nodefinal()

filegraph.write('\n')

connects.append('    %s -> nodefin' % (seqnamelst))

connects.reverse()
while len(connects) :
    filegraph.write(connects.pop()+"\n")

filegraph.write('}')

filegraph.close()
filejde.close()