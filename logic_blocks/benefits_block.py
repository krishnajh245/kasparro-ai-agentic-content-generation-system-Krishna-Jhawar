from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass(frozen=True)
class ProductBenefitsModel:
    product_name: str
    benefits: List[str]
    key_ingredients: List[str]


def generate_benefits_block(model: ProductBenefitsModel) -> Dict[str, Any]:
    """Generate a deterministic benefits block from product benefits and ingredients.

    Stateless: output depends only on the provided model.
    """
    benefit_items = [
        {
            "label": benefit,
            "description": f"{benefit} benefit of {model.product_name}",
        }
        for benefit in model.benefits
    ]

    return {
        "title": "Key Benefits",
        "summary": f"{model.product_name} focuses on: " + ", ".join(model.benefits),
        "benefit_items": benefit_items,
        "key_ingredients": model.key_ingredients,
    }
