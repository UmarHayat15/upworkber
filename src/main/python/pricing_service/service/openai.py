import os
import json
from openai import OpenAI


class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def search_price(self, product_info: str):
        completion = self.client.chat.completions.create(
            model="gpt-4o-search-preview",
            web_search_options={},
            messages=[
                {
                    "role": "user",
                    "content": f"what is the used priced on ebay for {product_info}, could you provide response in json",
                }
            ],
        )
        return [completion.choices[0].message.content]

    def image_description(self, image_url):
        response = self.client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "user", "content": [
                        {"type": "input_text", "text": "What product is in this image, Brand and Model please if possible"},
                        {"type": "input_image", "image_url": f"{image_url}"},
                    ],
                }
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "image_description",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "brand": {"type": "string"},
                            "model": {"type": "string"},
                            "product_category": {"type": "string"},
                        },
                        "required": ["brand", "model", "product_category"],
                        "additionalProperties": False
                    }
                }
            }
        )
        print(json.loads(response.output_text))
        return response.output_text