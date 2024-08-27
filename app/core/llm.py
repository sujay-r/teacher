from abc import ABC, abstractmethod
from typing import Dict, Optional

from openai import OpenAI


class LLM(ABC):
    @abstractmethod
    def call_llm(self, messages: Dict[str, str]) -> None:
        '''Sends a message to the LLM'''


class OpenAILLM(LLM):
    def __init__(self, openai_client: OpenAI, model: Optional[str]='gpt-4o-mini') -> None:
        self.openai_client = openai_client
        self.model = model
    
    def call_llm(self, messages: Dict[str, str], temperature: Optional[float]=0.7) -> None:
        llm_response = self.openai_client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature
        )
        return llm_response.choices[0].message.content
