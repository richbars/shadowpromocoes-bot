import os

from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv

from infrastructure.dto.productdto import ProductDTO
from application.domain.port.mercadolivre_port import MercadolivrePort
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

class MercadolivreAdapter(MercadolivrePort):

    def __init__(self):
        self._csrf_token = os.getenv("CSRF_TOKEN")

    def get_products(self) -> list[ProductDTO]:
        product_list = []

        rlightning, rday = self._fetch_offers()

        try:
            soup_lightning = BeautifulSoup(rlightning.content, "html.parser")
            soup_day = BeautifulSoup(rday.content, "html.parser")

            elements_lightning = soup_lightning.select("#results > div > div")[0].contents
            elements_day = soup_day.select("#results > div > div")[0].contents

            with ThreadPoolExecutor(max_workers=10) as executor:
                product_list.extend(filter(None, executor.map(self._parse_product, elements_lightning)))

            with ThreadPoolExecutor(max_workers=10) as executor:
                product_list.extend(filter(None, executor.map(self._parse_product, elements_day)))

        except Exception as e:
            print(f"Erro ao processar HTML: {e}")
            return product_list

        return product_list

    def _build_affiliate_link(self, product_url: str) -> tuple[str, str]:

        url = "https://www.mercadolivre.com.br/affiliate-program/api/v2/affiliates/createLink"
        payload = {"urls": [product_url], "tag": "sari7870152"}
        headers = {
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "x-csrf-token": self._csrf_token,
            "Cookie": (
                "ftid=s7BHX0Y6JhKfWeFarvpvY0woWTUQAGIW-1758834340722; "
                "orgnickp=SARI7870152; "
                "orguseridp=296388989; "
                "cookiesPreferencesNotLogged=%7B%22categories%22%3A%7B%22advertising%22%3Atrue%2C%22functionality%22%3Anull%2C%22performance%22%3Anull%2C%22traceability%22%3Atrue%7D%7D; "
                "p_dsid=2cfcfb33-e22c-4805-9984-df8454d2b795-1758834473882; "
                "_d2id=7cdafb2f-8987-48e7-82f9-b24c145930a8; "
                "_csrf=9qZwJKn8mKa-Wx8ohpyILclg; "
                "ssid=ghy-101808-IHjv79MMwrf1MhZ2Ao66cHHLxDGH0L-__-296388989-__-1855483212024--RRR_0-RRR_0; "
                "cp=07178540; "
                "ml_cart-quantity=0"
            )
        }

        try:
            response = requests.request("POST", url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()['urls'][0]

            if not response:
                raise ValueError(f"Error in: {product_url}")

            if not data['short_url']:
                raise ValueError(f"Not exist long_url for: {product_url}")

            return data['short_url'], data["id"]

        except requests.exceptions.HTTPError as e:
            print(f"HTTP error generating affiliate link for URL {product_url}: {e}")

        except (KeyError, IndexError, TypeError) as e:
            print(f"URL not allowed in affiliates program ({product_url}): {e}")

        except Exception as e:
            print(f"Error generating affiliate link for URL {product_url}: {e}")

    def _resolve_redirect(self, url: str) -> str:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        }
        response = requests.get(
            url,
            allow_redirects=True,
            timeout=10,
            headers=headers
        )
        return response.url

    def _parse_product(self, el):
        try:
            highlight = el.select_one('span.poly-component__highlight')
            type = highlight.text.strip() if highlight else "Oferta Relâmpago 🔥"

            image_tag = el.select_one('img.poly-component__picture')
            image = image_tag['data-src'] if image_tag else ""

            title_tag = el.select_one('h3.poly-component__title-wrapper')
            title = title_tag.text.strip() if title_tag else "Sem título"

            link_tag = el.select_one('a[href]')
            link = link_tag['href'] if link_tag else ""

            if "click" in link:
                link = self._resolve_redirect(link)

            price_tags = el.select('span.andes-money-amount__fraction')
            price = price_tags[1].text.strip() if len(price_tags) > 1 else "0"

            discount_tag = el.select_one('span.andes-money-amount__discount, span.poly-price__disc_label')
            discount = discount_tag.text.strip() if discount_tag else ""

            affiliate_link, id = self._build_affiliate_link(link)

            return ProductDTO(
                id=id,
                type=type,
                title=title,
                url_image=image,
                url=link,
                price=price,
                discount=discount,
                affiliate_link=affiliate_link
            )

        except Exception as e:
            print(f"Erro ao processar produto: {e}")
            return None

    def _fetch_offers(self) -> tuple[requests.Response, requests.Response]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        }

        try:
            url_offers_lightning = "https://www.mercadolivre.com.br/ofertas?promotion_type=lightning"
            url_offers_day = "https://www.mercadolivre.com.br/ofertas?promotion_type=deal_of_the_day"

            rlightning = requests.get(url_offers_lightning, headers=headers, timeout=10)
            rlightning.raise_for_status()

            rday = requests.get(url_offers_day, headers=headers, timeout=10)
            rday.raise_for_status()

            return rlightning, rday

        except requests.RequestException as e:
            print(f"Erro ao fazer requisição: {e}")
