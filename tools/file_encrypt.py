import base64

# 定义待编码的字符串
input_string = "04-42-1A-98-A1-AC"

# 步骤1: 进行base64编码
base64_encoded = base64.b64encode(input_string.encode()).decode()

# 步骤2: 进行异或加密
xor_key = "s"
encrypted_result = ''.join(chr(ord(char) ^ ord(xor_key)) for char in base64_encoded)

# 步骤3: 进行第二次base64编码
final_encoded_result = base64.b64encode(encrypted_result.encode()).decode()

# 步骤4: 在命令行输出最终加密结果
print(final_encoded_result)


# 最终加密结果
final_encoded_result = final_encoded_result

# 步骤1: 进行第二次base64解码
decoded_result = base64.b64decode(final_encoded_result).decode()

# 步骤2: 进行异或解密
xor_key = "s"
decrypted_result = ''.join(chr(ord(char) ^ ord(xor_key)) for char in decoded_result)

# 步骤3: 进行base64解码，得到原始字符串
original_string = base64.b64decode(decrypted_result).decode()

# 打印原始字符串
print(original_string)