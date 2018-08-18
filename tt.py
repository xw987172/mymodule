# coding:utf8
months = [
    31,28,31,30,31,30,31,31,30,31,30,31
]
def getnday(dt:str)->int:
    year,month,day = dt.split("-")
    result =0
    flag = False
    if int(year)%400 ==0 or (int(year)%4==0 and int(year)%100!=0):
        flag = True
    print(flag)
    for m,n in enumerate(months):
        if flag and m ==1:
            n = 29
        if int(month)!=m+1:
            result += n
        else:
            result += int(day)
            break
    return result

print(getnday("2016-07-03"))
import datetime

d1=datetime.date(2016,7,3)
print(d1.timetuple()[7])

a= [1,3,2]

print(a.sort())


from sklearn.datasets import make_blobs

from matplotlib import pyplot as plt

from sklearn.cluster import KMeans

x,y = make_blobs(
    n_samples=150,
    n_features=2,
    centers = 3
)

print(x,y)

z = KMeans(n_clusters=3)

m =z.fit_predict(x)
print(m)