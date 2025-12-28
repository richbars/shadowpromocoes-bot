from application.domain.entitie.mercadolivre_entity import MercadolivreEntity
from application.domain.port.mercadolivre_port import MercadolivrePort
from application.domain.port.mercadolivre_repository_port import MercadolivreRepository
from application.domain.port.mercadolivre_use_case_port import MercadolivreUseCasePort
from application.domain.port.telegram_port import TelegramPort

class MercadolivreUseCase(MercadolivreUseCasePort):

    def __init__(
        self,
        mercadolivre_port: MercadolivrePort,
        telegram_port: TelegramPort,
        mercadolivre_repository: MercadolivreRepository
    ):
        self.mercadolivre_port = mercadolivre_port
        self.telegram_port = telegram_port
        self.mercadolivre_repository = mercadolivre_repository

    def execute(self) -> None:
        try:
            products = self.mercadolivre_port.get_products()
            existing_ids = set(self.mercadolivre_repository.find_all_product_ids())

            new_products = [p for p in products if p.id not in existing_ids]
            if not new_products:
                return

            successful_products = []

            for p in new_products:
                try:
                    self.telegram_port.send_messages([p])
                    successful_products.append(MercadolivreEntity(p.id, p.affiliate_link))
                except Exception as e:
                    print(f"Erro ao enviar produto {p.id} para o Telegram: {e}")

            if successful_products:
                try:
                    self.mercadolivre_repository.save_all(successful_products)
                except Exception as e:
                    print(f"Erro ao salvar produtos na base: {e}")

        except Exception as e:
            print(f"Erro ao executar a rotina do Mercadolivre: {e}")

