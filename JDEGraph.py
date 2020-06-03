#!/usr/bin/env python
import os.path
import re
import string
import sys
import unicodedata
import os

#c:\Python38\python.exe JDEGraph.py gio.txt d

namefilejde    = sys.argv[1]
namefilefgraph = os.path.splitext(sys.argv[1])[0]+".gv"
if len(sys.argv) == 3:
    modo       = sys.argv[2]
else:
    modo       = ''
# namefilejde    = 'c:/Users/giovani_mesquita/projetos/JDEDocCode/N554308.txt'
# namefilefgraph = 'c:/Users/giovani_mesquita/projetos/JDEDocCode/N554308.gv'

if os.path.isfile(namefilefgraph):
    os.remove(namefilefgraph)
filejde   = open(namefilejde ,"r")
filegraph = open(namefilefgraph,"w+")

stack     = [ ]
connects  = [ ]
output    = [ ]
qif       = [ ]
qwhile    = [ ]
qother    = [ ]
qprevious = [ ]
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
values[1] = 'node000' # lastnode
values[2] = ''        # cmd
values[3] = ''        # lastcmd
values[4] = 1         # sequencial
values[5] = ''        # texto
values[6] = 0         # words
endoffile = 'N'

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
        connects.append('    %s -> %s [fontname = "Arial", fontsize = 10, fontcolor="green", color="green", label="Yes"]' % (nodeanterior,node))
        printroutedebug(nodeanterior,node)
    elif typenode == 'N':
        connects.append('    %s -> %s [fontname = "Arial", fontsize = 10, fontcolor="red", color="red", label="No"]' % (nodeanterior,node))
        printroutedebug(nodeanterior,node)
    else:
        connects.append('    %s -> %s' % (nodeanterior,node))
        printroutedebug(nodeanterior,node)
    if nodeanterior not in qprevious:
        qprevious.append(nodeanterior)

def nodeinitial():
    filegraph.write('    node000 [\n')
    filegraph.write('            shape=circle,\n')
    filegraph.write('            style="filled",\n')
    filegraph.write('            fillcolor="white:lightgreen",\n')
    filegraph.write('            label=""\n')
    filegraph.write('            ]\n')

def nodefinal():
    filegraph.write('    node999 [\n')
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

def nodewhile(seq,label):
    label = preparestring(label)
    filegraph.write('    %s [\n' % (seq))
    filegraph.write('            fontname="Arial",\n')
    filegraph.write('            fontsize=6,\n')
    filegraph.write('            shape=record,\n')
    filegraph.write('            style="diagonals,filled",\n')
    filegraph.write('            fillcolor="white:orange"\n')
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

def printdebug(args):
    if modo == 'd' or modo == 'D':
        print(">>> ",args)    

def printroutedebug(nodefrom,nodeto):
    if modo == 'd' or modo == 'D':
        print("\033[1;31;40m",'  ',nodefrom,' -- ',nodeto,"\033[0;37;40m")

def connectrest():
    if len(qif) + len(qwhile) == 0:
        while(len(qother) > 0):
            node = qother.pop()
            if values[1] != node:
                connectnode('',node,values[0])

def printqueues():
    if modo == 'd' or modo == 'D':
        print('\n')
        print("\033[1;34;40m",'IF       =',qif,"\033[0;37;40m")
        print("\033[1;34;40m",'WHILE    =',qwhile,"\033[0;37;40m")
        print("\033[1;34;40m",'OTHER    =',qother,"\033[0;37;40m")
        print("\033[1;34;40m",'PREVIOUS =',qprevious,"\033[0;37;40m")
        print('\n')

def printnode(args):
    if args[3] in ['If'] and args[2] not in ['And','Or']:
        nodeif(args[0],args[5])
        args[1] = args[0]
        args[4] += 1
        args[5] = ''
    elif args[3] in ['While'] and args[2] not in ['And','Or']:
        nodewhile(args[0],args[5])
        args[1] = args[0]
        args[4] += 1
        args[5] = ''
    elif args[3] not in tokens and args[2] in tokens:
        nodeattrib(args[0],args[5])
        args[1] = args[0]
        args[4] += 1
        args[5] = ''
    elif args[3] in ['End If', 'End While'] and args[2] not in tokens and args[5] != '':
        nodeattrib(args[0],args[5])
        args[1] = args[0]
        args[4] += 1
        args[5] = ''
    elif endoffile == 'S':
        nodeattrib(args[0],args[5])
        connectnode('',values[1],values[0])

filegraph.write('digraph R {\n')

nodeinitial()

if modo == 'd' or modo == 'D':
    os.system("cls")

if modo == 'd' or modo == 'D':
    print(">>>  actualnode[0], lastnode[1], actualcmd[2], lastcmd[3], sequencial[4], text[5], words[6]")

for line in filejde:

    if values[3] in ['If','Where'] and values[2] in ['And','Or']:
        values[3] = values[3]
    else:
        values[3] = values[2]

    lineatual = formatline(line)
    values[2] = linecommand(lineatual)

    if modo == 'd' or modo == 'D':
        print("\033[1;32;40m",lineatual,"\033[0;37;40m")
    
    printnode(values)
    connectrest()

    values[6] = lineatual.count(' ') + 1
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
                qif.append(values[0])
                if values[3] == 'If':
                    connectnode('S',values[1],values[0])
                elif values[3] != 'Else':
                    connectnode('',values[1],values[0])
                printdebug(values)
            elif values[2] in ['While']:
                values[5] = restline(values[2],lineatual)
                qwhile.append(values[0])
                if values[3] == 'If':
                    connectnode('S',values[1],values[0])
                else:
                    connectnode('',values[1],values[0])
                printdebug(values)
            elif values[2] in ['Else']:
                values[5] = ''
                printdebug(values)
                nodefrom = qif.pop()
                connectnode('N',nodefrom,values[0])
                qif.append(nodefrom)
            elif values[2] in ['And','Or']:
                values[5]  += r'\n' + lineatual
                printdebug(values)
            elif values[2] in ['End If']:
                values[5] = ''
                printdebug(values)
                nodefrom = qif.pop()
            elif values[2] in ['End While']:
                values[5] = ''
                printdebug(values)
                nodefrom = qwhile.pop()
            else:
                values[5] = ''
                printdebug(values)
        else:
            if values[3] == 'If' and values[2] not in ['And','Or']:
                connectnode('S',values[1],values[0])
            if values[5] == '' and values[3] in tokens:
                values[5] = lineatual
                printdebug(values)
            else:
                values[5]  += r'\n' + lineatual
                printdebug(values)

        if values[2] in tokens and values[3] not in tokens:
            if values[1] not in qprevious:
                qother.append(values[1])

printqueues()

endoffile = 'S'
printnode(values)
connectrest()

nodefinal()

filegraph.write('\n')

# Fixed
connectnode('','node000','node001')
connectnode('',values[0],'node999')

# connectnode('','node001','node002')
# connectnode('S','node002','node003')
# connectnode('N','node002','node011')
# connectnode('S','node003','node004')
# connectnode('N','node003','node005')
# connectnode('','node004','node012')
# connectnode('S','node005','node006')
# connectnode('N','node005','node010')
# connectnode('','node006','node007')
# connectnode('S','node007','node008')
# connectnode('N','node007','node009')
# connectnode('','node008','node012')
# connectnode('','node009','node012')
# connectnode('','node010','node012')
# connectnode('','node011','node012')

printqueues()
    
while len(connects):
    linha = connects.pop()
    filegraph.write(linha+"\n")
    if modo == 'd' or modo == 'D':
        print("\033[1;35;40m",linha,"\033[0;37;40m")

filegraph.write('}')

filegraph.close()
filejde.close()