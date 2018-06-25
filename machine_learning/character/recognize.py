# coding: utf8
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
from machine_learning.character.neuralnet import NeuralNetMLP

def load(path="/Users/xuwei/Downloads/",kind= "train"):
    labels_path = os.path.join(path,"%s-labels-idx1-ubyte" %(kind))
    images_path = os.path.join(path,"%s-images-idx3-ubyte" %(kind))

    with open(labels_path,'rb') as lp:
        magic, n = struct.unpack('>II',lp.read(8))
        labels = np.fromfile(lp,dtype=np.uint8)

    with open(images_path,'rb') as lp:
        magic, num, rows, cols = struct.unpack('>IIII',lp.read(16))
        images = np.fromfile(lp,dtype=np.uint8).reshape(len(labels),784)

    return images,labels

train_images,train_labels = load()
test_images,test_labels = load(kind="t10k")

print(train_images[0][0])
print(train_labels)
# fig,ax = plt.subplots(nrows=2,ncols=5,sharex=True,)
# '''绘制0-9的标准输出'''
# ax = ax.flatten()
# for i in range(10):
#     img = train_images[train_labels==i][0].reshape(28,28)
#     ax[i].imshow(img,cmap="Greys",interpolation="nearest")
#
# ax[0].set_xticks([])
# ax[0].set_yticks([])
# plt.tight_layout()
# plt.show()
nn = NeuralNetMLP(
    n_output    =10,                    # 10个输出单元，也就是模板值0-9
    n_features  =train_images.shape[1], # 786个输入单元，也就是特征维度
    n_hidden    =50,                    # 50个隐层单元
    l2          =0.1,                   # 正则化系数，降低过拟合程度
    l1          =0.0,
    epochs      =1000,                  # 遍历训练集的次数，也就是迭代次数
    eta         =0.001,                 # 学习速率
    alpha       =0.001,                 # 动量学习进度的参数，在上一轮迭代的基础上增加一个因子，用来加快权重更新的学习
    decrease_const=0.00001,             # 用来降低自适应学习的速率的常数d，随着迭代次数的增加而随之递减以更好的确保收敛
    shuffle     =True,                  # 在每次迭代前打乱训练集的顺序，以防止算法进入死循环
    minibatches =50,                    # 在每次迭代前，将训练数据划分为k个 小的批次，加快学习的过程，梯度由每个批次分别计算，而不是在整个训练集上进行计算
    random_state    =1
)
nn.fit(train_images,train_labels,print_progress=True)
plt.plot(range(len(nn.cost_)),nn.cost_)
plt.ylim([0,2000])
plt.ylabel('Cost')
plt.xlabel('Epochs * 50')
plt.tight_layout()
plt.show()