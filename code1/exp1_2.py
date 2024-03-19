# 导入sklearn库实现层次聚类算法
'''
代码逻辑：
n_clusters为聚类的个数，即要查找的聚类数；
metric用于计算链接的度量，可以使用“euclidean”,“l1”,“l2”,“manhattan”,“cosine”,或者“precomputed”。 如果设置为“无”，则使用“euclidean”。
如果linkage设置为“ward”，则只接受“euclidean”。
如果“precomputed””，则需要距离矩阵作为拟合方法的输入。上述代码使用的是euclidean；
linkage为使用的距离计算方法。这个参数可以选择设置为{‘ward’, ‘complete’, ‘average’, ‘single’}, 默认为ward。
这里我使用的距离计算方法为average，即组平均法。
随后使用fit_predict方法进行聚类，fit_predict方法会拟合并返回每个样本的聚类分配结果。
除了拟合之外，该方法还返回训练集中每个样本的聚类分配结果。这个方法返回的结果为聚类标签。
得到fit_predict返回结果之后，使用matplotlib.pyplot库的scatter方法生成散点图：

'''
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
# 导入numpy库
import numpy as np
# 生成随机数据
X = np.random.rand(10, 2)
print(X)

# 创建层次聚类对象，设置聚类个数为3，使用欧氏距离和最小方差法
model = AgglomerativeClustering(n_clusters=3, metric='euclidean', linkage='average')

# 对数据进行聚类
y = model.fit_predict(X)
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis')

# 打印聚类结果
print("每个数据所属的簇编号: ",y)
print("每个簇的成员: \n",model.children_)
plt.show()

