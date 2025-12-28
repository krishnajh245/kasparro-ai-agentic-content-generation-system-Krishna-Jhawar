from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class ProductPriceModel:
    product_name: str
    price: int


def generate_price_block(model: ProductPriceModel) -> Dict[str, Any]:
    """Generate a deterministic pricing block.

    Stateless: output depends only on the provided model.
    """
    return {
        "title": "Price",
        "product_name": model.product_name,
        "amount": model.price,
        "display": f"{model.price}",
    }
