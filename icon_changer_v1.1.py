# Created by Bibhuti (Facebook.com/bibhutithecoolboy) If you find it useful, please consider donating something.
# Contact me on Facebook to get the donation details.
# If you need any custom tools, feel free to contact me.

# A simple GUI application to change folder icons on Windows.
# Supports drag and drop for folder and icon selection.

import tkinter as tk
from tkinter import filedialog, ttk, messagebox, Toplevel
from tkinterdnd2 import DND_FILES, TkinterDnD
import shutil
import os
import subprocess
import webbrowser
from PIL import Image, ImageTk
import sys

class FolderIconChanger:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Icon Changer")
        self.root.configure(bg="#f0f2f5")
        self.root.resizable(True, True)
        
        # Set window icon
        try:
            self.root.iconbitmap("app_icon.ico")
        except:
            pass
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 10), padding=5)
        self.style.map("TButton", background=[("active", "#e0e0e0")])
        self.style.configure("TLabel", font=("Arial", 10), background="#f0f2f5")
        
        # Create main container
        self.main_frame = tk.Frame(root, bg="#f0f2f5", padx=15, pady=15)
        self.main_frame.pack(fill="both", expand=True)
        
        # Header
        tk.Label(
            self.main_frame,
            text="Folder Icon Changer",
            font=("Arial", 14, "bold"),
            bg="#f0f2f5",
            fg="#333333"
        ).grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Folder selection
        tk.Label(
            self.main_frame,
            text="Select Folder or Drag and Drop:",
            font=("Arial", 9),
            bg="#f0f2f5"
        ).grid(row=1, column=0, sticky="w", pady=2)
        self.entry_folder = tk.Entry(self.main_frame, width=35, font=("Arial", 9))
        self.entry_folder.grid(row=2, column=0, columnspan=2, sticky="ew", padx=(0, 5))
        self.entry_folder.drop_target_register(DND_FILES)
        self.entry_folder.dnd_bind('<<Drop>>', self.drop_folder)
        ttk.Button(
            self.main_frame,
            text="Browse",
            command=self.select_folder
        ).grid(row=2, column=2, sticky="w")
        
        # Folder drag-and-drop area
        self.folder_drop = tk.Label(
            self.main_frame,
            text="Drop Folder Here",
            font=("Arial", 9, "italic"),
            bg="#e6f3ff",
            bd=2,
            relief="groove",
            height=1,
            width=35
        )
        self.folder_drop.grid(row=3, column=0, columnspan=2, pady=2, padx=(0, 5))
        self.folder_drop.drop_target_register(DND_FILES)
        self.folder_drop.dnd_bind('<<Drop>>', self.drop_folder)
        
        # Icon selection
        tk.Label(
            self.main_frame,
            text="Select Icon (.ico) or Drag and Drop:",
            font=("Arial", 9),
            bg="#f0f2f5"
        ).grid(row=4, column=0, sticky="w", pady=2)
        self.entry_icon = tk.Entry(self.main_frame, width=35, font=("Arial", 9))
        self.entry_icon.grid(row=5, column=0, columnspan=2, sticky="ew", padx=(0, 5))
        self.entry_icon.drop_target_register(DND_FILES)
        self.entry_icon.dnd_bind('<<Drop>>', self.drop_icon)
        ttk.Button(
            self.main_frame,
            text="Browse",
            command=self.select_icon
        ).grid(row=5, column=2, sticky="w")
        
        # Icon drag-and-drop area
        self.icon_drop = tk.Label(
            self.main_frame,
            text="Drop .ico File Here",
            font=("Arial", 9, "italic"),
            bg="#e6f3ff",
            bd=2,
            relief="groove",
            height=1,
            width=35
        )
        self.icon_drop.grid(row=6, column=0, columnspan=2, pady=2, padx=(0, 5))
        self.icon_drop.drop_target_register(DND_FILES)
        self.icon_drop.dnd_bind('<<Drop>>', self.drop_icon)
        
        # Buttons frame for Change Icon and Clear Icon
        self.buttons_frame = tk.Frame(self.main_frame, bg="#f0f2f5")
        self.buttons_frame.grid(row=7, column=0, columnspan=3, pady=10)
        
        # Change Icon button
        ttk.Button(
            self.buttons_frame,
            text="Change Icon",
            command=self.submit
        ).pack(side="left", padx=5)
        
        # Clear Icon button
        ttk.Button(
            self.buttons_frame,
            text="Clear Icon",
            command=self.clear_icon
        ).pack(side="left", padx=5)
        
        # Result label
        self.result_label = tk.Label(
            self.main_frame,
            text="",
            font=("Arial", 9),
            bg="#f0f2f5",
            fg="#333333"
        )
        self.result_label.grid(row=8, column=0, columnspan=3, pady=2)
        
        # Credits frame
        self.credits_frame = tk.Frame(self.main_frame, bg="#ffffff", bd=1, relief="solid", padx=8, pady=5)
        self.credits_frame.grid(row=9, column=0, columnspan=3, pady=10, sticky="ew")
        
        tk.Label(
            self.credits_frame,
            text="Created by Bibhuti",
            font=("Arial", 9, "bold"),
            bg="#ffffff"
        ).pack(pady=1)
        fb_link = tk.Label(
            self.credits_frame,
            text="Facebook.com/bibhutithecoolboy",
            font=("Arial", 9),
            fg="#0066cc",
            bg="#ffffff",
            cursor="hand2"
        )
        fb_link.pack(pady=1)
        fb_link.bind("<Button-1>", lambda e: self.open_facebook())
        tk.Label(
            self.credits_frame,
            text="If you find this tool useful, please consider donating.",
            font=("Arial", 9),
            bg="#ffffff"
        ).pack(pady=1)
        tk.Label(
            self.credits_frame,
            text="If you need any custom tools, contact me via Facebook.",
            font=("Arial", 9),
            bg="#ffffff"
        ).pack(pady=1)
        
        # Donate Now button
        ttk.Button(
            self.credits_frame,
            text="Donate Now",
            command=self.show_qr_code
        ).pack(pady=5)
        
        # Configure grid weights
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(2, weight=0)
        
        # Center the main window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def select_folder(self):
        folder = filedialog.askdirectory(title="Select Folder")
        if folder:
            self.entry_folder.delete(0, tk.END)
            self.entry_folder.insert(0, folder)
    
    def select_icon(self):
        icon = filedialog.askopenfilename(title="Select Icon", filetypes=[("Icon files", "*.ico")])
        if icon:
            self.entry_icon.delete(0, tk.END)
            self.entry_icon.insert(0, icon)
    
    def submit(self):
        folder = self.entry_folder.get().strip()
        icon_path = self.entry_icon.get().strip()
        
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid folder!")
            return
        if not icon_path or not os.path.isfile(icon_path) or not icon_path.lower().endswith('.ico'):
            messagebox.showerror("Error", "Please select a valid .ico file!")
            return
        
        try:
            # Paths for desktop.ini and Icon.ico
            ini_path = os.path.join(folder, 'desktop.ini')
            dest_icon = os.path.join(folder, 'Icon.ico')
            
            # Remove existing desktop.ini and Icon.ico if they exist
            for file_path in [ini_path, dest_icon]:
                if os.path.exists(file_path):
                    try:
                        # Clear system and hidden attributes
                        subprocess.call(['attrib', '-S', '-H', file_path])
                        # Delete the file
                        os.remove(file_path)
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to remove existing file {file_path}: {str(e)}")
                        return
            
            # Copy new icon to folder
            shutil.copy(icon_path, dest_icon)
            
            # Create new desktop.ini
            with open(ini_path, 'w') as f:
                f.write('[.ShellClassInfo]\nIconResource=Icon.ico,0\n')
            
            # Set attributes to hide as system files
            subprocess.call(['attrib', '+S', '+H', ini_path])
            subprocess.call(['attrib', '+S', '+H', dest_icon])
            
            # Set folder to ReadOnly
            subprocess.call(['attrib', '+R', folder])
            
            self.result_label.config(text="Success! Refresh the folder (F5) to see the icon.", fg="#008800")
            messagebox.showinfo("Success", "Icon applied successfully! Press F5 to refresh the folder.")
        except Exception as e:
            self.result_label.config(text=f"Error: {str(e)}", fg="#cc0000")
            messagebox.showerror("Error", f"Failed to apply icon: {str(e)}")
    
    def clear_icon(self):
        folder = self.entry_folder.get().strip()
        
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid folder!")
            return
        
        try:
            # Paths for desktop.ini and Icon.ico
            ini_path = os.path.join(folder, 'desktop.ini')
            dest_icon = os.path.join(folder, 'Icon.ico')
            
            # Remove existing desktop.ini and Icon.ico if they exist
            for file_path in [ini_path, dest_icon]:
                if os.path.exists(file_path):
                    try:
                        # Clear system and hidden attributes
                        subprocess.call(['attrib', '-S', '-H', file_path])
                        # Delete the file
                        os.remove(file_path)
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to remove {file_path}: {str(e)}")
                        return
            
            # Clear folder's ReadOnly attribute
            subprocess.call(['attrib', '-R', folder])
            
            self.result_label.config(text="Success! Icon cleared. Refresh the folder (F5).", fg="#008800")
            messagebox.showinfo("Success", "Icon cleared successfully! Press F5 to refresh the folder.")
        except Exception as e:
            self.result_label.config(text=f"Error: {str(e)}", fg="#cc0000")
            messagebox.showerror("Error", f"Failed to clear icon: {str(e)}")
    
    def drop_folder(self, event):
        data = event.data.strip('{}')
        if os.path.isdir(data):
            self.entry_folder.delete(0, tk.END)
            self.entry_folder.insert(0, data)
    
    def drop_icon(self, event):
        data = event.data.strip('{}')
        if os.path.isfile(data) and data.lower().endswith('.ico'):
            self.entry_icon.delete(0, tk.END)
            self.entry_icon.insert(0, data)
    
    def open_facebook(self):
        webbrowser.open("https://facebook.com/bibhutithecoolboy")
    
    def show_qr_code(self):
        try:
            # Load QR code image
            if hasattr(sys, '_MEIPASS'):
                qr_path = os.path.join(sys._MEIPASS, 'payment_qr_code.png')
            else:
                qr_path = os.path.join(os.path.dirname(__file__), 'payment_qr_code.png')
            
            if not os.path.exists(qr_path):
                raise FileNotFoundError("QR code image not found at: " + qr_path)
            
            qr_image = Image.open(qr_path)
            qr_photo = ImageTk.PhotoImage(qr_image)
            
            # Create QR code window
            qr_window = Toplevel(self.root)
            qr_window.title("Donate via QR Code")
            qr_window.resizable(False, False)
            qr_window.configure(bg="#f0f2f5")
            
            # QR code label
            qr_label = tk.Label(qr_window, image=qr_photo, bg="#f0f2f5")
            qr_label.image = qr_photo
            qr_label.pack(pady=10)
            
            # Close button
            ttk.Button(
                qr_window,
                text="Close",
                command=qr_window.destroy
            ).pack(pady=10)
            
            # Center QR window
            qr_window.update_idletasks()
            width = qr_image.width + 20
            height = qr_image.height + 80
            screen_width = qr_window.winfo_screenwidth()
            screen_height = qr_window.winfo_screenheight()
            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)
            qr_window.geometry(f"{width}x{height}+{x}+{y}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load QR code image: {str(e)}\n\nPlease ensure 'payment_qr_code.png' is in the same folder as the script or EXE.")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = FolderIconChanger(root)
    root.mainloop()