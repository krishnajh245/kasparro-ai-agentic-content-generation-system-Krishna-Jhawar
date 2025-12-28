from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class ProductSafetyModel:
    product_name: str
    side_effects: str


def generate_safety_block(model: ProductSafetyModel) -> Dict[str, Any]:
   
    return {
        "title": "Safety & Side Effects",
        "known_side_effects": model.side_effects,
        "general_guidance": (
            "If you experience discomfort while using the product, consider reducing "
            "frequency of use or discontinuing and referring to the provided side "
            "effects description."
        ),
        "product_reference": model.product_name,
    }
