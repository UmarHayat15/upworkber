import asyncio
import aiohttp
import base64


class EbayService:
    def __init__(self):
        # Replace with your actual eBay credentials
        self.client_id = 'TinyIndu-lokomoko-SBX-8b020a690-a85f658c'
        self.client_secret = 'SBX-b020a6908aaf-a7b4-4d4b-89ec-f4be'
        self.api_endpoint = "https://api.sandbox.ebay.com"

    async def get_access_token(self, session):
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        print(f'encoded creds: {encoded_credentials}')

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "grant_type": "client_credentials",
            "scope": f"https://api.ebay.com/oauth/api_scope"
        }

        async with session.post(f"{self.api_endpoint}/identity/v1/oauth2/token", headers=headers, data=data) as resp:
            resp.raise_for_status()
            token_json = await resp.json()
            print(f'got token {token_json}')
            return token_json['access_token']

    async def search_similar_products(self, session, token, query, limit=5):
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        params = {
            "q": query,
            "limit": str(limit)
        }

        async with session.get(f"{self.api_endpoint}/buy/browse/v1/item_summary/search", headers=headers, params=params) as resp:
            resp.raise_for_status()
            data = await resp.json()
            items = data.get("itemSummaries", [])

            print("\n=== SIMILAR LISTINGS ===")
            for item in items:
                print("Title:", item.get("title"))
                print(" Item ID:", item.get("itemId"))
                print(" Condition:", item.get("condition"))
                print(" Price:", item.get("price", {}).get("value"), item.get("price", {}).get("currency"))
                print(" URL:", item.get("itemWebUrl"))
                print("-" * 60)

    async def search_catalog_product(self, session, token, query):
        headers = {
            "Authorization": f"Bearer {token}"
        }

        params = {
            "q": query,
            "limit": "3"
        }

        async with session.get(f"{self.api_endpoint}/commerce/catalog/v1_beta/product_summary/search", headers=headers, params=params) as resp:
            resp.raise_for_status()
            data = await resp.json()
            products = data.get("productSummaries", [])

            print("\n=== CATALOG MATCHES ===")
            for product in products:
                print("📘 Catalog Title:", product.get("title"))
                print("   ePID:", product.get("epid"))
                print("   Product URL:", product.get("productWebUrl"))
                print("   Aspects:", product.get("aspects", {}))
                print("=" * 60)

    async def wrapper(self):
        query = "iphone 11 64gb used"
        async with aiohttp.ClientSession() as session:
            token = await self.get_access_token(session)

            await asyncio.gather(
                self.search_similar_products(session, token, query),
                self.search_catalog_product(session, token, query)
            )