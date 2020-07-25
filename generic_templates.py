import tkinter as tk

class FrameTemplate:

    def __init__(self, parent_frame, text):
        self.text = text
        self.parent_frame = parent_frame

        label = tk.Label(self.parent_frame, text=self.text)
        label.grid()
