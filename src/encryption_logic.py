import os
import hashlib
import json
import sys

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class EmergencyDriveCrypto:
    def __init__(self, passkey: str):
        if len(passkey) != 16 or not passkey.isalnum():
            raise ValueError("Passkey must be a 16-character alphanumeric string.")
        self.key = hashlib.sha256(passkey.encode()).digest()  # Derive a 256-bit key from the passkey
        self.iv_store_path = self._get_iv_store_path()
        self.iv_store = {}
        self._load_iv_store()

    def _get_iv_store_path(self):
        """Return the path to the iv_index.json file located in the same directory as the executable or script."""
        if getattr(sys, 'frozen', False):  # Running as a PyInstaller executable
            app_dir = os.path.dirname(os.path.abspath(sys.executable))
            app_dir = os.path.abspath(os.path.join(app_dir, '../../../'))
            return os.path.join(app_dir, 'iv_index.json')
        else:  # Running as a script
            return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'iv_index.json')

    def _load_iv_store(self):
        """Load or initialize the IV store."""
        if os.path.exists(self.iv_store_path):
            with open(self.iv_store_path, 'r') as file:
                self.iv_store = json.load(file)
        else:
            self.iv_store = {}

    def _save_iv_store(self):
        """Save the IV store to disk."""
        with open(self.iv_store_path, 'w') as file:
            json.dump(self.iv_store, file, indent=4)

    def encrypt_file(self, file_path: str, output_path: str):
        # Read file content
        with open(file_path, 'rb') as file:
            plaintext = file.read()

        # Generate random IV
        iv = os.urandom(16)

        # Encrypt using AES-CBC
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

        # Write ciphertext to output file
        with open(output_path, 'wb') as file:
            file.write(ciphertext)

        # Save the IV to the IV store
        relative_path = os.path.relpath(output_path, os.getcwd())
        self.iv_store[relative_path] = iv.hex()
        self._save_iv_store()

    def decrypt_file(self, file_path: str, output_path: str):
        # Retrieve the IV from the IV store
        relative_path = os.path.relpath(file_path, os.getcwd())
        iv_hex = self.iv_store.get(relative_path)
        if not iv_hex:
            raise ValueError(f"IV not found for file: {file_path}")

        iv = bytes.fromhex(iv_hex)

        # Read ciphertext content
        with open(file_path, 'rb') as file:
            ciphertext = file.read()

        # Decrypt using AES-CBC
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

        # Write plaintext to output file
        with open(output_path, 'wb') as file:
            file.write(plaintext)

    def encrypt_folder(self, folder_path: str, output_folder: str):
        # Encrypt all files in the folder
        os.makedirs(output_folder, exist_ok=True)
        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, folder_path)
                output_path = os.path.join(output_folder, rel_path)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                self.encrypt_file(full_path, output_path)

    def decrypt_folder(self, folder_path: str, output_folder: str):
        # Decrypt all files in the folder
        os.makedirs(output_folder, exist_ok=True)
        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, folder_path)
                output_path = os.path.join(output_folder, rel_path)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                self.decrypt_file(full_path, output_path)

