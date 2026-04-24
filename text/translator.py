from typing import Any
from queue import Queue
from .text_processor import TextProcessor, Message
from llm.service import LLMService
from llm.promts import TRANSLATE_SYSTEM_PROMPT

class TextTranslator(TextProcessor):
    
    def start(self, text: str) -> None:
        text = TRANSLATE_SYSTEM_PROMPT.format(
            SOURCE_LANG="Slovak",
            SOURCE_CODE="sk",
            TARGET_LANG="Ukrainian",
            TARGET_CODE="uk",
            TEXT=text
        )
        return super().start(text)

def create_text_translator(queue: Queue[Message], config: dict[str, Any]) -> TextProcessor:
    llm_service = LLMService(llm_config=config)
    return TextTranslator(queue, llm_service=llm_service)
