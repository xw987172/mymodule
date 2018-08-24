# coding:utf-8
'''Part 1 ： 计算一个列表中元素出现的频次'''
from collections import Counter
a =  [1,2,1,3,1,2]
word_counts = Counter(a)
print(word_counts.most_common(2))
print(word_counts[1])

'''Part2 字典排序'''
rows = [
    {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
    {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
    {'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
    {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
]
from operator import itemgetter
rows_by_name = sorted(rows,key=itemgetter("fname"))
rows_by_uid = sorted(rows,key=itemgetter("uid"))

#  对于不支持排序的对象的处理
class people:
    def __init__(self,age):
        self.age = age

from operator import attrgetter
peoples = [people(10),people(9),people[18]]
sorted(peoples,key=attrgetter("people"))

'''不同序列，同一分割slice'''
from itertools import compress
a = "absdsafg"
b= [1,2,3,4,5,6,7,8]
c = [n>3 for n in b]
print(compress(a,c))

'''在两个不同的字典中寻值，字典有优先级'''
a = {"x":1,"y":2}
b = {"k":10,"x":20}
from collections import ChainMap
c = ChainMap(a,b)
print(c["x"])

'''两个列表合并遍历'''
from itertools import chain
a = [1,5]
b = [6,7,8]
for x in chain(a,b):
    print(x)

'''两个列表合并排序'''
import heapq
for c in heapq.merge(a,b):
    print(c)