#parent node
class BT_Root:

    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data
    
    def insert(self, data):
        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = BT_Root(data) 
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = BT_Root(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data
    
    def print(self):
        if self.left:
            self.left.print()
        print(self.data)
        if self.right:
            self.right.print()

print('--------------')

r = BT_Root(13)
r.insert(23)
r.insert(3)
r.insert(15)
r.insert(16)
r.insert(4)
r.print()

print('--------------')

s = BT_Root('Giovani')
s.insert('Perotto')
s.insert('Mesquita')
s.insert('Mora')
s.insert('Em')
s.insert('Porto')
s.insert('Alegre')
s.print()

print('--------------')