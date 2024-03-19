# 乘法同态加解密算法
# RSA同态加解密算法
import math
from Crypto.Util.number import *

# 模平方重复计算
def fastExpMod(b, e, n):
    # b是底数 e是指数 n是模数 (b^e) mod n
    a = 1
    while e != 0:
        if (e & 1) == 1:   # 从最低位扫描按位取数，当前位等于1，进行a的计算
            a = (a * b) % n
        # 当前位等于0的情况，a不用计算
        e = e >> 1  # 右移一位到下一位进行计算
        b = (b * b) % n
    return a

# 判断素数
def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

# 欧几里得算法判断两个数是否互素
def gcd(a, b):
    while a % b != 0:
        r = a % b
        a, b = b, r
    return b

# RSA加密算法
def encrypt(m, e, n):
    #return pow(m, e, n)  # 计算m^e模n
    return fastExpMod(m, e, n) # 使用模平方重复法快速计算m^e模n

# RSA解密算法
def decrypt(c, d, n):
    # return pow(c, d, n)  # 计算c^d模n
    return fastExpMod(c, d, n) # 使用模平方重复法快速计算c^d模n

# RSA同态加密算法
def homomorphic_encryption(m1, m2, e, n):
    c1 = encrypt(m1, e, n)
    c2 = encrypt(m2, e, n)
    #print(c1,c2,c1*c2)
    return (c1 * c2) % n

# RSA同态解密算法
def homomorphic_decryption(c3, d3, n):
    m = decrypt(c3, d3, n) # c3^d3 mod n
    return m

 # p,q 生成512位大整数
    #p = getPrime(512)
    #q = getPrime(512)

def main():
    m1, m2 = eval(input("输入明文m1,m2:"))
    p, q = eval(input("输入p和q："))
    e = eval(input("输入公钥e："))
    if is_prime(p) and is_prime(q):
        n = p * q
        phi = (p - 1) * (q - 1)
        # print(phi)
        if gcd(e, phi) == 1 and e > 1:
            d = inverse(e, phi)  # 计算e关于模数ϕ的逆元d，私钥d
            c3 = homomorphic_encryption(m1, m2, e, n)  # 同态加密的密文c3
            print("(c1*c2)进行RSA加密得到c3，并且c3 = {} mod {} = {} ".format(fastExpMod(m1*m2, e, n), n, c3))
            m3 = homomorphic_decryption(c3, d, n)
            print("c3解密得到m3,并且m3 = {} * {} = {}".format(m1, m2, m1*m2))

            # 验证其算法的同态性质
            if (c3 == ((encrypt(m1, e, n) * encrypt(m2, e, n)) % n)) and (m3 == (m1 * m2) % n):
                print("RSA算法满足乘同态性质！")
            else:
                print("不满足乘法同态！")
        else:
            print("输入公钥e有误！")
    else:
        print("p和q必须是素数！")


'''
测试案例1：
12,5
23,19
17
m3 = m1*m2 = 60; c3 = (c1 * c2) mod n = (331 * 61) mod 437 = 89
测试案例2：
64,59
7,11
17

测试案例3：
输入明文m1,m2:12,5
输入p和q：55,11
输入公钥e：5
p和q必须是素数！

测试案例4：
输入明文m1,m2:15,7
输入p和q：17,11
输入公钥e：6
输入公钥e有误！

测试案例5：
输入明文m1,m2:-12,5
输入p和q：7,11
输入公钥e：17
(m1*m2)进行RSA加密得到c3，并且c3 = 19 mod 77 = 19 
c3解密得到m3,并且m3 = -12 * 5 = -60
RSA算法满足乘同态性质！
'''
main()