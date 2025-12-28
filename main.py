import time
import schedule

from application.use_case.mercadolivre_use_case import MercadolivreUseCase
from infrastructure.adapter.mercadolivre_adapter import MercadolivreAdapter
from infrastructure.adapter.geminai_adapter import GeminiAdapter
from infrastructure.adapter.telegram_adapter import TelegramAdapter
from infrastructure.repository.mercadolivre_repository_impl import MercadolivreRepositoryImpl


def job(use_case: MercadolivreUseCase):
    print("🚀 Executando job MercadoLivre...")
    try:
        use_case.execute()
        print("✅ Job finalizado com sucesso\n")
    except Exception as e:
        print(f"❌ Erro no job: {e}\n")


if __name__ == "__main__":
    gemini_port = GeminiAdapter()
    mercadolivre_port = MercadolivreAdapter()
    telegram_port = TelegramAdapter(gemini_port)
    mercadolivre_repository = MercadolivreRepositoryImpl()

    use_case = MercadolivreUseCase(
        mercadolivre_port=mercadolivre_port,
        telegram_port=telegram_port,
        mercadolivre_repository=mercadolivre_repository
    )

    schedule.every(5).minutes.do(job, use_case=use_case)

    print("⏱ Scheduler iniciado (a cada 5 minutos)...\n")

    while True:
        schedule.run_pending()
        time.sleep(1)
