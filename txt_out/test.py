import random
from datetime import datetime, timedelta
import customtkinter as ctk
from pathlib import Path
import os
from PIL import Image

root_dir = Path(__file__).resolve().parent
text_path = os.path.join(root_dir, "info.txt")
logo_path = os.path.join(root_dir, "logo.png")

class WatchHistory(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry("400x500")
        self.title("Watch History")
        self.resizable(False, False)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=400, height=500)
        self.scrollable_frame.pack()
        self.build_ui()

    def build_ui(self):
        self.logo_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.logo_frame.pack(pady=20)
        logo_image = Image.open(logo_path)
        self.real_logo = ctk.CTkImage(logo_image, size=(64, 64))
        self.logo_label = ctk.CTkLabel(self.logo_frame, image=self.real_logo, text="")
        self.logo_label.pack(side="left", padx=(0, 10))
        self.name_label = ctk.CTkLabel( self.logo_frame, text="etflix", text_color="white", font=("Inter", 25, "bold"))
        self.name_label.pack(side="left")

        self.create_history()
        self.create_txt()

    def create_history(self):
        self.receipt = []
        self.receipt.append("-" * 36)
        atime = datetime.now() - timedelta(days=67)

        for i in range(10):
            self.receipt.append(f"Watched movie {i + 1} at time {atime.strftime('%d/%m/%Y')}")
            atime += timedelta(days=random.randint(0, 30))
            self.receipt.append(f"A random dice roll: {random.randint(1, 6)}\n")

        self.receipt.append("ACCOUNT: MR DUNNE")
        self.receipt.append("-" * 36)
        receipt_display = ctk.CTkLabel(self.scrollable_frame, text="\n".join(self.receipt), font=("Courier New", 14), justify="left")
        receipt_display.pack(pady=10)

    def create_txt(self):
        bank_name = "            Netflix            \n"

        with open(text_path, "w", encoding="utf-8") as file:
            file.write(bank_name + "\n".join(self.receipt))

app = ctk.CTk()
watch_history = WatchHistory(app)
app.mainloop()