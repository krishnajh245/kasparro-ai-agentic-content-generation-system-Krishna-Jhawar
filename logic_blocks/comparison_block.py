from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass(frozen=True)
class SimpleProductModel:
    product_name: str
    key_ingredients: List[str]
    benefits: List[str]
    price: int


def compare_products_block(primary: SimpleProductModel, comparison: SimpleProductModel) -> Dict[str, Any]:
    """Create a deterministic comparison block between two products.

    The comparison is purely structural and descriptive, based only on the
    provided product fields.
    """
    ingredients_comparison = {
        "primary": primary.key_ingredients,
        "comparison": comparison.key_ingredients,
    }

    benefits_comparison = {
        "primary": primary.benefits,
        "comparison": comparison.benefits,
    }

    price_comparison = {
        "primary": primary.price,
        "comparison": comparison.price,
    }

    summary = (
        f"{primary.product_name} and {comparison.product_name} differ in "
        f"ingredients, listed benefits, and price. {primary.product_name} is "
        f"priced at {primary.price}, while {comparison.product_name} is priced at "
        f"{comparison.price}."
    )

    return {
        "primary_product": {
            "name": primary.product_name,
            "key_ingredients": primary.key_ingredients,
            "benefits": primary.benefits,
            "price": primary.price,
        },
        "comparison_product": {
            "name": comparison.product_name,
            "key_ingredients": comparison.key_ingredients,
            "benefits": comparison.benefits,
            "price": comparison.price,
        },
        "ingredients_comparison": ingredients_comparison,
        "benefits_comparison": benefits_comparison,
        "price_comparison": price_comparison,
        "summary": summary,
    }
