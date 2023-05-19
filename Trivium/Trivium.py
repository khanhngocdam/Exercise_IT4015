import random
# Khởi tạo 80 bit IV
# iv = []
# for i in range(80):
#     iv.append(random.randint(0, 1))
# print("IV : " + ''.join(map(str, iv)))
# # Khởi tạo 80 bit khóa
# key = []
# for i in range(80):
#     key.append(random.randint(0, 1))
# print("Key : " + ''.join(map(str, key)))
iv =  [0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1]
key = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0]

def generate_trivium(iv, key, n): 
# Khởi tạo trạng thái ban đầu của 288 bit
    stream_key = []
    state = [0] * 288
    for i in range(80): 
        state[i] = iv[i]
        state[i+93] = key[i]
    state[285] = state[286] = state[287] = 1
# Vòng lặp sinh dòng khóa
    for i in range(1152 + n) : 
        r1 = state[65] ^ state[92] ^ (state[90] & state[91])
        r2 = state[176] ^ state[161] ^ (state[174] & state[175])
        r3 = state[287] ^ state[242] ^ (state[285] & state[286])
# Nếu chạy tới lần thứ 1153 trở đi thì thêm vào key stream        
        if(i >= 1152): 
            stream_key.append(r1 ^ r2 ^ r3)

        state[92] = r1 ^ state[170] 
        state[176] = r2 ^ state[263]
        state[287] = r3 ^ state[68]
        # Dich 1 vị trí các bit
        state.insert(0, state.pop())
    # Trả về dòng khóa dưới dạng chuỗi bit 
    return ''.join(map(str, stream_key))
# Hàm mã hóa
def encrypt_trivium(iv, key, plaint_text) :
    #Gọi hàm sinh dòng khóa
    key_stream = generate_trivium(iv, key, len(plaint_text)*8)
    #Chuyển dòng khóa dạng binary về string
    segments = [key_stream[i:i+8] for i in range(0, len(key_stream), 8)]
    key_stream_str = ''.join([chr(int(''.join(map(str, segment)), 2)) for segment in segments])
    #Xor 2 string gồm string muốn mã hóa và string stream key
    cipher_str = "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(key_stream_str, plaint_text)])
    #Trả về dạng chuỗi các byte
    return "".join([hex(ord(c)).replace("0x", "").zfill(2) for c in cipher_str])
#Hàm giải mã
def decrypt_trivium(iv, key, cipher_text) : 
    #Chuyển chuỗi byte về dạng string
    cipher_str = bytes.fromhex(cipher_text).decode('latin-1')
    #Sinh dòng khóa 
    key_stream = generate_trivium(iv, key, len(cipher_text)*4)
    #Chuyển dòng khóa dạng binary về dạng string
    segments = [key_stream[i:i+8] for i in range(0, len(key_stream), 8)]
    key_stream_str = ''.join([chr(int(''.join(map(str, segment)), 2)) for segment in segments])
    #Xor bản mã với khóa để thu được bản rõ và trả về bản rõ
    return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(key_stream_str, cipher_str)])

# Nhập message cần mã hóa
Plain_text = input("Enter a message: ")
#Bản mã
cipher_text = encrypt_trivium(iv, key, Plain_text) 
print("Bản mã : " + cipher_text)
#Bản rõ
dec_cipher_text = decrypt_trivium(iv, key, cipher_text)
print("Bản rõ : " + dec_cipher_text)





