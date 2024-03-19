# 密文检索-布隆过滤器
import mmh3

# 布隆过滤器类
class BloomFilter:
    def __init__(self, size, hash_count):
        super(BloomFilter, self).__init__()
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [0] * size

    # 添加关键词到布隆过滤器，并打印索引和当前过滤器状态
    def add(self, keyword, document_id):
        index = 0
        for seed in range(self.hash_count):
            index = mmh3.hash(keyword, seed) % self.size
            self.bit_array[index] = 1
        print("添加关键词 '{}', 文档: {}，该关键词在过滤器的索引: {}".format(keyword, document_id, index))
        print("当前的过滤器状态: {}\n".format(self.bit_array))

    def contains(self, keyword):
        index = 0
        for seed in range(self.hash_count):
            index = mmh3.hash(keyword, seed) % self.size
            if self.bit_array[index] == 0: # 如果关键词在布隆过滤器中找不到映射
                print("关键词:{}在过滤器中不存在".format(keyword))
                return
        print("关键词'{}'已经存在, 索引值: {}".format(keyword, index))

# 创建布隆过滤器实例
filter_size = 1000  # 过滤器大小
hash_count = 3    # 哈希函数数量
bloom_filter = BloomFilter(filter_size, hash_count) # 调用布隆过滤器BloomFilter类

# 添加关键词和对应的文档编号
# 文档数据
documents = {"ID1": ['In', '1977', 'Dalenius', 'articulated', 'a', 'desideratum', 'for', 'statistical', 'databases', 'nothing', 'about', 'an', 'individual', 'should', 'be', 'learnable', 'from', 'then', 'database', 'that', 'cannot', 'be', 'learned', 'without', 'access', 'to', 'the', 'database'],
             "ID2": ['We', 'give', 'a', 'general', 'impossibility', 'result', 'showing', 'that', 'a', 'formalization', 'of', 'Dalenius', 'goal', 'along', 'the', 'lines', 'of', 'semantic', 'security', 'cannot', 'be', 'achieved'],
             "ID3": ['Contrary', 'to', 'intuition', 'a', 'variant', 'of', 'the', 'result', 'threatens', 'the', 'privacy', 'even', 'of', 'someone', 'not', 'in', 'the', 'database'],
             "ID4": ['This', 'state', 'of', 'affairs', 'suggests', 'a', 'new', 'measure', 'differential', 'privacy', 'which', 'intuitively', 'captures', 'the', 'increased', 'risk', 'to', 'one’s', 'privacy', 'incurred', 'by', 'participating', 'in', 'a', 'database'],
             "ID5": ['The', 'techniques', 'developed', 'in', 'a', 'sequence', 'of', 'papers', 'culminating', 'in', 'those', 'described', 'in', 'can', 'achieve', 'any', 'desired', 'level', 'of', 'privacy', 'under', 'this', 'measure'],
             "ID6": ['In', 'many', 'cases', 'extremely', 'accurate', 'information', 'about', 'the', 'database', 'can', 'be', 'provided', 'while', 'simultaneously', 'ensuring', 'very', 'high', 'levels', 'of', 'privacy']}

# 输入文档数据
for doc_id, keyword_list in documents.items():
    for keyword in keyword_list:
        bloom_filter.add(keyword, doc_id)

# 选取20个关键词
k = ['articulated', 'desideratum', 'databases','formalization', 'privacy',
     'Dalenius', 'techniques', 'extremely', 'information', 'simultaneously',
     'measure', 'intuition', 'variant', 'showing', 'result',
     'new', 'threatens', 'apple', 'banana', 'pear']

# 查询关键词所在过滤器映射
print("查询结果:")
for i in k:
    bloom_filter.contains(i)

'''
#简单测试案例
bloom_filter.add("apple", 1)
bloom_filter.add("banana", 2)
bloom_filter.add("orange", 3)

bloom_filter.contains("apple")
bloom_filter.contains("banana")
bloom_filter.contains("orange")
bloom_filter.contains("pear")
'''