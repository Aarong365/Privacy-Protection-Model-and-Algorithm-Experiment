# 基于文档-关键词索引的方案(基于布隆过滤器的密文关键词检索方案)
import hashlib
from pybloom_live import ScalableBloomFilter
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

class BloomFilterIndex:
    def __init__(self, num_keys):
        self.num_keys = num_keys
        self.keys = []  # 密钥列表
        self.bloom_filters = {}  # 存储布隆过滤器的字典
        self.generate_keys() # 生成密钥
        self.document_id_list = [] # 记录添加的文档id列表

    def generate_keys(self):
        for i in range(self.num_keys):
            key = hashlib.sha256(str(i).encode()).digest()  # 使用SHA256哈希算法生成密钥
            self.keys.append(key)  # 将生成的密钥添加到密钥列表中

    # 陷门函数
    def trap_function(self, key, input_data):
        hmac = hashlib.sha256()
        hmac.update(bytes(key))
        hmac.update(bytes(str(input_data), 'utf-8'))
        return hmac.digest()  # 使用HMAC-SHA256伪随机函数计算值

    def build_index(self, document_id, keywords):
        self.document_id_list.append(document_id) # 记录关键词所在的文档id
        for keyword in keywords:
            if keyword not in self.bloom_filters:
                self.bloom_filters[keyword] = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)  # 创建布隆过滤器对象
            x_values = [self.trap_function(key, keyword) for key in self.keys]  # 计算关键词对应的r个x值
            y_values = [self.trap_function(document_id, x_value) for x_value in x_values]  # 计算文档标识对应的r个y值
            for y_value in y_values:
                self.bloom_filters[keyword].add(y_value)  # 将y值添加到对应关键词的布隆过滤器中

    def gen_trapdoor(self, keyword):
        x_prime_values = []
        x = 0
        for key in self.keys:
            x = self.trap_function(key, keyword)
            x_prime_values.append(x)
        return x_prime_values

    def search(self, keywords):
        document_ids = set()
        for document_id in self.document_id_list:  # 在文档1到6中进行查找
            for keyword in keywords:
                if keyword in self.bloom_filters:
                    x_prime_values = self.gen_trapdoor(keyword) # 计算陷门对应的r个x'值
                    y_prime_values = [self.trap_function(document_id, x_prime)for x_prime in x_prime_values]  # 计算文档标识对应的r个y'值

                    # 如果所有的y'值都存在于布隆过滤器中，那么all()函数将返回True，表示所有元素都满足条件。否则，如果至少有一个y'值不存在于布隆过滤器中，all()函数将返回False。
                    if all(y_prime in self.bloom_filters[keyword] for y_prime in y_prime_values):  # 检查所有y'值是否都在对应关键词的布隆过滤器中
                        document_ids.add(document_id)  # 若满足条件，则将文档标识添加到结果集中
        return document_ids  # 返回包含关键词的文档标识集合

index = BloomFilterIndex(num_keys=10)  # 创建布隆过滤器索引对象

# 文档数据
documents = {1: ['In', '1977', 'Dalenius', 'articulated', 'a', 'desideratum', 'for', 'statistical', 'databases', 'nothing', 'about', 'an', 'individual', 'should', 'be', 'learnable', 'from', 'then', 'database', 'that', 'cannot', 'be', 'learned', 'without', 'access', 'to', 'the', 'database'],
             2: ['We', 'give', 'a', 'general', 'impossibility', 'result', 'showing', 'that', 'a', 'formalization', 'of', 'Dalenius', 'goal', 'along', 'the', 'lines', 'of', 'semantic', 'security', 'cannot', 'be', 'achieved'],
             3: ['Contrary', 'to', 'intuition', 'a', 'variant', 'of', 'the', 'result', 'threatens', 'the', 'privacy', 'even', 'of', 'someone', 'not', 'in', 'the', 'database'],
             4: ['This', 'state', 'of', 'affairs', 'suggests', 'a', 'new', 'measure', 'differential', 'privacy', 'which', 'intuitively', 'captures', 'the', 'increased', 'risk', 'to', 'one’s', 'privacy', 'incurred', 'by', 'participating', 'in', 'a', 'database'],
             5: ['The', 'techniques', 'developed', 'in', 'a', 'sequence', 'of', 'papers', 'culminating', 'in', 'those', 'described', 'in', 'can', 'achieve', 'any', 'desired', 'level', 'of', 'privacy', 'under', 'this', 'measure'],
             6: ['In', 'many', 'cases', 'extremely', 'accurate', 'information', 'about', 'the', 'database', 'can', 'be', 'provided', 'while', 'simultaneously', 'ensuring', 'very', 'high', 'levels', 'of', 'privacy']}

# 用户检索的关键词
keywords_to_search = ['articulated', 'desideratum', 'databases', 'formalization', 'privacy',
                      'Dalenius', 'techniques', 'extremely', 'information', 'simultaneously',
                      'measure', 'intuition', 'variant', 'showing', 'result',
                      'new', 'threatens', 'captures', 'incurred', 'participating','pear']

def main():
    # 添加文档数据
    for doc_id, keyword_list in documents.items():
        index.build_index(doc_id, keyword_list)

    # 进行关键词检索
    for keyword in keywords_to_search:
        result = index.search([keyword])  # 在索引中搜索关键词
        if result:
            print("所检索的关键词为 '{}' 包含在文档{}中。".format(keyword, result))  # 若存在结果，则打印包含关键词的文档标识
        else:
            print("所检索的关键词'{}'不存在。".format(keyword))  # 若不存在结果，则打印未找到关键词

main()