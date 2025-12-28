from typing import List, Dict

from .product_parser_agent import Product


Question = Dict[str, str]


class QuestionGeneratorAgent:
    """Agent that deterministically generates categorized user questions.

    Categories: informational, usage, safety, purchase, comparison.
    """

    def __init__(self, product: Product) -> None:
        self._product = product

    def _informational_questions(self) -> List[Question]:
        p = self._product
        return [
            {
                "category": "informational",
                "question": f"What is {p.product_name}?",
            },
            {
                "category": "informational",
                "question": f"What is the concentration of {p.product_name}?",
            },
            {
                "category": "informational",
                "question": f"Which skin types is {p.product_name} suitable for?",
            },
            {
                "category": "informational",
                "question": f"What are the key ingredients in {p.product_name}?",
            },
        ]

    def _usage_questions(self) -> List[Question]:
        p = self._product
        return [
            {
                "category": "usage",
                "question": f"How should I apply {p.product_name}?",
            },
            {
                "category": "usage",
                "question": f"When should I use {p.product_name} in my routine?",
            },
            {
                "category": "usage",
                "question": f"How many drops of {p.product_name} should I use each time?",
            },
            {
                "category": "usage",
                "question": f"Can I use {p.product_name} in the morning routine?",
            },
        ]

    def _safety_questions(self) -> List[Question]:
        p = self._product
        return [
            {
                "category": "safety",
                "question": f"Can {p.product_name} cause side effects?",
            },
            {
                "category": "safety",
                "question": f"Is {p.product_name} suitable for sensitive skin?",
            },
            {
                "category": "safety",
                "question": f"What should I do if I feel tingling after applying {p.product_name}?",
            },
        ]

    def _purchase_questions(self) -> List[Question]:
        p = self._product
        return [
            {
                "category": "purchase",
                "question": f"What is the price of {p.product_name}?",
            },
            {
                "category": "purchase",
                "question": f"Does {p.product_name} offer good value for its price of {p.price}?",
            },
            {
                "category": "purchase",
                "question": f"Is {p.product_name} suitable as a primary serum at its price of {p.price}?",
            },
        ]

    def _comparison_questions(self) -> List[Question]:
        p = self._product
        return [
            {
                "category": "comparison",
                "question": f"How does {p.product_name} compare to other vitamin C serums in terms of concentration?",
            },
            {
                "category": "comparison",
                "question": f"How does the ingredient list of {p.product_name} compare to another serum?",
            },
            {
                "category": "comparison",
                "question": f"How does the price of {p.product_name} compare to a similar fictional product?",
            },
        ]

    def run(self) -> List[Question]:
        """Return a flat list of categorized questions (15+ total)."""
        questions: List[Question] = []
        questions.extend(self._informational_questions())
        questions.extend(self._usage_questions())
        questions.extend(self._safety_questions())
        questions.extend(self._purchase_questions())
        questions.extend(self._comparison_questions())
        return questions
