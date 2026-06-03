import customtkinter as ctk
from PIL import Image as im
import random

def pos(x: int, y: int, x_offset: int = 0, y_offset: int = 0) -> str:
    return f"{x}x{y}+{x_offset-8}+{y_offset}"

class Image():
    def __init__(self, app, path, size, pos = None, speed = 1):
        pil_image = im.open(path)
        self.label = ctk.CTkLabel(app, text="", image=ctk.CTkImage(light_image=pil_image, size=size))
        self.size = size
        self.pos = pos
        if pos: self.update_pos()
        self.speed = speed
    
    def update_pos(self):
        self.label.place(x=self.pos[0], y=self.pos[1])
    
    def move(self, x, y):
        self.pos[0] += x
        self.pos[1] += y
        self.update_pos()
    
    def goto(self, x = None, y = None):
        if x: self.pos[0] = x
        if y: self.pos[1] = y
        self.update_pos()
    

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
        self.row_count = 5
        
        self.images = []
        for j in range(self.row_count):
            y_pos = self.SCREEN_HEIGHT / (self.row_count - 1) * j - 30
            x_offset = (j % 2) * self.SCREEN_WIDTH / self.images_count / 2
            speed = random.randint(1, 100) / 20
            for i in range(self.images_count + 1):
                image = Image(self, "icon.png", (60, 60), None, speed)
                image.pos = [self.SCREEN_WIDTH / self.images_count * i - image.size[0] + x_offset, y_pos]
                self.images.append(image)
        
        button = ctk.CTkButton(self)
        button.place(x=640, y=360)
        
        self.animate_label()
    
    def animate_label(self):
        for x in self.images:
            x.move(x.speed, 0)
            
            if x.pos[0] >= self.SCREEN_WIDTH / self.images_count + self.SCREEN_WIDTH - x.size[0]:
                x.goto(-x.size[0])
        
        self.after(1, self.animate_label)
        

if __name__ == "__main__":
    app = Login(fg_color="black", geometry=pos(1280, 720, 0, 0))
    app.mainloop()