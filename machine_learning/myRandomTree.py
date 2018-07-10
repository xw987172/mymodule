# coding:utf8
from sklearn.ensemble import RandomForestRegressor

class myRandomTree(RandomForestRegressor):
    '''
    重构随机森林算法
    '''
    def __init__(self):
        super(myRandomTree,self).__init__()

class father(object):

    def __init__(self,a=1,b=2):

        self.a = a
        self.b = b


    def info(self):
        print("father:",self.a,self.b)

class child(father):

    def __init__(self,a,b):
        super(child,self).__init__(a,b)

    def work(self):
        self.info()

if __name__=="__main__":

    child(1,2).work()