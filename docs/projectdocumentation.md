# Problem Statement

Build a modular, agent-based automation system that takes a small structured product dataset and automatically generates machine-readable content pages (JSON). The system must demonstrate multi-agent workflows, agent orchestration, reusable content logic blocks, template-based generation, clean JSON output, and clear system abstraction.

# Solution Overview

The solution is a pure Python, file-based automation system. It ingests a single structured product JSON file, converts it into a canonical internal model using a dedicated parsing agent, and then drives multiple specialized agents to generate three machine-readable pages: an FAQ page, a product detail page, and a comparison page.

Reusable, stateless content logic blocks encapsulate common content structures such as benefits, usage, safety, pricing, and product comparison. These blocks are orchestrated by agents and combined according to simple JSON-based templates that declare required fields and logic block dependencies. The orchestrator script explicitly wires agents and templates in a deterministic pipeline, producing final JSON files under the `output/` directory.

# Scope & Assumptions

- Scope is limited to a single product dataset provided in `input_data.json`.
- No external knowledge, services, or APIs are used; all content is derived only from the given input fields.
- The system is file-based: it uses local JSON files as both input and output, with no databases or network communication.
- The only orchestrated execution entrypoint is `python orchestrator.py` from the project root.
- Agents encapsulate logic only for this content-generation workflow; they do not perform generic ML or NLP tasks.
- Product B in the comparison page is a fixed, structured fictional product defined purely in code for demonstration of comparison logic.

# System Design

## Agent Responsibilities

### ProductParserAgent

- Input: raw dictionary loaded from `input_data.json`.
- Responsibility: convert the raw dictionary into a strongly-typed, canonical `Product` dataclass.
- Normalizes list-like fields (e.g., `skin_type`, `key_ingredients`, `benefits`) to Python lists.
- Provides a single `run()` method that returns the `Product` model as the common representation shared across downstream agents.

### QuestionGeneratorAgent

- Input: canonical `Product` instance.
- Responsibility: deterministically generate 15+ user questions categorized into informational, usage, safety, purchase, and comparison.
- Exposes a `run()` method that returns a flat list of question dictionaries, each containing a `category` and `question` field.
- Uses only product attributes (name, concentration, price, benefits, etc.) to compose questions, ensuring they remain aligned with the source data.

### ContentLogicAgent

- Input: canonical `Product` instance.
- Responsibility: adapt the product model into specialized models for each content logic block (benefits, usage, safety, price) and call the corresponding block functions.
- Uses the following logic blocks:
  - `generate_benefits_block(ProductBenefitsModel)` from `logic_blocks/benefits_block.py`
  - `generate_usage_block(ProductUsageModel)` from `logic_blocks/usage_block.py`
  - `generate_safety_block(ProductSafetyModel)` from `logic_blocks/safety_block.py`
  - `generate_price_block(ProductPriceModel)` from `logic_blocks/price_block.py`
- `run()` aggregates the block outputs into a single dictionary keyed by block name (e.g., `"benefits"`, `"usage"`, `"safety"`, `"price"`).

### FAQPageAgent

- Inputs:
  - `Product` instance (canonical product model)
  - List of categorized questions from `QuestionGeneratorAgent`
  - Content logic blocks dictionary from `ContentLogicAgent`
  - FAQ template from `templates/faq_template.json`
- Responsibility: assemble a fully-structured FAQ JSON page.
- Uses the question category to select how answers are built:
  - Informational answers summarize concentration, ingredients, and benefits.
  - Usage answers reuse the usage block (or fallback to `how_to_use`).
  - Safety answers reuse the safety block side-effect description.
  - Purchase answers use the price block.
  - Comparison answers reuse the benefits block summary.
- `run()` returns a dictionary containing `page_type`, `product_name`, and a `faqs` list (each item has `category`, `question`, `answer`).

### ProductPageAgent

- Inputs:
  - `Product` instance
  - Content logic blocks dictionary
  - Product page template from `templates/product_page_template.json`
- Responsibility: construct the product detail page JSON by mapping product attributes and logic blocks into the template’s required fields.
- Embeds:
  - Basic fields: `product_name`, `concentration`, `skin_type`, `ingredients`, `side_effects`.
  - Structured blocks: `benefits`, `usage`, `safety`, `price` from the logic blocks.
- `run()` returns a dictionary conforming to the product page template’s `required_fields` definition.

### ComparisonPageAgent

- Inputs:
  - `Product` instance
  - Comparison template from `templates/comparison_template.json`
- Responsibility: compare the canonical product with a fictional, structured Product B.
- Internally constructs Product B using a `SimpleProductModel` from `logic_blocks/comparison_block.py` with deterministic fields (name, ingredients, benefits, price).
- Calls `compare_products_block(primary, comparison)` to generate:
  - `primary_product` and `comparison_product` sections
  - `ingredients_comparison`, `benefits_comparison`, `price_comparison`
  - `summary` describing the structural differences
- `run()` attaches the `page_type` from the template and returns the full comparison JSON.

## Orchestration Flow

The orchestration is performed explicitly in `orchestrator.py` and follows a linear, deterministic pipeline.

1. **Load Input Data**
   - Reads `input_data.json` from the project root into a raw dictionary.

2. **Parse Product**
   - Instantiates `ProductParserAgent` with the raw dictionary.
   - Calls `run()` to obtain the canonical `Product` model.

3. **Generate Questions**
   - Instantiates `QuestionGeneratorAgent` with the `Product` instance.
   - Calls `run()` to generate a categorized list of user questions.

4. **Generate Content Logic Blocks**
   - Instantiates `ContentLogicAgent` with the `Product` instance.
   - Calls `run()` to compute block outputs for benefits, usage, safety, and price.

5. **Load Templates**
   - Loads JSON templates from the `templates/` directory:
     - `faq_template.json`
     - `product_page_template.json`
     - `comparison_template.json`
   - Each template specifies `page_type`, `required_fields`, and `logic_block_dependencies` but no hard-coded product text.

6. **Generate FAQ Page**
   - Instantiates `FAQPageAgent` using:
     - Canonical `Product`
     - List of questions
     - Content logic blocks dictionary
     - FAQ template
   - Calls `run()` to receive a structured FAQ page that includes at least five question-answer pairs.

7. **Generate Product Page**
   - Instantiates `ProductPageAgent` with the `Product` instance, logic blocks, and product page template.
   - Calls `run()` to obtain a JSON document exposing product name, ingredients, benefits, usage, side effects, and price.

8. **Generate Comparison Page**
   - Instantiates `ComparisonPageAgent` with the `Product` instance and comparison template.
   - Calls `run()` to produce the comparison page describing GlowBoost versus Product B.

9. **Write Outputs**
   - Writes final JSON structures to:
     - `output/faq.json`
     - `output/product_page.json`
     - `output/comparison_page.json`
   - Uses a simple helper (`write_json`) to ensure directories exist and to format JSON with indentation.

## Reusability

- **Logic Blocks**
  - Implemented in `logic_blocks/` as stateless functions that depend only on their input dataclass models.
  - `generate_benefits_block`, `generate_usage_block`, `generate_safety_block`, and `generate_price_block` are used by multiple agents via the `ContentLogicAgent`.
  - `compare_products_block` is reused anywhere a structural comparison between two product models is needed (currently by `ComparisonPageAgent`).

- **Canonical Product Model**
  - The `Product` dataclass in `ProductParserAgent` is the single internal representation passed between agents.
  - This minimizes coupling: if the external input format changes, only the parser agent needs adjustment.

- **Templates**
  - JSON templates in `templates/` declare `required_fields` and `logic_block_dependencies` instead of embedding product-specific text.
  - Pages can be extended or reshaped by updating templates and the corresponding agents while keeping the core logic blocks unchanged.

## Why No LLM API Is Used

- The system is intentionally constrained to be fully deterministic and self-contained.
- All transformations are implemented using standard Python code, dataclasses, and pure functions.
- No calls are made to external language model APIs (such as OpenAI or others), and there is no dependency on network connectivity or cloud services.
- Questions and answers are generated by formatted strings that strictly combine and rearrange existing input fields.

## Why the System Is Deterministic

- Every agent’s `run()` method is a pure function of its inputs; there is no randomness, time-based logic, or external I/O that affects content.
- Logic blocks in `logic_blocks/` use only their input dataclasses and contain no side effects.
- The orchestrator follows a fixed execution order with a single entrypoint (`main()`), ensuring that the same input file always yields the same output JSON files.
- Product B is defined with constant fields in `ComparisonPageAgent`, making comparison results stable across runs.

## System Flow Diagram

```mermaid
flowchart TD
    A[input_data.json] --> B[ProductParserAgent]

    B --> C[QuestionGeneratorAgent]
    B --> D[ContentLogicAgent]

    C --> E[FAQPageAgent]
    D --> E

    D --> F[ProductPageAgent]

    B --> G[ComparisonPageAgent]

    E --> H[output/faq.json]
    F --> I[output/product_page.json]
    G --> J[output/comparison_page.json]

  ## System Architecture Diagram

```mermaid
flowchart TB
    subgraph Input
        A[input_data.json]
    end

    subgraph Core_Agents
        B[ProductParserAgent]
        C[QuestionGeneratorAgent]
        D[ContentLogicAgent]
    end

    subgraph Page_Agents
        E[FAQPageAgent]
        F[ProductPageAgent]
        G[ComparisonPageAgent]
    end

    subgraph Output
        H[faq.json]
        I[product_page.json]
        J[comparison_page.json]
    end

    A --> B
    B --> C
    B --> D
    C --> E
    D --> E
    D --> F
    B --> G
    E --> H
    F --> I
    G --> J


