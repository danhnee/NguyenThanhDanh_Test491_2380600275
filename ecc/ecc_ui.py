import tkinter as tk
from tkinter import messagebox
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64

# ====== ECC Key Generation ======
private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

# ====== Encrypt ======
def encrypt_message():
    try:
        message = input_text.get("1.0", tk.END).strip().encode()

        # Generate ephemeral key
        ephemeral_private = ec.generate_private_key(ec.SECP256R1())
        shared_key = ephemeral_private.exchange(ec.ECDH(), public_key)

        # Derive AES key
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
        ).derive(shared_key)

        iv = os.urandom(12)
        cipher = Cipher(algorithms.AES(derived_key), modes.GCM(iv))
        encryptor = cipher.encryptor()

        ciphertext = encryptor.update(message) + encryptor.finalize()

        result = base64.b64encode(
            ephemeral_private.public_key().public_bytes(
                serialization.Encoding.X962,
                serialization.PublicFormat.UncompressedPoint
            ) + iv + encryptor.tag + ciphertext
        )

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result.decode())

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ====== Decrypt ======
def decrypt_message():
    try:
        data = base64.b64decode(input_text.get("1.0", tk.END).strip())

        # Extract parts
        pub_len = 65
        ephemeral_pub_bytes = data[:pub_len]
        iv = data[pub_len:pub_len+12]
        tag = data[pub_len+12:pub_len+28]
        ciphertext = data[pub_len+28:]

        ephemeral_public = ec.EllipticCurvePublicKey.from_encoded_point(
            ec.SECP256R1(), ephemeral_pub_bytes
        )

        shared_key = private_key.exchange(ec.ECDH(), ephemeral_public)

        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
        ).derive(shared_key)

        cipher = Cipher(algorithms.AES(derived_key), modes.GCM(iv, tag))
        decryptor = cipher.decryptor()

        plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, plaintext.decode())

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ====== UI ======
root = tk.Tk()
root.title("ECC Encryption Tool")
root.geometry("600x500")

title = tk.Label(root, text="ECC Encrypt / Decrypt", font=("Arial", 16))
title.pack(pady=10)

input_label = tk.Label(root, text="Input:")
input_label.pack()

input_text = tk.Text(root, height=8)
input_text.pack(padx=10, pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

encrypt_btn = tk.Button(btn_frame, text="Encrypt", command=encrypt_message)
encrypt_btn.grid(row=0, column=0, padx=10)

decrypt_btn = tk.Button(btn_frame, text="Decrypt", command=decrypt_message)
decrypt_btn.grid(row=0, column=1, padx=10)

output_label = tk.Label(root, text="Output:")
output_label.pack()

output_text = tk.Text(root, height=8)
output_text.pack(padx=10, pady=5)

root.mainloop()