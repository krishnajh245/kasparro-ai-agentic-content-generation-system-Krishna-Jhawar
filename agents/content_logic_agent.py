from typing import Dict, Any

from .product_parser_agent import Product
from logic_blocks.benefits_block import ProductBenefitsModel, generate_benefits_block
from logic_blocks.usage_block import ProductUsageModel, generate_usage_block
from logic_blocks.safety_block import ProductSafetyModel, generate_safety_block
from logic_blocks.price_block import ProductPriceModel, generate_price_block


class ContentLogicAgent:
    """Agent that aggregates reusable, stateless content logic blocks."""

    def __init__(self, product: Product) -> None:
        self._product = product

    def run(self) -> Dict[str, Any]:
        benefits_model = ProductBenefitsModel(
            product_name=self._product.product_name,
            benefits=self._product.benefits,
            key_ingredients=self._product.key_ingredients,
        )
        usage_model = ProductUsageModel(
            product_name=self._product.product_name,
            how_to_use=self._product.how_to_use,
            skin_type=self._product.skin_type,
        )
        safety_model = ProductSafetyModel(
            product_name=self._product.product_name,
            side_effects=self._product.side_effects,
        )
        price_model = ProductPriceModel(
            product_name=self._product.product_name,
            price=self._product.price,
        )

        return {
            "benefits": generate_benefits_block(benefits_model),
            "usage": generate_usage_block(usage_model),
            "safety": generate_safety_block(safety_model),
            "price": generate_price_block(price_model),
        }
