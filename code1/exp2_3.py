# 3 倒排索引算法

def inverted_index(documents):
    index = {}
    for doc_id, document in enumerate(documents):
        words = document.split() # 将文档按空格分割成单词列表
        print(words)
        for word in words:
            if word not in index:
                index[word] = set() # 如果单词不存在于索引中，初始化一个空的文档ID集合
            index[word].add(doc_id) # 将当前文档ID添加到单词对应的文档ID集合中
            print("当前的索引{}".format(index))
    print(index)
    return index

def query(index, keywords):
    result = None
    for keyword in keywords:
        if keyword in index:
            if result == None:
                result = index[keyword] # 如果结果集为空，将当前关键词对应的文档ID集合赋值给结果集
            else:
                result = result.intersection(index[keyword]) # 求当前关键词对应的文档ID集合与结果集的交集
        else:
            return "关键词不存在" # 如果关键词不存在于索引中，直接返回提示
    return result

'''documents = ["In 1977 Dalenius articulated a desideratum for statistical databases nothing about an individual should be learnable from then database that cannot be learned without access to the database",
            "We give a general impossibility result showing that a formalization of Dalenius goal along the lines of semantic security cannot be achieved",
            "Contrary to intuition a variant of the result threatens the privacy even of someone not in the database",
             "This state of affairs suggests a new measure differential privacy which intuitively captures the increased risk to ones privacy incurred by participating in a database",
             "The techniques developed in a sequence of papers  culminating in those described in  can achieve any desired level of privacy under this measure",
             "In many cases extremely accurate information about the database can be provided while simultaneously ensuring very high levels of privacy"
             ]'''
documents = ["it is what it is", "what is it", "it is a banana"]
keywords = ["what", "is", "it"]
index = inverted_index(documents)
for word, docs in index.items():
    print("{}: {}".format(word,docs))
# 查询关键词
#keywords = ["database","a","the","privacy"]
query_result = query(index, keywords)
# 输出查询结果
print("关键词: {}".format(keywords))
print("查询结果: {}".format(query_result))

for id in query_result:
    print("检索的文档结果为：{}".format(documents[id]))

'''documents = ["it is what it is", "what is it", "it is a banana"]
keywords = ["what", "is", "it"]'''

'''keywords = ['articulated', 'desideratum', 'databases','formalization', 'privacy',
     'Dalenius', 'techniques', 'extremely', 'information', 'simultaneously',
     'measure', 'intuition', 'variant', 'showing', 'result',
     'new', 'threatens', 'captures', 'incurred', 'participating']'''