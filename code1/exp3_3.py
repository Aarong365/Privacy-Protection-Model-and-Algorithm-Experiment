# 百万富翁问题
# 运用RSA算法

from Crypto.PublicKey import RSA
from Crypto.Util import number

class Millionaire:
    def __init__(self, num_million, max_million=10, num_bits=512):
        self.key = RSA.generate(1024)  # 生成RSA密钥对
        self.million = num_million  # 参与者的百万富翁值，财富的位数
        self.max_million = max_million  # 富翁值的最大范围
        self.num_bits = num_bits  # RSA密钥的位数

    def get_publickey_pem(self):
        return self.key.publickey().exportKey('PEM')  # 导出公钥

    def get_ciphertext(self, peer_key_pem):
        peer_pub_key = RSA.importKey(peer_key_pem)  # 导入对方的公钥
        self.x = number.getRandomNBitInteger(self.num_bits)  # 随机生成的大整数x
        print("随机生成的大整数x:\n", self.x)
        k = pow(self.x, peer_pub_key.e, peer_pub_key.n)  # 使用RSA算法加密私有值x：Alice的公钥a加密 x ^ e mod n，得到 k = Enc(x)
        return k - self.million + 1  # 返回调整后的密文

    def get_sequence_z(self, ciphertext):
        y_u = []
        # Alice 计算Dec（k - j + i），总共计算10个数
        for i in range(self.max_million):
            y_u.append(pow(ciphertext + i, self.key.d, self.key.n))  # 解密密文得到一系列值 （ciphertext+i）^d mod n

        # 输出Alice解密k - j + i（i=1,2,3,...,10）的结果
        for i, y in enumerate(y_u):
            print("y{}: {}".format(i, y))

        p = number.getPrime(self.num_bits // 2)  # 生成素数p 位数为num_bits的一半
        print("产生的随机素数p: \n{}".format(p))
        z_u = [y % p for y in y_u]  # 计算z_u为y_u对p取余
        print("除以素数p取余得到的z : \n{}".format(z_u))
        final_z_u = []
        for i, z in enumerate(z_u):

            # Alice接下来在这个十个数从第 i 个数开始都 +1（嵌入自己的信息i）
            if i >= self.million - 1:  # i 从0开始，million要减1
                z = (z + 1) % p  # 从第 i 个数开始都 +1
            final_z_u.append(z)  # 将调整后的元素添加到最终的z_u中
        print("Alice 添加i之后的z : \n{}".format(final_z_u))
        return p, final_z_u  # 返回素数p和最终的z_u

    def comparing_wealth(self, p, batch_z):
        box = batch_z[self.million - 1]  # 获取第million个元素作为比较值
        # 对方更富有
        if self.x % p == box:
            return True
        # 对方财富较少或相等
        else:
            return False

if __name__ == '__main__':
    Alice = Millionaire(8)  # 创建Alice的实例
    Bob = Millionaire(7)  # 创建Bob的实例
    Alice_pubKey = Alice.get_publickey_pem()  # 获取Alice的公钥
    Bob_ciphertext = Bob.get_ciphertext(Alice_pubKey)  # Bob使用Alice的公钥生成密文
    print("Bob发送给Alice的k - j + 1的值：\n{}".format(Bob_ciphertext))
    print("Alice收到Bob发送的k - j + 1值，计算k - j + i的值(i = 1,2,...,10 共10个数 y0-y9): ")
    Alice_p, Alice_batch_z = Alice.get_sequence_z(Bob_ciphertext)  # Alice生成一组数字
    print("".format(Alice_batch_z))
    result = Bob.comparing_wealth(Alice_p, Alice_batch_z)  # Bob判断自己是否更富有
    print("财富比较结果：")
    if result:
        print("Alice比Bob更加富有")
    else:
        print("Bob比Alice更加富有或者两人财富相等")
