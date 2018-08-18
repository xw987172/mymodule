# coding:utf8
from sklearn.cluster import KMeans
from func.mymath import mymathclass

class myKmeans(KMeans):

    def __init__(self,**kwargs):
        super(self.__class__,self).__init__(**kwargs)

    def fit(self, X, y=None):
        model = super(self.__class__,self).fit(X,y)
        model.distance = list()
        m,n = X.shape
        for i in range(m):
            a = list(X[i])
            label = list(model.labels_)
            b = list(model.cluster_centers_[label[i]])
            model.distance.append(mymathclass.ouDistance(a,b))
        return model

from sklearn.datasets import make_blobs

x,y = make_blobs(
    n_samples=150,
    n_features=2,
    centers = 3
)

km = myKmeans(n_clusters=3)

z= km.fit(x)

print(z.distance)