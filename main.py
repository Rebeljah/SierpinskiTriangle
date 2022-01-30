import tkinter as tk
from tkinter import ttk
from PIL import ImageTk

from render import render_sierpinski


ROOT = None


class DisplayPanel(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self._image = None
        self.image_render = ttk.Label(self)

        self.image_render.pack()

    def render_image(self, to_depth):
        image = render_sierpinski(1000, to_depth)
        self._image = ImageTk.PhotoImage(image)
        self.image_render.config(image=self._image)


class ControlPanel(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.depth_slider = self.DepthSlider(self)
        self.depth_slider.pack()

    class DepthSlider(ttk.Scale):
        def __init__(self, master):
            super().__init__(
                master, from_=0, to=100, orient='vertical',
                command=self._set_depth
            )

            self.scale_step = 100 / ROOT.max_render_depth
            self.depth = 0

        def _set_depth(self, event):
            """If the depth level changes, re-render the triangle"""
            slider_depth = self.get() / self.scale_step
            if slider_depth != self.depth:
                self.depth = slider_depth
                ROOT.render(self.depth)


class UIRoot(tk.Tk):
    def __init__(self):
        super().__init__()
        global ROOT
        ROOT = self
        self.title("Sierpinski's Triangle")
        self.max_render_depth = 6

        self.content = ttk.Frame(self)

        self.display = DisplayPanel(self.content)
        self.display.pack(side=tk.LEFT)

        self.controls = ControlPanel(self.content)
        self.controls.pack(side=tk.RIGHT)

        self.content.pack(expand=True, fill=tk.BOTH)

        self.render(0)

    def render(self, depth):
        self.display.render_image(to_depth=depth)


if __name__ == '__main__':
    ui_root = UIRoot()
    ui_root.mainloop()
