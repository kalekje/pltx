import yaml
import oyaml as yaml
import functools as ft
import operator as op

# https://stackoverflow.com/questions/5484016/how-can-i-do-string-concatenation-or-string-replacement-in-yaml
def join(loader, node): ## define custom tag handler
    seq = loader.construct_sequence(node)
    print(seq, '<<<<')
    return ''.join([str(i) for i in seq])
yaml.add_constructor('!join', join) ## register the tag handler

def sum_(loader, node): ## define custom tag handler
    return sum(loader.construct_sequence(node))
yaml.add_constructor('!sum', sum_) ## register the tag handler

def concat(loader, node): ## define custom tag handler
    seq = loader.construct_sequence(node, deep=True)
    print(seq, '<<<<')
    return ft.reduce(op.add, seq)  # I made this up :) and think it's elegant, but why doesn't it work?
yaml.add_constructor('!concat', concat) ## register the tag handler

ft.reduce(op.add, [[1,2],[3,4],[5,6]]) # try it

#language=yaml
Y = """
defStr: &myStr StringWord
defList: &myList
  - Item1
  - Item2

# defList: &myList [Item1, Item2]

useStr: *myStr # works as expected
useList: *myList # works as expected

appStr: !join [*myStr, ' Newly added sentence']  # uses custom node definition to join strings

extList1: !concat [*myList, [Item3, Item4]]  # uses custom node definition to concat lists
extList2: !concat [[Item0, Item1], [Item3, Item4]]  # uses custom node definition to concat lists

sumThem: !sum [1,2,3,4,5]

"""

# D = yaml.safe_load(Y) # does not work with !join
D = yaml.load(Y)
for k, v in D.items():
    print(k,v)