from . import text

def ask(prompt: str, model: str = "gpt-4o-mini", temp: float = 0.0) -> str:
    """
    Call an LLM by name.

    If the model string contains a '/', it is treated as an OpenRouter model
    (e.g. 'openai/gpt-4o-mini'). Otherwise it is treated as an OpenAI model
    (e.g. 'gpt-4o' or 'gpt-4o-mini').
    """
    if "/" in model:
        client = text.OpenRouter(model_id=model, temperature=temp)
    else:
        client = text.OpenAI(model_id=model, temperature=temp)
    return client(prompt)
