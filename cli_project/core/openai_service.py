import os
from typing import Any, Optional

from openai import OpenAI


class OpenAIService:
    def __init__(self, model: str):
        provider = (os.getenv("LLM_PROVIDER", "openai") or "openai").lower()
        base_url = os.getenv("LLM_BASE_URL", "").strip()

        if provider == "groq" and not base_url:
            base_url = "https://api.groq.com/openai/v1"

        api_key = os.getenv("LLM_API_KEY", "").strip()
        if not api_key:
            # Provider-specific fallbacks for convenience
            api_key = (
                os.getenv("GROQ_API_KEY", "").strip()
                if provider == "groq"
                else os.getenv("OPENAI_API_KEY", "").strip()
            )

        if not api_key:
            if provider == "groq":
                raise ValueError("GROQ_API_KEY (o LLM_API_KEY) no puede estar vacío. Revisa tu .env")
            raise ValueError("OPENAI_API_KEY (o LLM_API_KEY) no puede estar vacío. Revisa tu .env")

        self.client = OpenAI(api_key=api_key, base_url=base_url or None)
        self.model = model

    def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        tools: Optional[list[dict[str, Any]]] = None,
        temperature: float = 1.0,
    ) -> Any:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }

        # OpenAI API will error if you send tools=[]; only include when non-empty.
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        return self.client.chat.completions.create(**kwargs)

    @staticmethod
    def assistant_text(message: Any) -> str:
        # OpenAI chat completion message content can be None when tool_calls are returned.
        return message.content or ""
