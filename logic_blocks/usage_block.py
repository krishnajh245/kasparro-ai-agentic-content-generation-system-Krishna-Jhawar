from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass(frozen=True)
class ProductUsageModel:
    product_name: str
    how_to_use: str
    skin_type: List[str]


def generate_usage_block(model: ProductUsageModel) -> Dict[str, Any]:
    """Generate a deterministic usage block based on how_to_use and skin types.

    Stateless: output depends only on the provided model.
    """
    return {
        "title": "How to Use",
        "instruction": model.how_to_use,
        "recommended_skin_types": model.skin_type,
        "routine_note": (
            f"Use {model.product_name} as directed in your routine. "
            f"It is suitable for: {', '.join(model.skin_type)} skin types."
        ),
    }
