from tkinter import Canvas, Tk
from PIL import Image, ImageTk


class ImgAnimation:
    def __init__(self, root, imgPaths, duration=1000):
        self.root = root
        self.imgPaths = imgPaths
        self.duration = duration
        self.canvas = Canvas(root)
        self.canvas.pack()
        self.current_frame = 0
        self.images = [Image.open(path) for path in imgPaths]
        self.photo_images = [ImageTk.PhotoImage(
            image) for image in self.images]
        self.image_object = self.canvas.create_image(
            0, 0, anchor='nw', image=self.photo_images[self.current_frame])
        self.animate()

    def animate(self):
        self.canvas.itemconfig(
            self.image_object, image=self.photo_images[self.current_frame])
        self.current_frame = (self.current_frame + 1) % len(self.imgPaths)
        self.root.after(self.duration, self.animate)
