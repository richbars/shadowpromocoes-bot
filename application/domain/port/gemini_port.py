from abc import ABC, abstractmethod


class GeminiPort(ABC):

    @abstractmethod
    def generate_description(self, prompt) -> str:
        pass
