from dataclasses import dataclass

@dataclass(frozen=True)
class MercadolivreEntity:
    id: str
    affiliate_link: str
