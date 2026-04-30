
from typing import Any, Literal, Callable
import tkinter as tk
from tkinter import scrolledtext, messagebox

class TextEditor(tk.Frame):

    current_file: str|None = None
    last_saved_content: str = ""

    def __init__(self, master: tk.Misc | None = None, **kwargs: Any):
        super().__init__(master, **kwargs)
        self.text_widget = scrolledtext.ScrolledText(self, wrap=tk.WORD, undo=True, maxundo=-1)
        self.text_widget.pack(expand=True, fill='both')
        self.text_widget.bind("<Control-z>", lambda event: self.undo())
        self.text_widget.bind("<Control-y>", lambda event: self.redo())
        self.text_widget.bind("<Control-x>", lambda event: self.cut())
        self.text_widget.bind("<Control-c>", lambda event: self.copy())
        self.text_widget.bind("<Control-v>", lambda event: self.paste())
        self.text_widget.bind("<Control-a>", lambda event: self.select_all())
    
    def get_content(self) -> str:
        return self.text_widget.get(1.0, "end-1c")

    def set_content(self, content: str) -> None:
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, content)

    def has_unsaved_changes(self) -> bool:
        return self.last_saved_content != self.get_content()

    def clear_unsaved_changes(self) -> None:
        self.last_saved_content = self.get_content()

    def set_current_file(self, file_path: str|None) -> None:
        self.current_file = file_path
    
    def undo(self):
        self.text_widget.event_generate("<<Undo>>")
        return "break"

    def redo(self):
        self.text_widget.event_generate("<<Redo>>")
        return "break"

    def cut(self):
        self.text_widget.event_generate("<<Cut>>")
        return "break"

    def copy(self):
        self.text_widget.event_generate("<<Copy>>")
        return "break"

    def paste(self):
        try:
            if self.text_widget.tag_ranges(tk.SEL):
                self.text_widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
            
            self.text_widget.event_generate("<<Paste>>")
        except tk.TclError:
            pass
        return "break"

    def select_all(self):
        self.text_widget.tag_add(tk.SEL, 1.0, tk.END)
        self.text_widget.mark_set(tk.INSERT, tk.END)
        self.text_widget.see(tk.INSERT)
        return "break"

    def set_state(self, state: Literal["normal", "disabled"]) -> None:
        self.text_widget.config(state=state)

    def new_file(self):
        if self.has_unsaved_changes():
            result = messagebox.askyesnocancel("Unsaved Changes", "Changes to the current file will be lost if you create a new file. Create new file anyway?")
            if result is not True:
                return  # user cancelled or pressed no
        self.set_content("")
        self.set_current_file(None)

    def open_file(self, file_path: str):
        if self.has_unsaved_changes():
            result = messagebox.askyesnocancel("Unsaved Changes", "Changes to the current file will be lost if you open a new file. Open new file anyway?")
            if result is not True:
                return
        
        with open(file_path, "r") as file:
            content = file.read()
            self.set_content(content)
            self.set_current_file(file_path)
            self.last_saved_content = content

    def close_file(self):
        if self.has_unsaved_changes():
            result = messagebox.askyesnocancel("Unsaved Changes", "Changes to the current file will be lost if you close it. Close anyway?")
            if result is not True:
                return
        if self.current_file is None:
            self.set_content("")
            self.set_current_file(None)

    def save_file(self, on_save_as: Callable[[], str] | None = None):
        if self.current_file is None:
            if on_save_as and callable(on_save_as):
                new_path = on_save_as()
                if not new_path:
                    return
                self.set_current_file(new_path)

        if self.current_file is None:
            messagebox.showerror("Error Saving File", "No file path specified for saving.")
            return
        
        try:
            with open(self.current_file, "w") as file:
                content = self.text_widget.get(1.0, tk.END)
                file.write(content)
            self.clear_unsaved_changes()
        except Exception as e:
            messagebox.showerror("Error Saving File", f"An error occurred while saving the file: {e}")
