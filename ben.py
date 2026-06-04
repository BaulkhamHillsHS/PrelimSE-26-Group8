import customtkinter as ctk
from PIL import Image as im
from PIL import ImageTk
import random
import math

def pos(x: int, y: int, x_offset: int = 0, y_offset: int = 0) -> str:
    return f"{x}x{y}+{x_offset-8}+{y_offset}"

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
        return self.canvas.bbox(self.id)
    

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
        pil_image_dark = im.open("icon1.png") 

        self.image_sizes = [(80, 80), (60, 60)]
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
        
        # Content goes here
        button = ctk.CTkButton(self)
        button.place(x=640, y=360)
        
        self.animate()
    
    def animate(self):
        for x in self.images:
            x.slide()
            if x.get_pos()[0] >= self.SCREEN_WIDTH / self.images_count + self.SCREEN_WIDTH - 60:
                x.goto(-60, "")
        
        self.after(16, self.animate)
        

if __name__ == "__main__":
    app = Login(fg_color="black", geometry=pos(1280, 720, 0, 0), title="Use this as the background of a login screen or something")
    app.mainloop()