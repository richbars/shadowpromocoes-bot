from abc import ABC, abstractmethod

from infrastructure.dto.productdto import ProductDTO


class MercadolivrePort(ABC):

    @abstractmethod
    def get_products(self) -> list[ProductDTO]:
        pass
