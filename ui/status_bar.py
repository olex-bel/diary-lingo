import tkinter as tk
from typing import Any

class StatusBar(tk.Frame):
    def __init__(self, master: tk.Misc | None = None, **kwargs: Any) -> None:
        super().__init__(master, **kwargs)
        self.label = tk.Label(self, height=1, font='AppUIFont', justify=tk.LEFT, anchor='w')
        self.label.pack(fill=tk.BOTH, expand=True)

    def set_status(self, status: str) -> None:
        self.label.config(text=status)