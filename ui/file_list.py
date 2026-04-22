import tkinter as tk
from typing import Any, Tuple, cast, Callable
from core.file_service import FileService
from core.file_watcher import FileWatcher

class FileList(tk.Frame):

    def __init__(
            self, 
            file_service: FileService,
            master: tk.Misc | None = None, 
            on_select: Callable[[str], None] | None = None,
            **kwargs: Any
        ) -> None:
        super().__init__(master, **kwargs)
        self.on_select = on_select
        self.listbox = tk.Listbox(self, selectmode='browse')
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind("<<ListboxSelect>>", self._on_item_selected)

        self.file_service = file_service
        self.file_watcher = FileWatcher(str(self.file_service.root), on_change=self.trigger_list_refresh)

    def _on_item_selected(self, event: tk.Event) -> None:
        selection = cast(Tuple[int, ...], self.listbox.curselection()) # type: ignore
    
        if selection:
            index = selection[0]
            filename = cast(str, self.listbox.get(index)) # type: ignore
            if self.on_select:
                self.on_select(self.file_service.get_full_path(filename))
    
    def refresh_list(self) -> None:
        self.listbox.delete(0, tk.END)
        for filename in self.file_service.get_files():
            self.listbox.insert(tk.END, filename)
    
    def trigger_list_refresh(self) -> None:
        self.after(0, self.refresh_list)
