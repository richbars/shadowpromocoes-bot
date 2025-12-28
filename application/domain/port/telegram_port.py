from abc import ABC, abstractmethod
from application.domain.dto.productdto import ProductDTO

class TelegramPort(ABC):

    @abstractmethod
    def send_messages(self, products: list[ProductDTO]) -> None:
        pass