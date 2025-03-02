import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import random
import string

class PasswordManager:
    """class to manage password storage and generation"""

    def __init__(self):
        """Launch PasswordManager dictionary to store passwords"""
        self.passwords = {}


    def add_password(self, website, username, password):
        """
        Add a new password to the passwordmanager.
            website (str): website for which the password is being stored
            username (str): username
            password (str): password 
            str: A confirmation message"""
        
        if website not in self.passwords:
            self.passwords[website] = {}
        self.passwords[website][username] = password
        return f"Password added for {username} on {website}"
    

    def generate_password(self, length=12):
        """
        Generate a random password.

            length (int): The length of the password to generate (default: 12).

            A randomly generated password.
        """
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))


    def get_all_passwords(self):
        """
        Displays all passwords in the manager.
        """
        return self.passwords

class PasswordManagerGUI:
    """
    Class to create and manage the GUI for the password manager.
    """

    def __init__(self, master):
        """
        Launches the GUI.
        """

        self.master = master
        self.pm = PasswordManager()
        master.title("Password Manager")

        # Create and place widgets
        tk.Label(master, text="Website:").grid(row=2, column=0, sticky="e")
        tk.Label(master, text="Username:").grid(row=4, column=0, sticky="e")
        tk.Label(master, text="Password:").grid(row=6, column=0, sticky="e")

        self.website_entry = tk.Entry(master)
        self.username_entry = tk.Entry(master)
        self.password_entry = tk.Entry(master, show="*")

        self.website_entry.grid(row=2, column=1)
        self.username_entry.grid(row=4, column=1)
        self.password_entry.grid(row=6, column=1)

        tk.Button(master, text="Add Password", command=self.add_password).grid(row=8, column=0, columnspan=2)
        tk.Button(master, text="Generate Password", command=self.generate_password).grid(row=10, column=0, columnspan=2)
        tk.Button(master, text="Display All Passwords", command=self.display_passwords).grid(row=12, column=0, columnspan=2)

    def add_password(self):
        """
        Add a new password to the manager using the input from the GUI.
        """
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        if website and username and password:
            result = self.pm.add_password(website, username, password)
            messagebox.showinfo("Success", result)
        else:
            messagebox.showerror("Error", "Please fill in all fields")


    def generate_password(self):
        """
        Generate a random password and display it in the password entry field.
        """
        length = simpledialog.askinteger("Password Length", "Enter password length:", minvalue=4, maxvalue=50)
        if length:
            password = self.pm.generate_password(length)
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, password)

    def display_passwords(self):
        """
        Display all stored passwords in a new window.
        """
        passwords = self.pm.get_all_passwords()
        if not passwords:
            messagebox.showinfo("No Passwords", "No passwords stored yet.")
            return

        # Create a new window to display passwords
        password_window = tk.Toplevel(self.master)
        password_window.title("Stored Passwords")

        # Create a treeview to display passwords in a table format
        tree = ttk.Treeview(password_window, columns=("Website", "Username", "Password"), show="headings")
        tree.heading("Website", text="Website")
        tree.heading("Username", text="Username")
        tree.heading("Password", text="Password")

        # Insert passwords into the treeview
        for website, users in passwords.items():
            for username, password in users.items():
                tree.insert("", "end", values=(website, username, password))

        tree.pack(expand=True, fill="both")

def main():
    """
    Main function to run the password manager application.
    """
    root = tk.Tk()
    PasswordManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

