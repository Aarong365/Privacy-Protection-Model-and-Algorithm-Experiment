# 非聚类算法库实现聚类算法
import numpy as np
import math


# 生成随机数据
np.random.seed(123)
X = np.random.rand(20,2)
print("随机生成的样本：\n",X)
# X = [[16.9,0],[38.5,0],[39.5,0],[80.8,0],[82,0],[834.6,0],[116.1,0]]

# 计算两点之间的欧式距离，支持多维
'''def euler_distance(point1: np.ndarray, point2: list) -> float:
    distance = 0.0
    for a, b in zip(point1, point2):
        distance += math.pow(a - b, 2)
    return math.sqrt(distance)
'''

# 计算距离矩阵
def dist_matrix(X):
    n = len(X)
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(i+1, n):
            D[i, j] = np.sqrt(np.sum((X[i] - X[j]) ** 2)) # 欧式距离公式
            #D[i, j] = euler_distance(X[i], X[j])
            #D[j, i] = D[i, j]
    return D

D = dist_matrix(X)

# 定义三种距离计算方法
'''
运用了Numpy的三个内置函数，min、max、mean来定义三种距离计算方法。
单链接（Single Linkage）函数：
计算聚类c1和c2之间的最小距离。它从距离矩阵D中选择聚类c1的元素与聚类c2的元素之间的最小距离，并返回该最小距离。

D[c1] 表示在距离矩阵 D 中选择索引为 c1 的行。
D[c1][:, c2] 表示在选取的行中选择索引为 c2 的列。
np.min(D[c1][:, c2]) 返回所选择的行列区域中的最小值。

全链接（Complete Linkage）函数：
计算聚类c1和c2之间的最大距离。它从距离矩阵D中选择聚类c1的元素与聚类c2的元素之间的最大距离，并返回该最大距离。

D[c1] 表示在距离矩阵 D 中选择索引为 c1 的行。
D[c1][:, c2] 表示在选取的行中选择索引为 c2 的列。
np.max(D[c1][:, c2]) 返回所选择的行列区域中的最大值。

组平均（Average Linkage）函数：
计算聚类c1和c2之间的平均距离。它从距离矩阵D中选择聚类c1的元素与聚类c2的元素之间的距离，并返回这些距离的平均值。
'''

# 输入距离矩阵D、聚类c1、聚类c2
def single_linkage(D, c1, c2):
    return np.min(D[c1][:, c2])
def complete_linkage(D, c1, c2):
    return np.max(D[c1][:, c2])
def average_linkage(D, c1, c2):
    return np.mean(D[c1][:, c2])

# 改进的距离计算方法
'''
def single_linkage(D, c1, c2):
    return np.min(D[np.ix_(c1, c2)])
def complete_linkage(D, c1, c2):
    return np.max(D[np.ix_(c1, c2)])
def average_linkage(D, c1, c2):
    return np.mean(D[np.ix_(c1, c2)])
'''

# 实现凝聚层次聚类算法
def agglomerative_clustering(D, method):
    n = D.shape[0] # 获取样本对象的数量
    clusters = [[i] for i in range(n)] # 初始化聚类，每个对象初始时作为单独的聚类
    min_distances = [] # 用于存储聚类过程中得到的最小距离值

    # 进行聚类
    while len(clusters) > 1:
        # 初始化最小距离和聚类索引
        # np.inf是NumPy库中的一个特殊常量，表示正无穷大的浮点数。
        # 在聚类算法中，np.inf通常用作初始最小距离的设定，以确保在比较过程中的初始最小距离值被正确更新。
        # min_d被初始化为np.inf，这意味着最初的最小距离被设置为正无穷大。
        # 然后在聚类过程中，通过比较不同聚类之间的距离，最小距离值会被逐步更新为更小的值。
        min_d = np.inf
        c1 = 0
        c2 = 0
        # 遍历所有的聚类
        for i in range(len(clusters)):
            for j in range(i+1, len(clusters)):
                # 使用指定的方法计算聚类之间的距离
                d = method(D, clusters[i], clusters[j])
                # 如果找到更小的距离，则更新最小距离和聚类索引
                if d < min_d:
                    min_d = d
                    # 得到最小聚类值的索引
                    c1 = i
                    c2 = j
        # 将最小距离添加到列表中，这里添加的最小距离是添加在列表之后，最终的最小值为min_distances[-1]
        min_distances.append(min_d)
        clusters[c1] += clusters[c2] # 合并聚类，将一个聚类的对象追加到另一个聚类中
        del clusters[c2] # 从列表中删除第二个聚类
        print("当前的聚类结果：{}".format(clusters))
    return clusters, min_distances  # 返回分类结果和最小距离值的列表

# 使用三种距离计算方法进行聚类
# 定义使用聚类计算方法的元组
methods = {"单链法": single_linkage, "全链法": complete_linkage, "组平均法": average_linkage}

# 调用并打印输出聚类方法、聚类结果、最短距离以及距离矩阵
for name, method in methods.items():
    print("聚类方法：", name)
    clusters, min_distances = agglomerative_clustering(D, method)
    print("最终的聚类结果：", clusters)
    print("聚类过程中得到的最短距离：{:.2f}".format(min_distances[-1]))
    print("距离矩阵：")
    print(D)
    print("\n")
