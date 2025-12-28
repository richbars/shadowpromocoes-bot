import os
import time
import requests
from dotenv import load_dotenv
from requests import HTTPError

from application.domain.port.telegram_port import TelegramPort
from application.domain.dto.productdto import ProductDTO
from application.domain.port.gemini_port import GeminiPort

load_dotenv()

class TelegramAdapter(TelegramPort):

    def __init__(self, gemini_port: GeminiPort):
        self._bot_token = os.getenv("TELEGRAM_TOKEN")
        self._channel_id = os.getenv("TELEGRAM_CHANNEL")
        self._gemini_port = gemini_port

        if not self._bot_token or not self._channel_id:
            raise RuntimeError("TELEGRAM_TOKEN ou TELEGRAM_CHANNEL não definidos")

        self._base_url = f"https://api.telegram.org/bot{self._bot_token}"

    def send_messages(self, products: list[ProductDTO]) -> None:

        for i in products:
            caption = self._build_caption(i)
            payload = {
                "chat_id": self._channel_id,
                "photo": i.url_image,
                "caption": caption,
                "parse_mode": "Markdown"
            }
            self._send_with_retry(payload)


    def _build_caption(self, product: ProductDTO) -> str:
        return (
            f"🔥 *{product.type}*\n\n"
            f"*{product.title}*\n\n"
            f"💰 *Preço:* R$ {product.price}\n"
            f"🏷 *Desconto:* {product.discount}\n\n"
            f"👉 [COMPRAR AGORA]({product.affiliate_link})"
        )

    def _send_with_retry(self, payload: dict, max_retries: int = 3) -> None:
        retries = 0

        while retries <= max_retries:
            try:
                time.sleep(1.2)
                response = requests.post(
                    f"{self._base_url}/sendPhoto",
                    json=payload,
                    timeout=10
                )
                response.raise_for_status()
                return

            except HTTPError as e:
                response = e.response

                if response is not None and response.status_code == 429:
                    retry_after = response.json().get(
                        "parameters", {}
                    ).get("retry_after", 5)

                    time.sleep(retry_after)
                    retries += 1
                    continue

                raise

        raise RuntimeError("Falha ao enviar mensagem após múltiplas tentativas")
