
from typing import Any, Callable
from langchain_core.output_parsers import StrOutputParser
from llm.factory import create_model
from llm.promts import SYSTEM_PROMPT

class LLMService:

    def __init__(self, llm_config: dict[str, Any]) -> None:
        self.model = create_model(llm_config=llm_config)
        self.chain = self.model | StrOutputParser()
    
    def stream_response(
        self,
        user_prompt: str,
        on_token: Callable[[str], None]
    ) -> None:
        messages = [
            ("system", SYSTEM_PROMPT),
            ("human", user_prompt),
        ]

        for chunk in self.chain.stream(messages):
            on_token(chunk)
