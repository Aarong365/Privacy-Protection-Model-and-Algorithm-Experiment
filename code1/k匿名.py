import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
raw_data = {
    'name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy','Jelly'],
    'age': [42, 52, 36, 24, 73,78],
    'preTestScore': [4, 24, 31, 2, 3,11],
    'postTestScore': [25, 94, 57, 62, 70,34]}
af = pd.DataFrame(raw_data, columns = ['name','age', 'preTestScore', 'postTestScore'])
print("原表：")
print(af)

# 创建年龄范围的分组
bins = [0, 20, 40, 70, np.inf] # 定义分组边界
labels = ['<20', '20-40', '40-70', '>70'] # 定义分组标签
af['age'] = pd.cut(af['age'], bins=bins, labels=labels) # 使用cut方法替换原有的age列

# 按照年龄范围进行排序
order = ['<20', '20-40', '40-70', '>70'] # 定义排序顺序
af.sort_values(by='age', key=lambda x: x.map(order.index), inplace=True) # 使用sort_values方法按照顺序排序

# 去除first_name和last_name
af.drop(columns=['name'], inplace=True) # 使用drop方法删除不需要的列

af.reset_index(drop=True, inplace=True)
print("泛化后：")
print(af)




