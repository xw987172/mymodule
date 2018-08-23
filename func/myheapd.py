# coding:utf8
import heapq
'''
__info__: headp 应用场景：取某一个列表中，最大或最小的n个数
nums = [26,12,68,2,10]
print(heapd.nlargest(3,nums))
print(heapd.nsmallest(3,nums))

heap = list(nums)
heapd.heapify(heap)  heap[0] 永远是最小的元素
heapd.heappop(heap)

portinfos = [
    {"name":"xw",age:18},
    {"name":"wx",age:17},
]
heapd.nsmallest(3,portinfos,key = lambda s:s["age"])
'''

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

class Item(object):
    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return self.__class__.__name__+":"+self.name

if __name__=="__main__":
    print(Item("xuwei"))
    q = PriorityQueue()
    q.push(Item("xw"),1)