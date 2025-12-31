import os
import time

import requests
from dotenv import load_dotenv
from requests import HTTPError, RequestException

from application.domain.port.gemini_port import GeminiPort
from application.domain.dto.productdto import ProductDTO

load_dotenv()

class GeminiAdapter(GeminiPort):

    def __init__(self):
        self._token = os.getenv("GEMINI_TOKEN")
        self._url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

    def generate_description(self, product: ProductDTO) -> str:
        retries = 0
        max_retries = 3
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": (
                                f"Atue como um Copywriter especialista em vendas diretas para Telegram.\n\n"
                                f"Objetivo: Criar um anúncio persuasivo seguindo EXATAMENTE este modelo de formatação:\n\n"
                                f"1. Título em negrito com emojis (Ex: 🔥 **Oferta Relâmpago** 🔥)\n"
                                f"2. Pular duas linhas.\n"
                                f"3. **Nome do Produto** + Principal Benefício.\n"
                                f"4. Pular uma linha.\n"
                                f"5. Dois diferenciais (um por linha) usando bullet points (escolha o melhor emoji).\n"
                                f"6. Pular duas linhas.\n"
                                f"7. Preço e Desconto em negrito (Ex: 💰 **Preço: R$ X (X% OFF)**).\n"
                                f"8. Pular duas linhas.\n"
                                f"9. Chamada para Ação: 👉 [COMPRAR AGORA](link)\n\n"
                                f"REGRAS CRÍTICAS:\n"
                                f"- Use Markdown (asteriscos para negrito: **texto**).\n"
                                f"- Responda APENAS o texto do anúncio, sem introduções ou '---'.\n"
                                f"- Garanta que haja espaço (linhas em branco) entre as seções para não ficar 'tudo junto'.\n\n"
                                f"Dados do Produto: {product}"
                            )
                        }
                    ]
                }
            ]
        }
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self._token
        }

        while retries < max_retries:

            try:
                response = requests.request("POST", self._url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                return data['candidates'][0]['content']['parts'][0]['text']

            except HTTPError as e:
                response = e.response
                status_code = response.status_code

                if status_code == 429:
                    wait_delay = int(response.json()['error']['details'][2]['retryDelay'].replace("s", ""))
                    time.sleep(wait_delay)
                    retries +=1
                    continue

                raise

            except RequestException:
                time.sleep(2 ** retries)
                retries += 1

        raise RuntimeError("Gemini API rate limit exceeded. Too many requests.")
