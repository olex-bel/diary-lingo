from typing import Any
from queue import Queue
from .text_processor import TextProcessor, Message
from llm.service import LLMService
from llm.promts import ANALYZE_SYSTEM_PROMPT

def create_text_analyzer(queue: Queue[Message], config: dict[str, Any]) -> TextProcessor:
    llm_service = LLMService(llm_config=config, system_prompt=ANALYZE_SYSTEM_PROMPT)
    return TextProcessor(queue, llm_service=llm_service)
