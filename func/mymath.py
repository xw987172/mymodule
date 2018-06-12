from math import sqrt

class mymathclass:
    @staticmethod
    def cosLike(vector1,vector2):
        dot_product = 0.0
        normA,normB = [0.0]*2
        for a,b in zip(vector1,vector2):
            dot_product += a*b
            normA += a**2
            normB += b**2
        if normA==0.0 or normB==0.0:
            raise Exception("平方和出现0")
        else:
            return dot_product/sqrt(normA*normB)