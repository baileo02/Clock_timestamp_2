import tkinter as tk

class FrameTemplate:

    def __init__(self, parent_frame, text):
        self.text = text
        self.parent_frame = parent_frame

        label = tk.Label(self.parent_frame, text=self.text)
        label.grid()

class MessageWindow(tk.Toplevel):

    def __init__(self, title, message, **kw):
        super().__init__(**kw)
        self.details_expanded = False
        self.title(title)
        self.geometry("200x50+{}+{}".format(self.master.winfo_x(), self.master.winfo_y()))
        self.resizable(False, False)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        tk.Label(self, text=message).grid(row=0, column=0, columnspan=3, pady=(7, 7), padx=(7, 7), sticky="ew")
        tk.Button(self, text="OK", command=self.destroy).grid(row=1, column=1, sticky="e")
