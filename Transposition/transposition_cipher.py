import math

def encrypt_transposition(key, message):
    # Tạo các cột trống dựa trên độ dài của key
    ciphertext = [''] * key
    
    # Chia tin nhắn vào các cột
    for column in range(key):
        current_index = column
        
        while current_index < len(message):
            ciphertext[column] += message[current_index]
            current_index += key
            
    return ''.join(ciphertext)

def decrypt_transposition(key, message):
    # Tính toán số hàng cần thiết
    num_columns = math.ceil(len(message) / key)
    num_rows = key
    num_shaded_boxes = (num_columns * num_rows) - len(message)
    
    plaintext = [''] * num_columns
    column = 0
    row = 0
    
    for symbol in message:
        plaintext[column] += symbol
        column += 1
        
        # Nếu đi hết hàng hoặc gặp ô trống (shaded box) ở cuối
        if (column == num_columns) or (column == num_columns - 1 and row >= num_rows - num_shaded_boxes):
            column = 0
            row += 1
            
    return ''.join(plaintext)

# --- Chạy thử ---
key = 8
msg = "Common sense is not so common."

encrypted = encrypt_transposition(key, msg)
decrypted = decrypt_transposition(key, encrypted)

print(f"Original:  {msg}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")