from typing import Dict, Any

from .product_parser_agent import Product


class ProductPageAgent:
    """Agent responsible for producing the product page JSON structure."""

    def __init__(
        self,
        product: Product,
        content_blocks: Dict[str, Any],
        template: Dict[str, Any],
    ) -> None:
        self._product = product
        self._content_blocks = content_blocks
        self._template = template

    def run(self) -> Dict[str, Any]:
        page_type = self._template.get("page_type", "product_page")

        return {
            "page_type": page_type,
            "product_name": self._product.product_name,
            "concentration": self._product.concentration,
            "skin_type": self._product.skin_type,
            "ingredients": self._product.key_ingredients,
            "benefits": self._content_blocks.get("benefits", {}),
            "usage": self._content_blocks.get("usage", {}),
            "safety": self._content_blocks.get("safety", {}),
            "side_effects": self._product.side_effects,
            "price": self._content_blocks.get("price", {}),
        }
