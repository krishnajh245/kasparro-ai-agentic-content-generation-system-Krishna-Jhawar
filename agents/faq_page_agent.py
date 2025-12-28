from typing import List, Dict, Any

from .product_parser_agent import Product
from .question_generator_agent import Question


class FAQPageAgent:
    """Agent responsible for producing the FAQ page JSON structure."""

    def __init__(
        self,
        product: Product,
        questions: List[Question],
        content_blocks: Dict[str, Any],
        template: Dict[str, Any],
    ) -> None:
        self._product = product
        self._questions = questions
        self._content_blocks = content_blocks
        self._template = template

    def _build_answer(self, question: Question) -> str:
        category = question["category"]
        benefits_block = self._content_blocks.get("benefits", {})
        usage_block = self._content_blocks.get("usage", {})
        safety_block = self._content_blocks.get("safety", {})
        price_block = self._content_blocks.get("price", {})

        if category == "informational":
            return (
                f"{self._product.product_name} has {self._product.concentration} "
                f"and key ingredients {', '.join(self._product.key_ingredients)}. "
                f"It focuses on benefits such as {', '.join(self._product.benefits)}."
            )
        if category == "usage":
            instruction = usage_block.get("instruction", self._product.how_to_use)
            return instruction
        if category == "safety":
            return safety_block.get("known_side_effects", self._product.side_effects)
        if category == "purchase":
            amount = price_block.get("amount", self._product.price)
            return f"The listed price of {self._product.product_name} is {amount}."
        if category == "comparison":
            return benefits_block.get(
                "summary",
                f"{self._product.product_name} is described by its ingredients and benefits.",
            )
        return ""

    def run(self) -> Dict[str, Any]:
        page_type = self._template.get("page_type", "faq")

        faqs: List[Dict[str, str]] = []
        for q in self._questions:
            faqs.append(
                {
                    "category": q["category"],
                    "question": q["question"],
                    "answer": self._build_answer(q),
                }
            )

        return {
            "page_type": page_type,
            "product_name": self._product.product_name,
            "faqs": faqs,
        }
