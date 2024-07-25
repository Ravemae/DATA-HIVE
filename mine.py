import tkinter as tk
from tkinter import messagebox
import requests
import customtkinter as ctk

# URL of your FastAPI server
BASE_URL = "http://localhost:8000"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter FastAPI Integration")

        self.token = None
        
       
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

       
        self.frame = ctk.CTkFrame(root)
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(self.frame, text="Username").pack(pady=10)
        self.username = ctk.CTkEntry(self.frame)
        self.username.pack(pady=10)

        ctk.CTkLabel(self.frame, text="Password").pack(pady=10)
        self.password = ctk.CTkEntry(self.frame, show="*")
        self.password.pack(pady=10)

        self.login_button = ctk.CTkButton(self.frame, text="Login", command=self.login)
        self.login_button.pack(pady=20)

        self.protected_button = ctk.CTkButton(self.frame, text="Get Protected Content", command=self.get_protected_content)
        self.protected_button.pack(pady=20)

    def login(self):
        username = self.username.get()
        password = self.password.get()

        response = requests.post(f"{BASE_URL}/token", data={"username": username, "password": password})
        
        if response.status_code == 200:
            self.token = response.json().get("access_token")
            messagebox.showinfo("Success", "Login successful")
        else:
            messagebox.showerror("Error", "Login failed")

    def get_protected_content(self):
        if not self.token:
            messagebox.showerror("Error", "You need to login first")
            return
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{BASE_URL}/user/details", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            data_content = data['full_name']
            messagebox.showinfo("Protected Content", data_content)
        else:
            messagebox.showerror("Error", "Failed to retrieve protected content")

if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()
