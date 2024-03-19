import math
import pandas as pd
import numpy as np

# 计算基于拉普拉斯分布的噪声
def laplace_noisy(sensitivety, epsilon):
    noisy = np.random.laplace(0, sensitivety / epsilon, 1)
    return noisy

# 基于laplace的分布函数的反函数计算
def laplace_noisy2(sensitivety, epsilon):
    b = sensitivety / epsilon
    u1 = np.random.random()
    u2 = np.random.random()
    if u1 <= 0.5:
        noisy = -b * np.log(1. - u2)
    else:
        noisy = b * np.log(u2)
    return noisy

# 计算基于拉普拉斯加噪的混淆值
def laplace_mech(data, sensitivety, epsilon):
    data += laplace_noisy(sensitivety, epsilon)
    return data

class serve():
    def __init__(self,len,D):
        self.D = D
        self.len = len

    def check(self):
        d = self.D.loc[self.D.index <= (self.len-1)]
        # print(d)
        d = d['infection HBV'].value_counts().to_dict()
        sum = float(d['yes'])
        print('加噪声前的数据：',sum)
        sensitivety = 1
        epsilon = 2
        data_noisy = laplace_mech(sum, sensitivety, epsilon)
        print("添加噪声后的数据 = %.16f" % data_noisy)

    def table(self,):
        self.D = pd.DataFrame(
            data=[['alice', 'yes'], ['bob', 'no'], ['carolyn', 'no'], ['david', 'yes'], ['findy', 'no'], ['nancy', 'yes'],
                  ['jack', 'no'], ['lindsay', 'no'], ['wahana', 'no'], ['luna', 'yes']],
            columns=['name', 'infection HBV'])
        print('原始数据表，在服务器端生成，只有服务器端掌握\n',self.D)
        return self.D['name']

if __name__=='__main__':
  # 生成数据表
  len = int(input('查询的行数：'))
  df = serve(len,0)
  D = df.table()
  print('这是查询者掌握的不显示敏感信息的数据表\n',D)
  df.check()
