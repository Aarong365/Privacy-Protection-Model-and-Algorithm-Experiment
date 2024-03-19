import hashlib
from pybloom_live import ScalableBloomFilter
from Crypto.Cipher import AES
import math

key = b'ThisIsASecretKey'  # 设置密钥（16字节）
cipher = AES.new(key, AES.MODE_ECB)  # 创建AES加密器对象


class BloomFilterIndex:
    def __init__(self, num_keys):
        self.num_keys = num_keys
        self.keys = []  # 密钥列表
        self.bloom_filters = {}  # 存储布隆过滤器的字典
        self.generate_keys()

    def generate_keys(self):
        for i in range(self.num_keys):
            key = hashlib.sha256(str(i).encode()).digest()  # 使用SHA256哈希算法生成密钥
            self.keys.append(key)  # 将生成的密钥添加到密钥列表中

    def build_index(self, document_id, keywords):
        for keyword in keywords:
            if keyword not in self.bloom_filters:
                self.bloom_filters[keyword] = ScalableBloomFilter(
                    mode=ScalableBloomFilter.SMALL_SET_GROWTH)  # 创建布隆过滤器对象
            padded_keyword = self.pad_keyword(keyword)
            encrypted_keyword = cipher.encrypt(padded_keyword.encode())  # 使用AES加密关键词
            x_values = [self.pseudo_random_function(key, encrypted_keyword) for key in self.keys]  # 计算关键词对应的r个x值
            encrypted_doc_id = cipher.encrypt(str(document_id).encode())  # 使用AES加密文档标识
            y_values = [self.pseudo_random_function(encrypted_doc_id, x_value) for x_value in x_values]  # 计算文档标识对应的r个y值
            for y_value in y_values:
                self.bloom_filters[keyword].add(y_value)  # 将y值添加到对应关键词的布隆过滤器中

    def pad_keyword(self, keyword):
        block_size = 16  # AES块大小为16字节
        num_blocks = math.ceil(len(keyword) / block_size)
        padded_length = num_blocks * block_size
        padding = padded_length - len(keyword)
        padded_keyword = keyword + chr(padding) * padding
        return padded_keyword

    def pseudo_random_function(self, key, input_data):
        hmac = hashlib.sha256()
        hmac.update(bytes(key))
        hmac.update(bytes(str(input_data), 'utf-8'))
        return hmac.digest()  # 使用HMAC-SHA256伪随机函数计算值

    def search_documents(self, keywords):
        document_ids = set()
        for document_id in range(1, 7):  # 在文档1到6中进行查找
            for keyword in keywords:
                if keyword in self.bloom_filters:
                    padded_keyword = self.pad_keyword(keyword)
                    encrypted_keyword = cipher.encrypt(padded_keyword.encode())  # 使用AES加密关键词
                    x_prime_values = [self.pseudo_random_function(key, encrypted_keyword) for key in
                                      self.keys]  # 计算陷门对应的r个x'值
                    encrypted_doc_id = cipher.encrypt(str(document_id).encode())  # 使用AES加密文档标识
                    y_prime_values = [self.pseudo_random_function(encrypted_doc_id, x_prime) for x_prime in
                                      x_prime_values]  # 计算文档标识对应的r个y'值
                    if all(
                            y_prime in self.bloom_filters[keyword]
                            for y_prime in y_prime_values
                    ):  # 检查所有y'值是否都在对应关键词的布隆过滤器中
                        document_ids.add(document_id)  # 若满足条件，则将文档标识添加到结果集中
        return document_ids  # 返回包含关键词的文档标识集合

index = BloomFilterIndex(num_keys=10)  # 创建布隆过滤器索引对象

# 添加文档
index.build_index(1, ['In', '1977', 'Dalenius', 'articulated', 'a', 'desideratum', 'for', 'statistical', 'databases:', 'nothing', 'about', 'an', 'individual', 'should', 'be', 'learnable', 'from', 'then', 'database', 'that', 'cannot', 'be', 'learned', 'without', 'access', 'to', 'the', 'database'])
index.build_index(2, ['We', 'give', 'a', 'general', 'impossibility', 'result', 'showing', 'that', 'a', 'formalization', 'of', 'Dalenius’', 'goal', 'along', 'the', 'lines', 'of', 'semantic', 'security', 'cannot', 'be', 'achieved'])
index.build_index(3, ['Contrary', 'to', 'intuition,', 'a', 'variant', 'of', 'the', 'result', 'threatens', 'the', 'privacy', 'even', 'of', 'someone', 'not', 'in', 'the', 'database'])
index.build_index(4, ['This', 'state', 'of', 'affairs', 'suggests', 'a', 'new', 'measure,', 'differential', 'privacy,', 'which,', 'intuitively,', 'captures', 'the', 'increased', 'risk', 'to', 'one’s', 'privacy', 'incurred', 'by', 'participating', 'in', 'a', 'database'])
index.build_index(5, ['The', 'techniques', 'developed', 'in', 'a', 'sequence', 'of', 'papers', ',', 'culminating', 'in', 'those', 'described', 'in', ',', 'can', 'achieve', 'any', 'desired', 'level', 'of', 'privacy', 'under', 'this', 'measure'])
index.build_index(6, ['In', 'many', 'cases,', 'extremely', 'accurate', 'information', 'about', 'the', 'database', 'can', 'be', 'provided', 'while', 'simultaneously', 'ensuring', 'very', 'high', 'levels', 'of', 'privacy'])

# 搜索关键词
keywords_to_search = [
    "1977", "Dalenius", "statistical", "databases",
    "impossibility", "result", "semantic", "security",
    "intuition", "variant", "privacy", "database",
    "state", "affairs", "measure", "differential",
    "techniques", "sequence", "papers", "described",
]
for keyword in keywords_to_search:
    result = index.search_documents([keyword])  # 在索引中搜索关键词
    if result:
        print(f"Keyword '{keyword}' is found in {result}.")  # 若存在结果，则打印包含关键词的文档标识
    else:
        print(f"Keyword '{keyword}' is not found.")  # 若不存在结果，则打印未找到关键词
