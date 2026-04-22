from typing import Any

def _create_ollama_model(model_name: str, temperature: float):
    from langchain_ollama import ChatOllama

    return ChatOllama(
        model=model_name,
        validate_model_on_init=True,
        temperature=temperature
    )

def create_model(llm_config: dict[str, Any]):
    provider = llm_config['provider']
    model = llm_config['model']
    temperature = llm_config['temperature']

    match provider:
        case 'ollama':
            return _create_ollama_model(model_name=model, temperature=temperature)
        case _:
            raise ValueError(f'Unsupported LLM provider: {provider}')