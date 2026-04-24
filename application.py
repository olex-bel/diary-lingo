import tkinter as tk
from tkinter import font
from typing import Any
from queue import Queue, Empty
from text import TextProcessor, Message, MessageType, create_text_analyzer, create_text_translator
from ui import TextView, StatusBar, TextEditor, FileList
from core.file_service import FileService

POLLING_INTERVAL_MS = 100

class Application(tk.Tk):
    
    def __init__(self, config: dict[str, Any], screenName: str | None = None, **kwargs: Any) -> None:
        super().__init__(screenName=screenName, **kwargs)
        self.configuration = config
        font.Font(name='AppMainFont', family=config['app']['font_family'], size=config['app']['font_size_main'])
        font.Font(name='AppUIFont', family=config['app']['font_family'], size=config['app']['font_size_ui'])
        self.file_service = FileService(config['data']["entries_path"])
        self._configure_window()
        self._setup_ui()
        self.message_queue: Queue[Message] = Queue()
        self.analyzer = create_text_analyzer(self.message_queue, config=config["llm"])
        self.translator = create_text_translator(self.message_queue, config=config["translator"])
 
        
    def _configure_window(self) -> None:
        self.geometry(self.configuration["app"]["window_geometry"])
        self.title('Diary Lingo')
    
    def _create_main_panes(self, parent: tk.Misc | None = None) -> tk.PanedWindow:
        main_paned = tk.PanedWindow(parent, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=4)

        file_frame = tk.Frame(main_paned, width=200)
        file_label = tk.Label(file_frame, text="Entries", bg="lightgrey")
        file_label.pack(fill=tk.X)
    
        self.file_list = FileList(
            self.file_service,
            file_frame, 
            on_select=self.on_file_selected
        )
        self.file_list.pack(fill=tk.BOTH, expand=True)

        editor_frame = tk.Frame(main_paned)
        self.editor = TextEditor(editor_frame)
        self.editor.pack(fill=tk.BOTH, expand=True)

        main_paned.add(file_frame, stretch="never")  # type: ignore
        main_paned.add(editor_frame, stretch="always")  # type: ignore
        return main_paned

    def _create_menu(self) -> None:
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.editor.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Save", command=self.on_file_saved, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Close", command=self.editor.close_file, accelerator="Ctrl+W")

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.editor.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.editor.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.editor.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.editor.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.editor.paste, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.editor.select_all, accelerator="Ctrl+A")

        llm_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Actions", menu=llm_menu)
        llm_menu.add_command(label="Analyze", command=self.on_analyze_click, accelerator="Ctrl+Enter")
        llm_menu.add_command(label="Translate", command=self.on_translate_click, accelerator="Ctrl+T")

    def _setup_ui(self) -> None:
        self.status_bar = StatusBar(self, padx=10)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.BOTH)

        vertical_pane = tk.PanedWindow(self, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=4)
        vertical_pane.pack(fill=tk.BOTH, expand=True)

        main_paned = self._create_main_panes(vertical_pane)
        self.viewer = TextView(vertical_pane)
        vertical_pane.add(main_paned, stretch="always") # type: ignore
        vertical_pane.add(self.viewer, stretch="never", height=150) # type: ignore

        self._create_menu()

    def _set_input_state(self, enabled: bool) -> None:
        state = tk.NORMAL if enabled else tk.DISABLED
        self.editor.set_state(state)

    def on_file_saved(self) -> None:
        self.editor.save_file(on_save_as=lambda: self.file_service.get_full_path(self.file_service.generate_unique_filename()))

    def on_file_selected(self, filename: str) -> None:
        self.editor.open_file(filename)
        
    def _run_llm_task(self, processor: TextProcessor, task_name: str) -> None:
        if self.analyzer.is_running or self.translator.is_running:
            self.status_bar.set_status(f"Please wait, another task is in progress...")
            return

        user_input = self.editor.get_content().strip()
        if not user_input:
            self.status_bar.set_status("Text is empty.")
            return

        self.viewer.clear_text()
        self.viewer.append_text(f"--- {task_name} ---\n")
        self._set_input_state(False)

        processor.start(user_input)

    def on_analyze_click(self) -> None:
        self._run_llm_task(self.analyzer, "Analysis")

    def on_translate_click(self) -> None:
        self._run_llm_task(self.translator, "Translation")
    
    def _handle_message(self, message: Message) -> None:
        match message.type:
            case MessageType.STATUS:
                self.status_bar.set_status(message.payload)
            case MessageType.TOKEN:
                self.viewer.append_text(message.payload)
            case MessageType.END:
                self._set_input_state(True)
                self.status_bar.set_status('Ready.')
            case MessageType.ERROR:
                self.viewer.append_text(f'Error: {message.payload}\n\n')
                self._set_input_state(True)
                self.status_bar.set_status('Ready.')
    
    def _process_queue(self) -> None:
        try:
            while True:
                message = self.message_queue.get_nowait()
                self._handle_message(message)
        except Empty:
            pass
        except Exception as e:
            print(f'Error processing message queue: {e}')
        finally:
            self.after(POLLING_INTERVAL_MS, self._process_queue)
    
    def mainloop(self, n: int = 0) -> None:
        self.after(POLLING_INTERVAL_MS, self._process_queue)
        super().mainloop(n)
