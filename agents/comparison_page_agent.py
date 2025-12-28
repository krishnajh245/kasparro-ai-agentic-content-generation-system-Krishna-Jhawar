from typing import Dict, Any, List

from .product_parser_agent import Product
from logic_blocks.comparison_block import SimpleProductModel, compare_products_block


class ComparisonPageAgent:
    """Agent responsible for producing the comparison page JSON structure.

    Compares the primary product with a fictional structured Product B.
    """

    def __init__(self, product: Product, template: Dict[str, Any]) -> None:
        self._product = product
        self._template = template

    def _build_product_b(self) -> SimpleProductModel:
        """Create a fictional but structured Product B.

        Values are deterministic and self-contained.
        """
        product_name = "Product B Serum"
        key_ingredients: List[str] = ["Ingredient 1", "Ingredient 2"]
        benefits: List[str] = ["Benefit A", "Benefit B"]
        price = 799

        return SimpleProductModel(
            product_name=product_name,
            key_ingredients=key_ingredients,
            benefits=benefits,
            price=price,
        )

    def run(self) -> Dict[str, Any]:
        page_type = self._template.get("page_type", "comparison_page")

        primary = SimpleProductModel(
            product_name=self._product.product_name,
            key_ingredients=self._product.key_ingredients,
            benefits=self._product.benefits,
            price=self._product.price,
        )
        product_b = self._build_product_b()

        comparison_block = compare_products_block(primary, product_b)
        comparison_block["page_type"] = page_type

        return comparison_block
