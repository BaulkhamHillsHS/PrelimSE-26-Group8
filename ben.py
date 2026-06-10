import customtkinter as ctk
from PIL import Image as im
from PIL import ImageTk, ImageEnhance
import random
import math

def pos(x: int, y: int, x_offset: int = 0, y_offset: int = 0) -> str:
    return f"{x}x{y}+{x_offset-8}+{y_offset}"

# rounded rect canvas element
# def create_rrect(canvas: ctk.CTkCanvas, x1, y1, x2, y2, r, fill):
#     points = [
#         # corner 1
#         x1, y1 + r, x1, y1 + r,
#         x1, y1,
#         x1 + r, y1, x1 + r, y1,
        
#         # corner 2
#         x2 - r, y1, x2 - r, y1,
#         x2, y1,
#         x2, y1 + r, x2, y1 + r,
        
#         # corner 3
#         x2, y2 - r, x2, y2 - r,
#         x2, y2,
#         x2 - r, y2, x2 - r, y2,
        
#         # corner 4
#         x1 + r, y2, x1 + r, y2,
#         x1, y2,
#     ]
#     return canvas.create_polygon(points, smooth=True, fill=fill)

def create_rrect(canvas: ctk.CTkCanvas, width, height, pos, r, fill):
    x1, y1 = pos
    x2 = x1 + width
    y2 = y1 + height
    points = [
        # corner 1
        x1, y1 + r, x1, y1 + r,
        x1, y1,
        x1 + r, y1, x1 + r, y1,
        
        # corner 2
        x2 - r, y1, x2 - r, y1,
        x2, y1,
        x2, y1 + r, x2, y1 + r,
        
        # corner 3
        x2, y2 - r, x2, y2 - r,
        x2, y2,
        x2 - r, y2, x2 - r, y2,
        
        # corner 4
        x1 + r, y2, x1 + r, y2,
        x1, y2,
        x1, y2 - r, x1, y2 - r
    ]
    return canvas.create_polygon(points, smooth=True, fill=fill)



class Image():
    def __init__(self, canvas: ctk.CTkCanvas, image, pos, speed = 1):
        self.canvas = canvas
        self.id = self.canvas.create_image(*pos, image=image, anchor="nw")
        self.speed = speed
    
    def move(self, x, y):
        self.canvas.move(self.id, x, y)
    
    def goto(self, x, y):
        self.canvas.moveto(self.id, x, y)
    
    def slide(self):
        self.canvas.move(self.id, self.speed, 0)
    
    def get_pos(self):
        return self.canvas.tk.call(self.canvas._w, "coords", self.id)
    
    def get_size(self):
        bbox = self.canvas.bbox(self.id)
        x = bbox[2] - bbox[0]
        y = bbox[3] - bbox[1]
        return (x, y)
    
class Panel():
    def __init__(self, canvas: ctk.CTkCanvas, width, height, r, pos, fill, padding):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.pos = pos
        self.padding = padding
        create_rrect(canvas, width, height, pos, r, fill)
    
    def get_pos(self):
        return (self.pos[0] - 2, self.pos[1])
    
    def get_dim(self):
        return (self.width, self.height)
    
    def get_udim(self):
        return (self.width - self.padding[0] - self.padding[1], self.height - self.padding[2] - self.padding[3])

class Login(ctk.CTk):
    def __init__(
        self, 
        fg_color: tuple[str, str] | str = "white",
        geometry: str = pos(500, 400, 0, 0),
        title: str = "Untitled App",
        minsize: tuple[int, int] = None,
        maxsize: tuple[int, int] = None,
        resizable: tuple[bool, ...] = (True, True),
    ):
        super().__init__(fg_color)

        self.geometry(geometry)
        self.SCREEN_WIDTH = int(geometry.split("x")[0])
        self.SCREEN_HEIGHT = int(geometry.split("x")[1].split("+")[0])
        
        self.title(title)
        if minsize: self.minsize(*minsize)
        if maxsize: self.maxsize(*maxsize)
        self.resizable(*resizable)
        self.update()
        self.build_ui()
    def build_ui(self):
        self.images_count = 9
        self.row_count = 7
        
        pil_image = im.open("icon0.png")
        pil_image_dark = ImageEnhance.Brightness(im.open("icon0.png")).enhance(0.6)

        # ctk.FontManager.load_font("Poppins-Regular.ttf")
        
        main_font = ctk.CTkFont(family="Inter Regular", size=16)

        self.image_sizes = [(90, 90), (60, 60)]
        self.image = ImageTk.PhotoImage(pil_image.resize(self.image_sizes[0]))
        self.image_dark = ImageTk.PhotoImage(pil_image_dark.resize(self.image_sizes[1]))
        
        self.canvas = ctk.CTkCanvas(self, width=1280, height=720, bg="black")
        self.canvas.place(x=-2, y=0)
        # self.images = self.canvas.create_image(0, 0, image=self.photo, anchor="center")

        self.images = []
        for j in range(self.row_count):
            y_pos = self.SCREEN_HEIGHT / (self.row_count - 1) * j - self.image_sizes[j % 2][0] / 2
            x_offset = (j // 2) % 2 * self.SCREEN_WIDTH / self.images_count / 2
            # speed = random.randint(40, 100) / 50
            speed = (1 + j % 2) / 3
            for i in range(self.images_count + 1):
                # image = self.canvas.create_image(self.SCREEN_WIDTH / self.images_count * i - 60 + x_offset, y_pos, image=self.photo, anchor="nw")
                image = Image(self.canvas, self.image if j % 2 == 0 else self.image_dark, (self.SCREEN_WIDTH / self.images_count * i - self.image_sizes[j % 2][0] / 2 + x_offset, y_pos), speed)
                self.images.append(image)
        
        login_panel = Panel(self.canvas, (w:=400), (f := 0.85)*self.SCREEN_HEIGHT, 40, ((self.SCREEN_WIDTH - w) / 2, (1 - f)*self.SCREEN_HEIGHT / 2), "#36363B", (30, 30, 30, 30))
        
        # Content goes here
        title = im.open("netty.png")
        title_pad = 30
        
        self.asdf = ImageTk.PhotoImage(title.resize(((w_x:=login_panel.get_udim()[0] - 2 * title_pad), int(title.size[1] / title.size[0] * w_x))))
        self.netflix = self.canvas.create_image(login_panel.pos[0] + login_panel.padding[0] + title_pad, login_panel.pos[1] + login_panel.padding[2] + title_pad, image=self.asdf, anchor="nw")
        
        self.email_frame = ctk.CTkFrame(self, login_panel.get_udim()[0], 56, 10, bg_color="#36363B", fg_color="#4C4C53", border_width=2, border_color="#6F6F70")
        self.email_frame.place(x=login_panel.get_pos()[0] + login_panel.padding[0], y=self.canvas.bbox(self.netflix)[3] + 40)
        self.email_frame.rowconfigure(0, weight=1)
        self.email_frame.columnconfigure(1, weight=1)
        self.email_frame.grid_propagate(False)
        
        self.email = ctk.CTkEntry(self.email_frame, font=main_font, placeholder_text="Email or mobile number", border_width=0, fg_color="#4C4C53", text_color="#98989B")
        self.email.grid(row=0, column=1, sticky="nesw", pady=2, padx=(0, 15))
        self.person_icon = ctk.CTkLabel(self.email_frame, image=ctk.CTkImage(light_image=(p:=im.open("person.png")), size=p.size), text="")
        self.person_icon.grid(row=0, column=0, padx=(12, 10))
        
        self.password_frame = ctk.CTkFrame(self, login_panel.get_udim()[0], 56, 10, bg_color="#36363B", fg_color="#4C4C53", border_width=2, border_color="#6F6F70")
        self.password_frame.place(x=login_panel.get_pos()[0] + login_panel.padding[0], y=self.canvas.bbox(self.netflix)[3] + 40 + 56 + 24)
        self.password_frame.rowconfigure(0, weight=1)
        self.password_frame.columnconfigure(1, weight=1)
        self.password_frame.grid_propagate(False)
        
        self.password = ctk.CTkEntry(self.password_frame, font=main_font, placeholder_text="Password", border_width=0, fg_color="#4C4C53", show="•", text_color="#98989B")
        self.password.grid(row=0, column=1, sticky="nesw", pady=2, padx=(0, 15))
        self.lock_icon = ctk.CTkLabel(self.password_frame, image=ctk.CTkImage(light_image=(p:=im.open("lock.png")), size=p.size), text="")
        self.lock_icon.grid(row=0, column=0, padx=(12, 10))
        
        self.visibility = [im.open("eye.png"), im.open("blind.png")]
        self.hide = ctk.CTkButton(self.password_frame, width=0, height=40, text="", fg_color="#4C4C53", image=ctk.CTkImage(light_image=(p:=self.visibility[1]), size=p.size), command=lambda: self.toggle_show(self.password, self.hide), anchor="center", hover_color="#4C4C53")
        self.hide.grid(row=0, column=2, padx=(0, 5), pady=(3, 0))
        
        self.remember = ctk.CTkCheckBox(self, text_color="#AAAAAD", bg_color="#36363B", font=("Inter Regular", 14), text="Remember me", checkbox_height=16, border_width=2, fg_color="red", hover=False)
        self.remember.place(x=login_panel.get_pos()[0] + login_panel.padding[0] + 1, y=self.canvas.bbox(self.netflix)[3] + 40 + 56 + 24 + 56 + 12)
        
        self.forgot = ctk.CTkButton(self, width=140, text="Forgot password?", border_width=0, bg_color="#36363B", fg_color="#36363B", anchor="e", text_color="#AAAAAD", hover=False, font=("Inter Regular", 14))
        self.forgot.place(x=login_panel.get_pos()[0] + login_panel.get_dim()[0] - login_panel.padding[0] - 140, y=self.canvas.bbox(self.netflix)[3] + 40 + 56 + 24 + 56 + 12)
        
        button_width = 56
        self.login_button = ctk.CTkButton(self, login_panel.get_dim()[0] - login_panel.padding[0] - login_panel.padding[1], button_width, 10, bg_color="#36363B", fg_color="#d81f26", text="Login", font=("Inter Black", 20), text_color="white", hover_color="#b41f24")
        self.login_button.place(x=login_panel.get_pos()[0] + login_panel.padding[0], y=login_panel.get_pos()[1] + login_panel.get_dim()[1] - login_panel.padding[3] - button_width)
        
        self.animate()
    
    def animate(self):
        for x in self.images:
            x.slide()
            if x.get_pos()[0] >= self.SCREEN_WIDTH / self.images_count + self.SCREEN_WIDTH - x.get_size()[0]:
                x.goto(-x.get_size()[0], "")
        
        self.after(16, self.animate)
        
    def toggle_show(self, entry: ctk.CTkEntry, button: ctk.CTkButton):
        current = entry.cget("show")
        if current != "":
            entry.configure(show="")
            button.configure(image=ctk.CTkImage(light_image=(p:=self.visibility[1])))
        else:
            entry.configure(show="•")
            button.configure(image=ctk.CTkImage(light_image=(p:=self.visibility[0])))
        

if __name__ == "__main__":
    app = Login(fg_color="black", geometry=pos(1280, 720, 0, 0), title="Use this as the background of a login screen or something", resizable=(False, False))
    app.mainloop()