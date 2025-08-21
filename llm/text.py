import os
import httpx
import openai


OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


class BaseModel:
    """Abstract base class for LLM models."""

    def __init__(self, name: str, temperature: float = 0.0) -> None:
        self.name = name
        self.temperature = temperature

    def __call__(self, prompt: str) -> str:
        raise NotImplementedError()

    @property
    def call_timeout(self) -> int:
        return 0


class OpenRouter(BaseModel):
    """Wrapper for OpenRouter API supporting multiple models."""

    def __init__(self, model_id: str = "openai/gpt-4o-mini", temperature: float = 0):
        """
        Args:
            model_id (str): Full OpenRouter model ID (e.g. "openai/gpt-4o-mini").
            temperature (float): Sampling temperature.
        """
        super().__init__(model_id, temperature)
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise EnvironmentError("Missing OPENROUTER_API_KEY in environment variables.")

        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=OPENROUTER_BASE_URL,
            timeout=httpx.Timeout(connect=5, read=15, write=15, pool=5),
        )
        self.model = model_id

    def __call__(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
        )
        return response.choices[0].message.content

    @property
    def call_timeout(self) -> int:
        return 5


class OpenAI(BaseModel):
    """Wrapper for OpenAI API with consistent interface."""

    def __init__(self, model_id: str = "gpt-4o-mini", temperature: float = 0.0) -> None:
        """
        Args:
            model_id (str): OpenAI model ID (e.g. "gpt-4o" or "gpt-4o-mini").
            temperature (float): Sampling temperature.
        """
        super().__init__("OpenAI", temperature)
        self.client = openai.OpenAI()
        self.model = model_id

    def __call__(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt},
            ],
            temperature=self.temperature,
        )
        return response.choices[0].message.content

    @property
    def call_timeout(self) -> int:
        return 1
