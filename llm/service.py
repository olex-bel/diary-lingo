
from typing import Any, Callable, Tuple
from langchain_core.output_parsers import StrOutputParser
from llm.factory import create_model

class LLMService:

    def __init__(self, llm_config: dict[str, Any], system_prompt: str | None = None) -> None:
        self.model = create_model(llm_config=llm_config)
        self.chain = self.model | StrOutputParser()
        self.system_prompt = system_prompt
    
    def stream_response(
        self,
        user_prompt: str,
        on_token: Callable[[str], None]
    ) -> None:
        messages: list[Tuple[str, str]] = []
        
        if self.system_prompt is not None:  
            messages.append(("system", self.system_prompt))
        messages.append(("human", user_prompt))

        for chunk in self.chain.stream(messages):
            on_token(chunk)
