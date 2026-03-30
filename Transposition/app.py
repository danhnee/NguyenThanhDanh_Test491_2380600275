import tkinter as tk
from tkinter import messagebox
import math

# --- Thuật toán mã hóa ---
def encrypt_logic(key, message):
    ciphertext = [''] * key
    for column in range(key):
        current_index = column
        while current_index < len(message):
            ciphertext[column] += message[current_index]
            current_index += key
    return ''.join(ciphertext)

def decrypt_logic(key, message):
    num_columns = math.ceil(len(message) / key)
    num_rows = key
    num_shaded_boxes = (num_columns * num_rows) - len(message)
    plaintext = [''] * num_columns
    column = 0
    row = 0
    for symbol in message:
        plaintext[column] += symbol
        column += 1
        if (column == num_columns) or (column == num_columns - 1 and row >= num_rows - num_shaded_boxes):
            column = 0
            row += 1
    return ''.join(plaintext)

# --- Xử lý sự kiện UI ---
def handle_encrypt():
    try:
        key = int(entry_key.get())
        msg = entry_input.get("1.0", tk.END).strip()
        if not msg:
            messagebox.showwarning("Lỗi", "Vui lòng nhập nội dung!")
            return
        result = encrypt_logic(key, msg)
        entry_output.delete("1.0", tk.END)
        entry_output.insert(tk.END, result)
    except ValueError:
        messagebox.showerror("Lỗi", "Key phải là một số nguyên!")

def handle_decrypt():
    try:
        key = int(entry_key.get())
        msg = entry_input.get("1.0", tk.END).strip()
        if not msg:
            messagebox.showwarning("Lỗi", "Vui lòng nhập nội dung cần giải mã!")
            return
        result = decrypt_logic(key, msg)
        entry_output.delete("1.0", tk.END)
        entry_output.insert(tk.END, result)
    except ValueError:
        messagebox.showerror("Lỗi", "Key phải là một số nguyên!")

# --- Giao diện (UI) ---
root = tk.Tk()
root.title("Transposition Cipher Tool")
root.geometry("500x450")

# Label & Input cho Message
tk.Label(root, text="Nhập nội dung (Input):", font=("Arial", 10, "bold")).pack(pady=5)
entry_input = tk.Text(root, height=5, width=50)
entry_input.pack(pady=5)

# Label & Input cho Key
tk.Label(root, text="Nhập Key (Số nguyên):", font=("Arial", 10, "bold")).pack(pady=5)
entry_key = tk.Entry(root, width=10)
entry_key.pack(pady=5)

# Khung chứa nút bấm
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn_encrypt = tk.Button(frame_buttons, text="Mã hóa (Encrypt)", command=handle_encrypt, bg="green", fg="white", padx=10)
btn_encrypt.pack(side=tk.LEFT, padx=5)

btn_decrypt = tk.Button(frame_buttons, text="Giải mã (Decrypt)", command=handle_decrypt, bg="blue", fg="white", padx=10)
btn_decrypt.pack(side=tk.LEFT, padx=5)

# Label & Output cho Result
tk.Label(root, text="Kết quả (Result):", font=("Arial", 10, "bold")).pack(pady=5)
entry_output = tk.Text(root, height=5, width=50, bg="#f0f0f0")
entry_output.pack(pady=5)

root.mainloop()