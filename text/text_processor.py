import time
import threading
from queue import Queue
from dataclasses import dataclass
from enum import Enum
from llm.service import LLMService

class MessageType(Enum):
    STATUS = "status"
    TOKEN = "token"
    END = "end"
    ERROR = "error"

@dataclass
class Message:
    type: MessageType
    payload: str

class TextProcessor:
    
    def __init__(self, queue: Queue[Message], llm_service: LLMService) -> None:
        self.queue = queue
        self.is_running = False
        self.llm_service = llm_service
        self.msg_start = "Processing..."
        self.msg_end = "Finished in {elapsed:.1f}s."
    
    def _emit(self, message_type: MessageType, payload: str) -> None:
        message = Message(type=message_type, payload=payload)
        self.queue.put(message)
    
    def _on_status_update(self, message: str):
        self._emit(MessageType.STATUS, message)
    
    def _on_token(self, chunk: str):
        self._emit(MessageType.TOKEN, chunk)
    
    def _process_text(self, text: str) -> None:
        self.is_running = True
        try:
            self._emit(MessageType.STATUS, self.msg_start)
            start_time = time.perf_counter()
            self.llm_service.stream_response(
                user_prompt=text,
                on_token=self._on_token
            )
            elapsed = time.perf_counter() - start_time
            self._emit(MessageType.STATUS, self.msg_end.format(elapsed=elapsed))
            self._emit(MessageType.END, '')
        except Exception as e:
            self._emit(MessageType.ERROR, str(e))
        finally:
            self.is_running = False

    def start(self, text: str) -> None:
        if not self.is_running:
            threading.Thread(target=self._process_text, args=(text,), daemon=True).start()