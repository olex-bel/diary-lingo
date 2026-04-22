
import tkinter as tk
from typing import Any

class TextView(tk.Text):
    
    def __init__(self, master: tk.Misc | None = None, **kwargs: Any) -> None:
        super().__init__(master, **kwargs)

        self.scrollbar = tk.Scrollbar(self.master)
        self.configure(wrap='word', font='AppMainFont', yscrollcommand=self.scrollbar.set)
        self.tag_configure("indented", lmargin1=5, lmargin2=5, rmargin=5)
        self.scrollbar.config(command=self.yview) # type: ignore
        self.scrollbar.pack(side='right', fill='y')
        self.config(state=tk.DISABLED)

    def append_text(self, content: str) -> None:
        self.config(state=tk.NORMAL)
        self.insert('end', content, 'indented')
        self.config(state=tk.DISABLED)
    
    def clear_text(self) -> None:
        self.config(state=tk.NORMAL)
        self.delete('1.0', 'end')
        self.config(state=tk.DISABLED)