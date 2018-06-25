# coding:utf8

class myclass:

    def __init__(self):
        self._mything =1

    def _get_i(self):
        return self._mything

    def _set_i(self,value):
        self._mything = value

    def _delete_i(self):
        print("yeah...")

    mything = property(_get_i,_set_i,_delete_i,"my thing")

def hello(self):
    print("hello")

# klass = type("ttt",(object,),{'method':hello})
# inst = klass()
# inst.method()

def computer(data):
    for ele in data:
        yield ele*12

print(list(computer([1,2,3,4,5])))


def Singleton(cls):
    _instance = {}
    def _singleton(*args, **kargs):
        print(_instance)
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@Singleton
class A(object):
    a = 1

    def __init__(self, x=0):
        self.x = x


a1 = A(2)
a2 = A(3)
print(a1.x,a2.x)