# 使用scipy库实现层次聚类算法
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt

# 准备数据集
data = np.random.rand(4, 1)
print(data)

# 聚类
linkage_matrix = linkage(data, method='average')

# 可视化聚类结果
dendrogram(linkage_matrix)
A=[]
for i in range(len(data)):
    a=chr(i+ord('A'))
    A.append(a)

print(linkage_matrix)
plt.show()
