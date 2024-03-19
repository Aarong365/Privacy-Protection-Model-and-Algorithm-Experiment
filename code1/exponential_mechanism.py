# 差分隐私保护-指数机制
import random
import pandas as pd
import numpy as np
from prettytable import PrettyTable

# 创建数据表
data = pd.DataFrame({
    "name": ["Alice", "Bob", "Cral", "David", "Eve"],
    "age": [30, 25, 40, 35, 45],
    "gender": ["F", "M", "M", "M", "F"],
    "salary": [60000, 50000, 90000, 80000, 70000]
})
print("员工工资表：\n", data)
print("")

# 定义打分函数，计算敏感属性（工资）的差异度量
def score(df):
    return np.abs(df["salary"] - target_salary)

# 定义指数机制，计算每个敏感属性（工资）的概率分布
def exponential_mechanism(df, score, sensitivity, epsilon):
    print("当前的隐私预算", epsilon)
    # 计算数据表中每个工资的打分值
    scores = score(df)

    print("打分值：")
    for i in scores:
        print("{}".format(i),end=" ")
    print("")

    # 输出概率归一化处理
    probabilities = np.exp(epsilon * scores / (2 * sensitivity))
    probabilities = probabilities / np.sum(probabilities)  # 给每个员工的工资计算概率，打分值高的工资值，概率大

    print("每个员工工资的概率：")
    for i in probabilities:
        print("{:.4f}".format(i), end=" ")
    print("")
    print("")
    return probabilities

# 定义一个函数，根据不同的隐私预算运行指数机制，并输出结果和概率分布
def compare_results(df, score, sensitivity, epsilon_values):
    # 创建一个PrettyTable对象，用于输出结果的表格
    table = PrettyTable()
    table.field_names = ["隐私预算", "输出结果", "概率分布(Alice-Eve)"]

    # 遍历每个隐私预算
    for epsilon in epsilon_values:
        # 运行指数机制，获取概率分布
        probabilities = exponential_mechanism(df, score, sensitivity, epsilon)
        # 将概率分布转换为字符串，以一行的形式输出
        probabilities_str = ' '.join([f'{p:.4f}' for p in probabilities])
        # 随机选择一个工资作为输出结果
        result = np.random.choice(df["salary"], p=probabilities)
        # 将结果和概率分布添加到表格中
        table.add_row([epsilon, result, probabilities_str])
    # 输出表格
    print("不同隐私预算下的结果和概率分布：")
    print(table)

# 设置查询目标工资
target_salary = random.choice(data["salary"]) # 随机选取查询工资值
print("查询的工资信息是：", target_salary)
# 定义敏感度和隐私预算
sensitivity = abs(score(data).max() - score(data).min())  # 计算敏感度的公式（打分函数敏感度）
# sensitivity = max(abs(score(data) - data["salary"]))  # ppt上的思路
print("敏感度sensitivity：", sensitivity)
print("")
# 隐私预算列表
epsilon_values = [0.0, 0.1, 0.3, 0.5, 0.8, 1.0, 5.0, 10.0, 20.0, 50.0]

# 调用函数，比较不同隐私预算下的差分处理结果和概率分布
result_probabilities = compare_results(data, score, sensitivity, epsilon_values)

'''
代码所要实现的是一个指数机制的示例，它使用一个员工工资表作为输入数据，根据查询目标工资来计算工资的差异度量，
并根据不同的隐私预算运行指数机制，根据概率随机输出一个的工资作为查询结果，并显示每个敏感属性（工资）的概率分布。
'''