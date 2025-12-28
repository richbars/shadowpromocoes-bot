from abc import ABC, abstractmethod


class MercadolivreRepository(ABC):

    @abstractmethod
    def exists_by_product_id(self, product_id: str) -> bool:
        pass

    @abstractmethod
    def find_all_product_ids(self) -> list[str]:
        pass

    @abstractmethod
    def save_all(self, entities: list) -> None:
        pass

