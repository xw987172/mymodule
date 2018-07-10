# coding:utf8
'''
__target__: 决策树联系
__base__: 信息熵，
'''
import numpy as np
import pandas as pd
from math import log

class jcTree:
    '''
    信息熵，信息增益
    '''
    trainData = list()
    trainLabel = list()
    featureValues = dict()  # 每个特征所有可能的取值

    def __init__(self,trainData,trainLabel,threshold):
        self.loadData(trainData,trainLabel)
        self.threshold = threshold
        self.tree = self.createTree(range(0,len(trainLabel)), range(0,len(trainData[0])))

    def loadData(self,trainData,trainLabel):
        '''
        加载数据
        :return: 
        '''
        if len(trainData)!=len(trainLabel):
            raise ValueError("输入值错误")

        self.trainData = trainData
        self.trainLabel = trainLabel

        for data in trainData:
            for index,value in enumerate(data):
                if not index in self.featureValues.keys():
                    self.featureValues[index] = [value]
                if not value in self.featureValues[index]:
                    self.featureValues[index].append(value)

    def caculateEntropy(self,dataset):
        '''
        计算信息熵
        :param dataset: 
        :return: 
        '''
        labelCount = self.labelCount(dataset)
        size = len(dataset)
        result = 0
        for i in labelCount.values():
            pi = i / float(size)
            result -= pi*(log(pi)/log(2))
        return result

    def calculateGain(self,dataset,feature):
        '''
        计算信息增益
        :param dataset: 
        :param feature: 
        :return: 
        '''
        values = self.featureValues[feature]
        result = 0
        for v in values:
            subDataSet = self.splitDataset(dataset=dataset, feature=feature, value=v)
            result += len(subDataSet)/float(len(dataset))* self.caculateEntropy(subDataSet)
        return self.caculateEntropy(dataset=dataset) - result

    def labelCount(self,dataset):
        '''
        计算数据集中，每个标签出现的次数
        :param dataset: 
        :return: 
        '''
        labelCount = {}
        for i in dataset:
            if self.trainLabel[i] in labelCount.keys():
                labelCount[self.trainLabel[i]] +=1
            else:
                labelCount[self.trainLabel[i]] = 1
        return labelCount

    def createTree(self,dataset,features):
        labelCount = self.labelCount(dataset)
        # 如果特征集为空，则该树为单节点树
        # 计算数据集中出现次数最多的标签
        if not features:
            return max(list(labelCount.items()),key = lambda x:x[1])[0]

        # 如果数据集中，只包同一种标签，该树为单节点树
        if len(labelCount) == 1:
            return list(labelCount.keys())[0]

        # 计算特征集中每个特征的信息增益
        l = list()
        for f in features:
            result = [f,self.calculateGain(dataset=dataset, feature=f)]
            l.append(result)
        # l = map(lambda x:[x,self.calculateGain(dataset=dataset, feature=x)],features)

        # 选取信息增益最大的特征
        feature,gain = max(l,key=lambda x:x[1])

        # 如果最大信息增益小于阈值，则该树为单节点树
        if self.threshold>gain:
            return max(list(labelCount.items()),key = lambda x:x[1])[0]

        tree = dict()
        # 选取特征子集
        subFeatures = filter(lambda x: x != feature, features)
        tree['feature'] = feature

        # 构建子树
        for value in self.featureValues[feature]:
            subDataset = self.splitDataset(dataset=dataset,feature=feature,value=value)

            # 保证子数据集非空
            if not subDataset:
                continue
            tree[value] = self.createTree(dataset=subDataset, features=subFeatures)
        return tree

    def splitDataset(self,dataset,feature,value):
        result = []
        for index in dataset:
            if self.trainData[index][feature]==value:
                result.append(index)
        return result

    def classify(self,data):
        def f(tree, data):
            if type(tree)!= dict:
                return tree
            else:
                return f(tree[data[tree['feature']]], data)
        return f(self.tree,data)



if __name__=="__main__":
    trainData = [
        [0, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 1, 0, 1],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 1],
        [1, 1, 1, 1],
        [1, 0, 1, 2],
        [1, 0, 1, 2],
        [2, 0, 1, 2],
        [2, 0, 1, 1],
        [2, 1, 0, 1],
        [2, 1, 0, 2],
        [2, 0, 0, 0],
    ]

    trainLabel = [0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0]

    tree = jcTree(trainData=trainData, trainLabel=trainLabel, threshold=0)
    print(tree.tree)
    '''下面是用Python包实现的决策树'''
    from sklearn.tree import DecisionTreeClassifier
    tree = DecisionTreeClassifier(criterion="entropy",max_depth=3,random_state=0)
    tree.fit(trainData,trainLabel)
    print(tree)

