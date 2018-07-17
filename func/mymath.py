from math import sqrt

class mymathclass:
    @staticmethod
    def cosLike(vector1,vector2):
        dot_product = 0.0
        normA,normB = [0.0]*2
        for a,b in zip(vector1,vector2):
            if a==None or b==None:
                continue
            a = float(a)
            b = float(b)
            dot_product += a*b
            normA += a**2
            normB += b**2
        if normA==0.0 or normB==0.0:
            raise Exception("平方和出现0")
        else:
            return dot_product/sqrt(normA*normB)

    @staticmethod
    def ouDistance(vector1,vector2):
        '''
        欧式距离,差平方和 开方
        :param vector1: 
        :param vector2: 
        :return: 
        '''
        return sqrt(sum(pow(a-b,2) for a,b in zip(vector1,vector2)))

    @staticmethod
    def selfRelate(X,k=None):
        '''
        自相关系数
        :param X: 序列
        :param k: 延迟
        :return: 
        '''
        avg = sum(X)/len(X)
        fenzi = 0
        fenmu = 0
        for i in range(len(X)-k):
            fenzi += (X[i]-avg)*(X[i+k] - avg)

        for i in range(len(X)):
            fenmu += (X[i]-avg)**2

        return round(fenzi/fenmu,4)


if __name__=="__main__":
    x = list(range(1,21))
    for i in range(1,7):
        print(i,mymathclass.selfRelate(x,i))

    # for i in range(5,60):
    #     a = list(range(1,i))
    #     b = reversed(a)
    #
    #     c = mymathclass.cosLike(a,b)
    #     print("个数为{0}的反相似度为：{1}".format(i,c-0.7))