from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass(frozen=True)
class Product:
    """Canonical internal product model used across the system."""

    product_name: str
    concentration: str
    skin_type: List[str]
    key_ingredients: List[str]
    benefits: List[str]
    how_to_use: str
    side_effects: str
    price: int


class ProductParserAgent:
    """Agent responsible for converting raw input into the canonical Product model."""

    def __init__(self, raw_data: Dict[str, Any]) -> None:
        self._raw_data = raw_data

    def run(self) -> Product:
        # Ensure all list-like fields are lists
        skin_type = list(self._raw_data.get("skin_type", []))
        key_ingredients = list(self._raw_data.get("key_ingredients", []))
        benefits = list(self._raw_data.get("benefits", []))

        return Product(
            product_name=self._raw_data.get("product_name", ""),
            concentration=self._raw_data.get("concentration", ""),
            skin_type=skin_type,
            key_ingredients=key_ingredients,
            benefits=benefits,
            how_to_use=self._raw_data.get("how_to_use", ""),
            side_effects=self._raw_data.get("side_effects", ""),
            price=int(self._raw_data.get("price", 0)),
        )
