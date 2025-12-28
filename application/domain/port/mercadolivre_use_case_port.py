from abc import ABC, abstractmethod

class MercadolivreUseCasePort(ABC):

    @abstractmethod
    def execute(self) -> None:
        pass