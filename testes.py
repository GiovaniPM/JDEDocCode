lst = [ 'node001', 'node002', 'node003' ]
print(lst)
test = 'node002' in lst
print(test)
lst.remove('node002')
print(lst)
test = 'node002' in lst
print(test)
test = len(lst) > 0
print(test)