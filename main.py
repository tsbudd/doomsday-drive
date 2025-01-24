import os
import tkinter as tk
from tkinter import filedialog, messagebox
from encryption_logic import EmergencyDriveCrypto


class EncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Doomsday Drive Encryption")

        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Window dimensions
        window_width = 500
        window_height = 300

        # Calculate position to center the window
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Set window geometry (widthxheight+X+Y)
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        # Validation for passkey (must be 16 characters long)
        self.passkey_var = tk.StringVar()
        self.passkey_var.trace_add("write", self.limit_passkey_length)

        # Passkey Entry
        self.passkey_label = tk.Label(root, text="Enter 16-Character Passkey:")
        self.passkey_label.pack(pady=5)

        # Frame for Entry and Toggle Button
        passkey_frame = tk.Frame(root)
        passkey_frame.pack(pady=5)

        # Passkey Entry
        self.passkey_entry = tk.Entry(passkey_frame, show="*", width=30, textvariable=self.passkey_var)
        self.passkey_entry.pack(side=tk.LEFT)

        # Toggle Visibility Button
        self.toggle_button = tk.Button(passkey_frame, text="Show", command=self.toggle_passkey_visibility)
        self.toggle_button.pack(side=tk.LEFT)

        # Padding Frame
        self.padding_frame = tk.Frame(root)
        self.padding_frame.pack(pady=20)

        # Folder Selection
        self.folder_path = tk.StringVar()
        self.folder_button = tk.Button(root, text="Select Folder", command=self.select_folder, state=tk.DISABLED)
        self.folder_button.pack(pady=5)
        self.folder_label = tk.Label(root, textvariable=self.folder_path)
        self.folder_label.pack(pady=5)

        # Encrypt Button
        self.encrypt_button = tk.Button(root, text="Encrypt", command=self.encrypt, state=tk.DISABLED)
        self.encrypt_button.pack(pady=10)

        # Decrypt Button
        self.decrypt_button = tk.Button(root, text="Decrypt", command=self.decrypt, state=tk.DISABLED)
        self.decrypt_button.pack(pady=5)

    def limit_passkey_length(self, *args):
        """Ensure passkey is limited to 16 characters"""
        value = self.passkey_var.get()
        if len(value) > 16:
            self.passkey_var.set(value[:16])  # Trim to 16 characters if too long
            value = value[:16]  # Trim to 16 characters if too long

        # Enable buttons if passkey is valid (16 characters long)
        if len(value) == 16:
            self.enable_buttons()
        else:
            self.disable_buttons()

    def enable_buttons(self):
        """Enable the action buttons when the passkey is 16 characters long"""
        self.folder_button.config(state=tk.NORMAL)

    def enable_encrypt(self):
        """Enable the action buttons when the passkey is 16 characters long"""
        self.encrypt_button.config(state=tk.NORMAL)
        self.decrypt_button.config(state=tk.DISABLED)

    def enable_decrypt(self):
        """Enable the action buttons when the passkey is 16 characters long"""
        self.encrypt_button.config(state=tk.DISABLED)
        self.decrypt_button.config(state=tk.NORMAL)

    def disable_buttons(self):
        """Disable the action buttons until the passkey is valid"""
        self.folder_button.config(state=tk.DISABLED)
        self.encrypt_button.config(state=tk.DISABLED)
        self.decrypt_button.config(state=tk.DISABLED)

    def toggle_passkey_visibility(self):
        """Toggle the visibility of the passkey"""
        if self.passkey_entry.cget("show") == "*":
            self.passkey_entry.config(show="")
            self.toggle_button.config(text="Hide")  # Change button text to 'Hide'
        else:
            self.passkey_entry.config(show="*")
            self.toggle_button.config(text="Show")  # Change button text to 'Show'

    def select_folder(self):
        project_root = os.getcwd()  # This gets the current working directory (project root)
        folder = filedialog.askdirectory(initialdir=project_root)
        if folder:
            self.folder_path.set(folder)
            if self.folder_path.get().endswith("_encrypted"):
                self.enable_decrypt()
            else:
                self.enable_encrypt()

    def encrypt(self):
        passkey = self.passkey_var.get()
        if len(passkey) != 16 or not passkey.isalnum():
            messagebox.showerror("Error", "Passkey must be 16 alphanumeric characters.")
            return

        crypto = EmergencyDriveCrypto(passkey)

        # Encrypt Folder
        if self.folder_path.get():
            output_folder = self.folder_path.get() + "_encrypted"
            try:
                crypto.encrypt_folder(self.folder_path.get(), output_folder)
                messagebox.showinfo("Success", f"Folder encrypted: {output_folder}\n\n"
                                               f"Make sure to delete the original folder!")
                self.root.quit()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "No file or folder selected.")

    def decrypt(self):
        passkey = self.passkey_var.get()
        if len(passkey) != 16 or not passkey.isalnum():
            messagebox.showerror("Error", "Passkey must be 16 alphanumeric characters.")
            return

        crypto = EmergencyDriveCrypto(passkey)

        # Decrypt Folder
        if self.folder_path.get() and self.folder_path.get().endswith("_encrypted"):
            output_folder = self.folder_path.get().replace("_encrypted", "")
            try:
                crypto.decrypt_folder(self.folder_path.get(), output_folder)
                messagebox.showinfo("Success", f"Folder decrypted: {output_folder}\n\n"
                                               f"Make sure to delete the decrypted folder when you are done")
                self.root.quit()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "No valid encrypted file or folder selected.")


# Main Execution
if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()
