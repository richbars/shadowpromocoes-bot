from dataclasses import dataclass


@dataclass(frozen=True)
class ProductDTO:
    id: str
    type: str
    title: str
    url_image: str
    url: str
    price: str
    discount: str
    affiliate_link: str
