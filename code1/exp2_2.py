# python库函数实现布隆过滤器
from pybloom_live import BloomFilter # 使用了pybloom_live库中的BloomFilter数据结构

bloom_filter = BloomFilter(capacity=100, error_rate=0.01) # 创建了一个布隆过滤器对象bloom_filter，指定了容量为100和误判率为0.01。
documents = {"ID1":['In', '1977', 'Dalenius', 'articulated', 'a', 'desideratum', 'for', 'statistical', 'databases', 'nothing', 'about', 'an', 'individual', 'should', 'be', 'learnable', 'from', 'then', 'database', 'that', 'cannot', 'be', 'learned', 'without', 'access', 'to', 'the', 'database'],
             "ID2":['We', 'give', 'a', 'general', 'impossibility', 'result', 'showing', 'that', 'a', 'formalization', 'of', 'Dalenius', 'goal', 'along', 'the', 'lines', 'of', 'semantic', 'security', 'cannot', 'be', 'achieved'],
             "ID3":['Contrary', 'to', 'intuition', 'a', 'variant', 'of', 'the', 'result', 'threatens', 'the', 'privacy', 'even', 'of', 'someone', 'not', 'in', 'the', 'database'],
             "ID4":['This', 'state', 'of', 'affairs', 'suggests', 'a', 'new', 'measure', 'differential', 'privacy', 'which', 'intuitively', 'captures', 'the', 'increased', 'risk', 'to', 'one’s', 'privacy', 'incurred', 'by', 'participating', 'in', 'a', 'database'],
             "ID5":['The', 'techniques', 'developed', 'in', 'a', 'sequence', 'of', 'papers', 'culminating', 'in', 'those', 'described', 'in', 'can', 'achieve', 'any', 'desired', 'level', 'of', 'privacy', 'under', 'this', 'measure'],
             "ID6":['In', 'many', 'cases', 'extremely', 'accurate', 'information', 'about', 'the', 'database', 'can', 'be', 'provided', 'while', 'simultaneously', 'ensuring', 'very', 'high', 'levels', 'of', 'privacy']}
for doc_id, keyword_list in documents.items():
    for keyword in keyword_list:
        bloom_filter.add(keyword)
k = ['articulated', 'desideratum', 'databases','formalization', 'privacy',
     'Dalenius', 'techniques', 'extremely', 'information', 'simultaneously',
     'measure', 'intuition', 'variant', 'showing', 'result',
     'new', 'threatens', 'captures', 'incurred', 'participating', 'apple', 'banana']
for keyword in k:
    if keyword in bloom_filter:
        keyword_found_id = set() # 设置一个集合，添加存在关键词的文档id，保证不会重复
        for key, value in documents.items():
            if keyword in value:
                keyword_found_id.add(key)
        print("关键词'{}'已经存在，存在于以下文档:{}。".format(keyword, keyword_found_id))
    else:
        print("关键词'{}'不存在。".format(keyword))



