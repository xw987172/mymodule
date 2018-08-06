# coding = utf8
'''
多层神经网络算法
以识别0-9 10个数字为例，构建三层：输入层784，隐层单元50，10个输出单元的网络
'''
import numpy as np
from scipy.special import expit
import sys


class NeuralNetMLP():
    '''神经网络--多层感知器'''

    def __init__(self, n_output, n_features, n_hidden=30, l1=0.0, l2=0.0, epochs=500, eta=0.001, alpha=0.0,
                 decrease_const=0.0, shuffle=True, minibatches=1, random_state=None):
        np.random.seed(random_state)  # 设置随机种子，确保每次np.random.random()生成的随机数都是相同的
        self.n_output = n_output  # 输出层的特征数量
        self.n_hidden = n_hidden  # 隐层的特征数量
        self.n_features = n_features  # 输入层的特征数量
        self.w1, self.w2 = self._initialize_weights()  # 分类样本
        self.l1 = l1  # 正则化系数，用于降低过拟合程度，L1正则化参数
        self.l2 = l2  # 正则化系数，用于降低过拟合程度，L2正则化参数
        self.epochs = epochs  # 遍历训练集的次数-迭代次数
        self.eta = eta  # 学习速率
        self.alpha = alpha  # 动量学习进度的参数，在上一轮迭代的基础上，增加一个因子，加快权重更新，关键就要看权重更新策略
        self.decrease_const = decrease_const  # 降低自适应学习速率eta的常数d，随着迭代次数的增加而递降能更好的确保收敛
        self.shuffle = shuffle  # 在每次迭代前打乱训练集的顺序，避免进入死循环
        self.minibatches = minibatches  # 每次迭代中，将训练数据分成 xx个小批次，为加速学习的过程，梯度由每个批次分别计算，而不是在整个数据集上进行计算

    def _initialize_weights(self):
        '''
        把输入值先分为隐层50个分类，再把隐层的50个分类分为输出层的10个分类
        生成输入层-隐层的维度的分类，以及从隐层-输出层的随机数据，其实就是两组分类
        :return: 
        '''
        w1 = np.random.uniform(-1.0, 1.0, size=self.n_hidden * (self.n_features + 1))
        w1 = w1.reshape(self.n_hidden, self.n_features + 1)
        w2 = np.random.uniform(-1.0, 1.0, size=self.n_output * (self.n_hidden + 1))
        w2 = w2.reshape(self.n_output, self.n_hidden + 1)
        return w1, w2

    def _sigmoid(self, z):
        '''S函数，把数据压缩到0-1之间'''
        return expit(z)

    def _sigmoid_gradient(self, z):
        '''
        神经网络的阈值，S函数的求导值
        :param z: 
        :return: 
        '''
        sg = self._sigmoid(z)
        return sg * (1 - sg)

    def _encode_labels(self, y, k):
        '''
        目的是把所有的样本条数，做成一个onehotencoding
        :param y:输出的真实分类 
        :param k: 输出层数量10
        :return: 
        '''
        onehot = np.zeros((k, y.shape[0]))  # 生成50*样本数量的0矩阵，应该是为了，在50行分类中
        for idx, val in enumerate(y):
            onehot[val, idx] = 1.0
        return onehot

    def _add_bias_unit(self, x, how="column"):
        if how == "column":
            x_new = np.ones((x.shape[0], x.shape[1] + 1))
            x_new[:, 1:] = x
        elif how == "row":
            x_new = np.ones((x.shape[0] + 1, x.shape[1]))
            x_new[1:, :] = x
        else:
            raise AttributeError("how 只有两个值-column,row")
        return x_new

    def _feedforward(self, partData, w1, w2):
        '''

        :param partData:等分的小部分训练集 
        :param w1: 
        :param w2: 
        :return: 
        '''
        a1 = self._add_bias_unit(partData, how='column')
        z2 = w1.dot(a1.T)
        a2 = self._sigmoid(z2)
        a2 = self._add_bias_unit(a2, how="row")
        z3 = w2.dot(a2)
        a3 = self._sigmoid(z3)
        return a1, z2, a2, z3, a3

    def _L2_reg(self, lambda_, w1, w2):
        '''
        L1正则化系数
        :param L1: 
        :param w1: 
        :param w2: 
        :return: 
        '''
        return (lambda_ / 2.0) * (np.sum(w1[:, 1:] ** 2) + np.sum(w2[:, 1:] ** 2))

    def _L1_reg(self, lambda_, w1, w2):
        '''
        L1正则化系数
        :param L1: 
        :param w1: 
        :param w2: 
        :return: 
        '''
        return (lambda_ / 2.0) * (np.abs(w1[:, 1:]).sum() + np.abs(w2[:, 1:]).sum())

    def _get_cost(self, y_enc, output, w1, w2):
        '''

        :param y: 
        :param w1: 
        :param w2: 
        :return: 
        '''
        term1 = -y_enc * (np.log(output))
        term2 = (1 - y_enc) * np.log(1 - output)

        cost = np.sum(term1 - term2)
        L1_term = self._L1_reg(self.l1, w1, w2)
        L2_term = self._L2_reg(self.l2, w1, w2)
        cost = cost + L1_term + L2_term
        return cost

    def fit(self, x, y, print_progress=False):
        '''
        训练
        :param x: 特征集
        :param y: 结果集
        :param print_process: 
        :return: 
        '''
        self.cost_ = []
        X_data, Y_data = x.copy(), y.copy()

        y_enc = self._encode_labels(y, self.n_output)

        delta_w1_prev = np.zeros(self.w1.shape)
        delta_w2_prev = np.zeros(self.w2.shape)

        for i in range(self.epochs):
            self.eta /= (1 + self.decrease_const * i)

            if print_progress:
                sys.stdout.write('\r Epoch:{0}/{1}'.format(i + 1, self.epochs))
                sys.stdout.flush()

            if self.shuffle:
                idx = np.random.permutation(y.shape[0])  # permutation 生成0 - n 梯度为1 的随机数组
                X_data, Y_data = X_data[idx], Y_data[idx]  # 打乱顺序

            mini = np.array_split(range(Y_data.shape[0]), self.minibatches)  # 把训练集拆分分50份
            for idx in mini:
                a1, z2, a2, z3, a3 = self._feedforward(x[idx], self.w1, self.w2)

                cost = self._get_cost(y_enc=y_enc[:, idx], output=a3, w1=self.w1, w2=self.w2)

                self.cost_.append(cost)

                grad1, grad2 = self._get_gradient(a1=a1, a2=a2, a3=a3, z2=z2, y_enc=y_enc[:, idx], w1=self.w1,
                                                  w2=self.w2)

                delta_w1,delta_w2 = self.eta*grad1,self.eta*grad2
                self.w1 -= (delta_w1+(self.alpha*delta_w1_prev))
                self.w2 -= (delta_w2+(self.alpha*delta_w2_prev))
                delta_w1_prev , delta_w2_prev = delta_w1, delta_w2
        return self

    def predict(self, x):
        a1, z2, a2, z3, a3 = self._feedforward(x, self.w1, self.w2)
        y_pred = np.argmax(z3, axis=0)
        return y_pred

    def _get_gradient(self, a1, a2, a3, z2, y_enc, w1, w2):
        '''

        :param a1: 
        :param a2: 
        :param a3: 
        :param z2: 
        :param y_enc: 
        :param w1: 
        :param w2: 
        :return: 
        '''
        sigma3 = a3 - y_enc
        z2 = self._add_bias_unit(z2, how='row')
        sigma2 = w2.T.dot(sigma3) * self._sigmoid_gradient(z2)
        sigma2 = sigma2[1:, :]
        grad1 = sigma2.dot(a1)
        grad2 = sigma3.dot(a2.T)

        grad1[:, 1:] += (w1[:, 1:] * (self.l1 + self.l2))
        grad2[:, 1:] += (w2[:, 1:] * (self.l1 + self.l2))

        return grad1, grad2


if __name__ == "__main__":
    X_train = np.random.uniform(-10, 10, size=100 * 100)
    X_train = X_train.reshape(100, 100)
    Y_train = [0] * 20 + [2] * 20 + [3] * 20 + [4] * 40
    Y_train = np.array(Y_train)
    nn = NeuralNetMLP(
        n_output=4,
        n_features=X_train.shape[1],
        n_hidden=50,
        l2=0.1,
        l1=0.0,
        epochs=1000,
        eta=0.001,
        alpha=0.001,
        decrease_const=0.0001,
        shuffle=True,
        minibatches=50,
        random_state=1,
    )
    nn.fit(X_train, Y_train)
