import re

from bs4 import BeautifulSoup
import requests
from infrastructure.dto.productdto import ProductDTO
from application.domain.port.mercadolivre_port import MercadolivrePort


class MercadolivreAdapter(MercadolivrePort):

    def get_products(self) -> list[ProductDTO]:

        product_list: list[ProductDTO] = []
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        }

        url_offers_day = "https://www.mercadolivre.com.br/ofertas?promotion_type=lightning#filter_applied=promotion_type"
        r = requests.get(url_offers_day, headers=headers)
        soup = BeautifulSoup(r.content, "html.parser")

        elements = soup.select("#results > div > div")[0].contents

        for el in elements:
            try:

                highlight = el.find_next('span', class_='poly-component__highlight')

                type = highlight.text.strip() if highlight else "Oferta Relâmpago 🔥"
                image = el.find_next('img', class_='poly-component__picture')['data-src']
                title = el.find_next('h3', class_='poly-component__title-wrapper').text

                link = el.find_next('a', href=True)['href']

                if "click1" in link:
                    link = self._resolve_redirect(link)

                price = el.find_all_next('span', class_='andes-money-amount__fraction')[1].text

                discount = el.find_next('span', class_='andes-money-amount__discount poly-price__disc--pill')

                if not discount:
                    discount = el.find_next('span', class_='poly-price__disc_label andes-money-amount__discount poly-price__disc_label--pill')

                affiliate_link, id = self._build_affiliate_link(link)

                product = ProductDTO(
                    id=id,
                    type=type,
                    title=title,
                    url_image=image,
                    url=link,
                    price=price,
                    discount=discount.text,
                    affiliate_link=affiliate_link
                )

                product_list.append(product)

            except Exception as e:
                print(f"Erro ao processar produto: {e}")
                continue

        return product_list

    def _build_affiliate_link(self, product_url: str) -> tuple[str, str]:

        url = "https://www.mercadolivre.com.br/affiliate-program/api/v2/affiliates/createLink"
        payload = {"urls": [product_url], "tag": "sari7870152"}
        headers = {
            "cookie": "_d2id=ae1e8c38-f920-4b85-833b-e4b92bf3a419-n; _csrf=mvhNg5Dr5e45RETz7o1y--YT",
            "accept": "application/json, text/plain, */*",
            "accept-language": "pt-BR,pt;q=0.5",
            "content-type": "application/json",
            "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6Ijk4OTU4NiIsImFwIjoiMTgzNDg4Njc5MSIsImlkIjoiZmI4YWU4ZTVmM2Q3NTYyMiIsInRyIjoiMzU5YmI1MGNjZTdhYWM0OWYzZDJmMmFlNGU4MWVmZTgiLCJ0aSI6MTc2Njg2NjU1NzE4NCwidGsiOiIxNzA5NzA3In19",
            "traceparent": "00-359bb50cce7aac49f3d2f2ae4e81efe8-fb8ae8e5f3d75622-01",
            "tracestate": "1709707@nr=0-1-989586-1834886791-fb8ae8e5f3d75622----1766866557184",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "x-csrf-token": "qm5AldP5-X-0uZtkL3mRunv-kV91ZJUDy918",
            "x-newrelic-id": "XQ4OVF5VGwIHVFdVBwQBVlE=",
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
                raise ValueError(f"Error in: {url}")

            if not data['short_url']:
                raise ValueError(f"Not exist long_url for: {url}")

            return data['short_url'], data["id"]

        except requests.exceptions.HTTPError as e:
            print(f"HTTP error generating affiliate link: {e}")

        except (KeyError, IndexError, TypeError) as e:
            print(f"Invalid API response structure: {e}")

        except Exception as e:
            print(f"Error in generate affiliate link: {e}")

    def _get_id_product(self, product_url: str) -> str:
        match = re.search(r"/(MLBU?)-?(\d+)", product_url)

        if not match:
            return None

        prefix = match.group(1)
        number = match.group(2)

        return f"{prefix}-{number}"

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