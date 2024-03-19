# Paillier 同态加解密算法（加同态）

from phe import paillier

# 生成密钥对
public_key, private_key = paillier.generate_paillier_keypair()

# 加密函数
def encrypt(public_key, plaintext):
    ciphertext = public_key.encrypt(plaintext)
    return ciphertext

# 解密函数
def decrypt(private_key, ciphertext):
    plaintext = private_key.decrypt(ciphertext)
    return plaintext

# 同态加法
def homomorphic_addition(ciphertext1, ciphertext2):
    result = ciphertext1 + ciphertext2
    return result


# 测试案例：
plaintext1 = 5585
plaintext2 = 4242

ciphertext1 = encrypt(public_key, plaintext1)
ciphertext2 = encrypt(public_key, plaintext2)

# 对相加后的密文进行解密
homomorphic_result = homomorphic_addition(ciphertext1, ciphertext2)
decrypted_result = decrypt(private_key, homomorphic_result)

print("同态加法计算(ciphertext1+ciphertext2)解密后的结果为:{}".format(decrypted_result))
print("明文相加(plaintext1+plaintext2)的结果为:{}".format(plaintext1 + plaintext2))

# 验证同态性
if decrypted_result == (plaintext1 + plaintext2):
    print("Paillier算法满足加法同态。")
else:
    print("Paillier算法不满足加法同态性。")



'''
plaintext1 = -10
plaintext2 = 5

plaintext1 = -10.5
plaintext2 = 5.1


plaintext1 = 10
plaintext2 = 5
'''