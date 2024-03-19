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

# 定义打分函数，计算工资（敏感属性）的差异度量
def score(df):
    return np.abs(df["salary"] - target_salary)

# 定义指数机制，计算每个工资的概率分布
def exponential_mechanism(df, score, sensitivity, epsilon):
    # 计算数据表中每个工资的打分
    scores = score(df)

    # 输出概率归一化处理
    probabilities = np.exp(-epsilon * scores / (2 * sensitivity))
    probabilities = probabilities / np.sum(probabilities)
    return probabilities

def compare_results(df, score, sensitivity, epsilon_values):
    # 创建一个PrettyTable对象，用于输出结果的表格
    table = PrettyTable()
    table.field_names = ["隐私预算", "工资", "概率分布", "是否满足要求"]

    # 遍历每个隐私预算
    for epsilon in epsilon_values:
        # 运行指数机制，获取概率分布
        probabilities = exponential_mechanism(df, score, sensitivity, epsilon)
        # 将概率分布转换为字符串，以一行的形式输出
        probabilities_str = ' '.join([f'{p:.4f}' for p in probabilities])

        # 检查是否满足 exp(εq(D, r) / (2Δq)) 的要求
        satisfies_requirement = np.all(probabilities < np.exp(epsilon * score(df) / (2 * sensitivity)))

        # 输出结果和概率分布，并标记是否满足要求
        for i, salary in enumerate(df["salary"]):
            table.add_row([epsilon, salary, probabilities_str, "满足" if satisfies_requirement else "不满足"])

    # 输出表格
    print("不同隐私预算下的结果和概率分布：")
    print(table)

# 设置查询目标工资
target_salary = 1

# 定义敏感度和隐私预算
sensitivity = abs(score(data).max() - score(data).min())
print("敏感度sensitivity：", sensitivity)
print("")

# 隐私预算列表
epsilon_values = [0.0, 0.1, 0.3, 0.5, 0.8, 1.0, 5.0, 10.0, 20.0]

# 调用函数，比较不同隐私预算下的差分处理结果和概率分布
result_probabilities = compare_results(data, score, sensitivity, epsilon_values)

