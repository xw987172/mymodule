# coding:utf8
def b():
    print("in b...")


def mydecorator(function=None,st =None):
    def dec(myfunc):
        if myfunc.__name__=="a":
            return b
        else:
            return myfunc
    return dec

# def achive(function=None,st=None):
#     a = mydecorator(
#         lambda x:x+1,
#         "hello achive"
#     )
#     if function:
#         return a(function)
#     else:
#         a
@mydecorator(st="xuwei -a")
def a():
    print("in a...")


print(getattr(b,"__name__"))