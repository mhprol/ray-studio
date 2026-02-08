# Ray Studio 🎨

[AI-MANUAL.md](docs/AI-MANUAL.md)

AI-powered marketing asset generator — Holo-inspired visual production toolkit.

## Project Overview

Ray Studio is a visual generation engine designed to streamline the creation of on-brand marketing assets. It combines structured Brand DNA, flexible templates, and state-of-the-art AI generation (Flux/SDXL) to produce high-quality visuals for various platforms.

The core concept revolves around:
```
Brand DNA + Template + AI Generation = On-Brand Marketing Asset
```

Ray Studio handles the heavy lifting of composition, text placement, and image generation, allowing marketers to focus on strategy and creative direction. It serves as the visual production engine within the Promethia marketing ecosystem.

## Installation

Ray Studio requires Python 3.9 or higher.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-org/ray-studio.git
    cd ray-studio
    ```

2.  **Install dependencies:**
    ```bash
    pip install .
    ```

    For development (including testing tools):
    ```bash
    pip install -e ".[dev]"
    ```

## Quick Start

Generate your first asset in seconds.

1.  **Create a Brand DNA file (`brand.yaml`):**
    (See [Brand DNA Configuration](#brand-dna-configuration) for details, or use the example below)
    ```yaml
    brand:
      name: "Acme Corp"
      tagline: "Quality First"
      colors:
        primary: "#007BFF"
        secondary: "#6C757D"
        accent: "#28A745"
        background: "#F8F9FA"
        text: "#343A40"
      fonts:
        heading: "Arial"
        body: "Helvetica"
        accent: "Courier New"
      tone: "professional"
      expression: "minimalist"
      logo:
        primary: "path/to/logo.png"
    ```

2.  **Generate a Promo Image:**
    ```bash
    ray-studio generate promo \
      --dna brand.yaml \
      --output promo.png \
      --headline "Summer Sale" \
      --subheadline "50% Off Everything"
    ```

## CLI Usage Guide

Ray Studio provides a command-line interface for generating assets.

### Generate Single Asset

The `generate` command creates a single asset from a template.

```bash
ray-studio generate <TEMPLATE> [OPTIONS]
```

**Options:**
- `--dna, -d PATH`: Path to Brand DNA YAML file (Required).
- `--output, -o PATH`: Output file path (Required).
- `--preset, -p NAME`: Export preset (e.g., `instagram_post`, `linkedin_post`). Default: `instagram_post`.
- `--headline TEXT`: Headline text.
- `--subheadline TEXT`: Subheadline text.
- `--cta TEXT`: Call-to-action button text.
- `--var KEY=VALUE`: Set arbitrary template variables.

### Batch Generation

The `batch` command generates assets for multiple platforms simultaneously.

```bash
ray-studio batch <TEMPLATE> [OPTIONS]
```

**Options:**
- `--dna, -d PATH`: Path to Brand DNA YAML file (Required).
- `--output-dir, -o PATH`: Directory to save generated assets (Required).
- `--presets, -p NAME`: List of presets to generate (e.g., `instagram_post facebook_post`).
- `--headline TEXT`: Headline text.

### List Resources

- **List Templates:** `ray-studio templates`
- **List Presets:** `ray-studio presets`

## Template System Overview

Templates define the structure and logic of an asset. They are YAML-based configurations located in the `templates/` directory.

A template consists of:
- **Layout**: Defines the overall structure (e.g., `stack`, `grid`).
- **Layers**: Individual components like text, images, or shapes.
- **Inputs**: Variables that can be passed via the CLI (e.g., `headline`, `product_image`).

See `src/ray_studio/templates/base.py` for the Pydantic models defining the schema.

## Brand DNA Configuration

Brand DNA is the single source of truth for visual identity. It is defined in a YAML file.

**Schema (`src/ray_studio/dna/schema.py`):**
- **Brand Identity**: Name, tagline, colors, fonts, tone, expression, logos.
- **Audience**: Description, pain points, desires.
- **Products**: List of products with images and descriptions.
- **Content**: Hashtags, CTA phrases.

## Compositor Operations Guide

The Compositor (`src/ray_studio/compositor/`) is responsible for assembling the asset. It uses the Python Imaging Library (PIL) to stack layers based on the template definition.

**Key Concepts:**
- **Layers**: Can be `background` (solid, gradient, AI-generated), `text`, `logo`, `cta_button`, or `image`.
- **Positioning**: Layers are positioned relative to the canvas or other layers (e.g., `top-left`, `center`, `below_previous`).
- **Styling**: Styles are resolved from the Brand DNA (e.g., `color: dna.brand.colors.primary`).

## Integration with Promethia Pipeline

Ray Studio acts as the visual production node in the Promethia marketing pipeline.

1.  **Strategy Agents (Iris/Nina)**: Analyze market data and generate a creative brief.
2.  **Copywriting**: Generates headlines, body copy, and CTAs based on the brief.
3.  **Ray Studio**:
    - Selects the appropriate template.
    - Resolves Brand DNA parameters.
    - Generates visual elements using AI (if needed).
    - Composites the final asset.
4.  **Publishing**: The generated asset is ready for distribution.

## Examples

### Single-Platform Workflow

Generate a testimonial graphic for Instagram.

```bash
ray-studio generate testimonial \
  --dna brand.yaml \
  --output testimonial_ig.png \
  --preset instagram_post \
  --quote "Best service ever!" \
  --author "Jane Doe"
```

### Multi-Platform Workflow

Generate a product showcase for Instagram, Facebook, and LinkedIn.

```bash
ray-studio batch product_showcase \
  --dna brand.yaml \
  --output-dir ./campaign_launch/ \
  --presets instagram_post facebook_post linkedin_post \
  --product_name "SuperWidget" \
  --product_image ./widget.png \
  --features "Fast\nReliable\nAffordable"
```

## Contributing

Contributions are welcome!

1.  **Fork the repository.**
2.  **Create a feature branch.**
3.  **Install dev dependencies:** `pip install -e ".[dev]"`
4.  **Run tests:**
    ```bash
    PYTHONPATH=src python3 tests/verify_templates.py
    PYTHONPATH=src python3 tests/verify_dna.py
    # Run other verification scripts in tests/ as needed
    ```
5.  **Submit a Pull Request.**

## License

MIT License. See `LICENSE` for details.
