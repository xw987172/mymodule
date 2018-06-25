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


if __name__=="__main__":
    a = [1,1,1,1,1]
    b = [1,1,1,1,1]
    print(mymathclass.cosLike(a,b))

    # for i in range(5,60):
    #     a = list(range(1,i))
    #     b = reversed(a)
    #
    #     c = mymathclass.cosLike(a,b)
    #     print("个数为{0}的反相似度为：{1}".format(i,c-0.7))