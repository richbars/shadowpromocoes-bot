from abc import ABC, abstractmethod

from application.domain.dto.productdto import ProductDTO


class MercadolivrePort(ABC):

    @abstractmethod
    def get_products(self) -> list[ProductDTO]:
        pass
