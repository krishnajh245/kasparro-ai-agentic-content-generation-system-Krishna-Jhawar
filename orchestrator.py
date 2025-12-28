import json
from pathlib import Path
from typing import Any, Dict

from agents.product_parser_agent import ProductParserAgent
from agents.question_generator_agent import QuestionGeneratorAgent
from agents.content_logic_agent import ContentLogicAgent
from agents.faq_page_agent import FAQPageAgent
from agents.product_page_agent import ProductPageAgent
from agents.comparison_page_agent import ComparisonPageAgent


BASE_DIR = Path(__file__).parent
INPUT_PATH = BASE_DIR / "input_data.json"
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "output"


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main() -> None:
    # Load raw input data
    raw_input = load_json(INPUT_PATH)

    # Agent 1: parse product into canonical model
    product_parser = ProductParserAgent(raw_input)
    product = product_parser.run()

    # Agent 2: generate categorized questions
    question_generator = QuestionGeneratorAgent(product)
    questions = question_generator.run()

    # Agent 3: generate reusable content logic blocks
    content_logic_agent = ContentLogicAgent(product)
    content_blocks = content_logic_agent.run()

    # Load templates
    faq_template = load_json(TEMPLATES_DIR / "faq_template.json")
    product_page_template = load_json(TEMPLATES_DIR / "product_page_template.json")
    comparison_template = load_json(TEMPLATES_DIR / "comparison_template.json")

    # Agent 4: FAQ page
    faq_agent = FAQPageAgent(
        product=product,
        questions=questions,
        content_blocks=content_blocks,
        template=faq_template,
    )
    faq_page = faq_agent.run()

    # Agent 5: Product page
    product_page_agent = ProductPageAgent(
        product=product,
        content_blocks=content_blocks,
        template=product_page_template,
    )
    product_page = product_page_agent.run()

    # Agent 6: Comparison page
    comparison_agent = ComparisonPageAgent(
        product=product,
        template=comparison_template,
    )
    comparison_page = comparison_agent.run()

    # Write outputs
    write_json(OUTPUT_DIR / "faq.json", faq_page)
    write_json(OUTPUT_DIR / "product_page.json", product_page)
    write_json(OUTPUT_DIR / "comparison_page.json", comparison_page)


if __name__ == "__main__":
    main()
