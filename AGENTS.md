# AGENTS.md — Ray Studio

## Project Overview

AI-powered marketing asset generator inspired by Holo.ai. Produces on-brand visual content from client DNA + templates + AI generation. Part of the Promethia ecosystem.

**Benchmark**: Holo.ai (tryholo.ai)
**Focus**: Static images and marketing assets (v1), extensible to motion/video (future)

## Core Concept

```
Client DNA + Template + AI Generation = On-Brand Marketing Asset
```

The system learns a client's brand identity and automatically produces consistent, professional marketing visuals without manual design work.

## Architecture

```
ray-studio/
├── pyproject.toml
├── src/
│   └── ray_studio/
│       ├── __init__.py
│       ├── cli.py                 # Main CLI (click)
│       ├── config.py              # Settings + API keys
│       │
│       ├── dna/                   # Brand DNA management
│       │   ├── __init__.py
│       │   ├── loader.py          # Load from YAML/MD
│       │   ├── schema.py          # Pydantic models
│       │   └── extractor.py       # Extract DNA from URL (future)
│       │
│       ├── templates/             # Template engine
│       │   ├── __init__.py
│       │   ├── registry.py        # Template discovery
│       │   ├── base.py            # Base template class
│       │   └── concepts/          # Template implementations
│       │       ├── promo.py
│       │       ├── testimonial.py
│       │       ├── before_after.py
│       │       ├── us_vs_them.py
│       │       ├── stats.py
│       │       ├── product_showcase.py
│       │       └── ...
│       │
│       ├── generators/            # AI image generation
│       │   ├── __init__.py
│       │   ├── base.py            # Generator interface
│       │   ├── fal.py             # fal.ai Flux
│       │   ├── replicate.py       # Replicate API
│       │   └── local.py           # Local SD (future)
│       │
│       ├── compositor/            # Image composition
│       │   ├── __init__.py
│       │   ├── engine.py          # PIL-based compositor
│       │   ├── layers.py          # Layer management
│       │   ├── text.py            # Text rendering
│       │   ├── effects.py         # Filters, overlays
│       │   └── atoms/             # SVG atoms (imported)
│       │
│       ├── export/                # FLEXIBLE EXPORT SYSTEM
│       │   ├── __init__.py
│       │   ├── formats.py         # Format definitions
│       │   ├── presets.py         # Platform presets
│       │   ├── optimizer.py       # Size/quality optimization
│       │   └── metadata.py        # EXIF/IPTC injection
│       │
│       └── assets/                # Built-in assets
│           ├── fonts/
│           ├── icons/
│           └── overlays/
│
├── templates/                     # Template definitions (YAML)
│   ├── promo.yaml
│   ├── testimonial.yaml
│   ├── before_after.yaml
│   └── ...
│
├── examples/
│   └── client_dna_example.yaml
│
└── tests/
```

## Brand DNA Schema

```yaml
# client_dna.yaml
brand:
  name: "Acme Corp"
  tagline: "Innovation for Everyone"
  
  # Visual Identity
  colors:
    primary: "#1E40AF"
    secondary: "#60A5FA"
    accent: "#F59E0B"
    background: "#FFFFFF"
    text: "#1F2937"
  
  fonts:
    heading: "Montserrat"
    body: "Inter"
    accent: "Playfair Display"
  
  # Brand Personality
  tone: "professional"  # professional, playful, bold, elegant, minimal
  expression: "elegante"  # maps to visual style
  
  # Assets
  logo:
    primary: "./assets/logo.png"
    white: "./assets/logo-white.png"
    icon: "./assets/icon.png"

audience:
  description: "Small business owners aged 30-50"
  pain_points:
    - "Not enough time for marketing"
    - "Can't afford agencies"
    - "Inconsistent brand presence"
  desires:
    - "Professional-looking content"
    - "Easy to use tools"
    - "Fast results"

products:
  - name: "Pro Plan"
    description: "Everything you need to grow"
    image: "./assets/products/pro.png"
    price: "$49/month"
    
content:
  hashtags: ["#innovation", "#growth", "#business"]
  cta_phrases:
    - "Start Free Trial"
    - "Learn More"
    - "Get Started Today"
```

## Template System

Templates define the visual concept and layout:

```yaml
# templates/promo.yaml
name: promo
description: "Promotional offer with bold CTA"
category: sales

# Layout definition
layout:
  type: stack  # stack, grid, overlay, split
  direction: vertical
  padding: 40

layers:
  - type: background
    source: ai_generate  # ai_generate, solid, gradient, image
    prompt_template: "Modern abstract background, {dna.tone} style, {dna.colors.primary} and {dna.colors.secondary} color scheme, minimal, clean"
    
  - type: logo
    source: dna.brand.logo.primary
    position: top-left
    size: [120, auto]
    margin: 20
    
  - type: text
    content: "{input.headline}"
    font: dna.fonts.heading
    size: 48
    color: dna.colors.text
    position: center
    max_width: 80%
    
  - type: text
    content: "{input.subheadline}"
    font: dna.fonts.body
    size: 24
    color: dna.colors.secondary
    position: below_previous
    margin_top: 16
    
  - type: cta_button
    text: "{input.cta}"
    background: dna.colors.accent
    color: "#FFFFFF"
    position: bottom-center
    padding: [16, 32]
    border_radius: 8
    margin_bottom: 40

# Required inputs
inputs:
  headline:
    type: string
    required: true
    example: "50% OFF This Week Only"
  subheadline:
    type: string
    required: false
    example: "Don't miss out on our biggest sale"
  cta:
    type: string
    default: "Shop Now"
```

## AI Generation Integration

```python
# generators/fal.py
import httpx
from .base import GeneratorBase

class FalGenerator(GeneratorBase):
    """fal.ai Flux image generation"""
    
    BASE_URL = "https://fal.run/fal-ai"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.AsyncClient(
            headers={"Authorization": f"Key {api_key}"}
        )
    
    async def generate(
        self,
        prompt: str,
        size: tuple[int, int] = (1024, 1024),
        model: str = "flux/schnell",  # schnell (fast) or dev (quality)
        seed: int = None
    ) -> bytes:
        """Generate image from prompt"""
        
        response = await self.client.post(
            f"{self.BASE_URL}/{model}",
            json={
                "prompt": prompt,
                "image_size": {"width": size[0], "height": size[1]},
                "seed": seed,
                "num_images": 1
            }
        )
        
        result = response.json()
        image_url = result["images"][0]["url"]
        
        # Download image
        img_response = await self.client.get(image_url)
        return img_response.content
    
    async def generate_with_style(
        self,
        prompt: str,
        style: str,  # elegante, vibrante, minimal, etc.
        dna: BrandDNA,
        size: tuple[int, int]
    ) -> bytes:
        """Generate with brand style applied"""
        
        style_prompts = {
            "elegante": "elegant, sophisticated, premium, clean lines",
            "vibrante": "vibrant, colorful, energetic, dynamic",
            "minimal": "minimalist, clean, simple, whitespace",
            "bold": "bold, impactful, strong contrast, dramatic",
            "warm": "warm tones, cozy, inviting, soft lighting",
        }
        
        enhanced_prompt = f"{prompt}, {style_prompts.get(style, '')}, color palette: {dna.colors.primary} and {dna.colors.secondary}"
        
        return await self.generate(enhanced_prompt, size)
```

## FLEXIBLE EXPORT SYSTEM

The export system is platform-agnostic and format-flexible:

```python
# export/formats.py
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class ImageFormat(Enum):
    PNG = "png"
    JPEG = "jpeg"
    WEBP = "webp"
    AVIF = "avif"
    TIFF = "tiff"
    BMP = "bmp"

class ColorSpace(Enum):
    SRGB = "sRGB"
    ADOBE_RGB = "AdobeRGB"
    CMYK = "CMYK"  # For print
    P3 = "DisplayP3"

@dataclass
class ExportConfig:
    """Flexible export configuration"""
    
    # Dimensions (None = keep original)
    width: Optional[int] = None
    height: Optional[int] = None
    scale: float = 1.0
    
    # Format
    format: ImageFormat = ImageFormat.PNG
    quality: int = 95  # 1-100 for lossy formats
    
    # Color
    color_space: ColorSpace = ColorSpace.SRGB
    bit_depth: int = 8  # 8 or 16
    
    # Optimization
    optimize: bool = True
    strip_metadata: bool = False
    
    # For web
    progressive: bool = False  # Progressive JPEG
    
    # Custom metadata
    metadata: Optional[dict] = None

# export/presets.py
PRESETS = {
    # Social Media - Organic
    "instagram_post": ExportConfig(width=1080, height=1080, format=ImageFormat.JPEG, quality=90),
    "instagram_story": ExportConfig(width=1080, height=1920, format=ImageFormat.JPEG, quality=90),
    "instagram_reel_cover": ExportConfig(width=1080, height=1920, format=ImageFormat.JPEG, quality=90),
    "facebook_post": ExportConfig(width=1200, height=630, format=ImageFormat.JPEG, quality=90),
    "facebook_story": ExportConfig(width=1080, height=1920, format=ImageFormat.JPEG, quality=90),
    "twitter_post": ExportConfig(width=1600, height=900, format=ImageFormat.PNG),
    "linkedin_post": ExportConfig(width=1200, height=627, format=ImageFormat.PNG),
    "pinterest_pin": ExportConfig(width=1000, height=1500, format=ImageFormat.JPEG, quality=90),
    "tiktok_cover": ExportConfig(width=1080, height=1920, format=ImageFormat.JPEG, quality=90),
    "youtube_thumbnail": ExportConfig(width=1280, height=720, format=ImageFormat.JPEG, quality=95),
    "whatsapp_status": ExportConfig(width=1080, height=1920, format=ImageFormat.JPEG, quality=85),
    
    # Google My Business / Local
    "gmn_post": ExportConfig(width=1200, height=900, format=ImageFormat.JPEG, quality=90),
    "gmn_cover": ExportConfig(width=1080, height=608, format=ImageFormat.JPEG, quality=90),
    "gmn_logo": ExportConfig(width=250, height=250, format=ImageFormat.PNG),
    
    # Paid Ads
    "meta_ad_square": ExportConfig(width=1080, height=1080, format=ImageFormat.JPEG, quality=95),
    "meta_ad_story": ExportConfig(width=1080, height=1920, format=ImageFormat.JPEG, quality=95),
    "meta_ad_landscape": ExportConfig(width=1200, height=628, format=ImageFormat.JPEG, quality=95),
    "google_display_300x250": ExportConfig(width=300, height=250, format=ImageFormat.JPEG, quality=90),
    "google_display_728x90": ExportConfig(width=728, height=90, format=ImageFormat.JPEG, quality=90),
    "google_display_160x600": ExportConfig(width=160, height=600, format=ImageFormat.JPEG, quality=90),
    "google_display_320x50": ExportConfig(width=320, height=50, format=ImageFormat.JPEG, quality=90),
    
    # Email
    "email_header": ExportConfig(width=600, height=200, format=ImageFormat.JPEG, quality=85),
    "email_banner": ExportConfig(width=600, height=300, format=ImageFormat.JPEG, quality=85),
    
    # Print (CMYK, high quality)
    "print_a4": ExportConfig(width=2480, height=3508, format=ImageFormat.TIFF, color_space=ColorSpace.CMYK, bit_depth=16),
    "print_flyer": ExportConfig(width=1240, height=1754, format=ImageFormat.TIFF, color_space=ColorSpace.CMYK, bit_depth=16),
    "print_business_card": ExportConfig(width=1050, height=600, format=ImageFormat.TIFF, color_space=ColorSpace.CMYK, bit_depth=16),
    
    # Web/General
    "web_hero": ExportConfig(width=1920, height=1080, format=ImageFormat.WEBP, quality=90),
    "web_og_image": ExportConfig(width=1200, height=630, format=ImageFormat.JPEG, quality=90),
    "favicon": ExportConfig(width=512, height=512, format=ImageFormat.PNG),
    
    # Raw/Maximum Quality
    "raw_png": ExportConfig(format=ImageFormat.PNG, bit_depth=16, optimize=False),
    "raw_tiff": ExportConfig(format=ImageFormat.TIFF, bit_depth=16),
}

# export/exporter.py
class Exporter:
    """Flexible export with any format/size combination"""
    
    def export(
        self,
        image: Image,
        output_path: str,
        config: ExportConfig = None,
        preset: str = None,
        custom_size: tuple[int, int] = None,
        **kwargs
    ) -> str:
        """
        Export image with maximum flexibility.
        
        Args:
            image: PIL Image
            output_path: Destination path
            config: Full ExportConfig object
            preset: Use a preset name (overridden by config)
            custom_size: Override size (width, height)
            **kwargs: Override any ExportConfig field
        
        Returns:
            Path to exported file
        """
        # Build config from preset or defaults
        if config:
            cfg = config
        elif preset:
            cfg = PRESETS.get(preset, ExportConfig())
        else:
            cfg = ExportConfig()
        
        # Apply overrides
        for key, value in kwargs.items():
            if hasattr(cfg, key):
                setattr(cfg, key, value)
        
        if custom_size:
            cfg.width, cfg.height = custom_size
        
        # Process image
        processed = self._process(image, cfg)
        
        # Save
        return self._save(processed, output_path, cfg)
    
    def export_multi(
        self,
        image: Image,
        output_dir: str,
        presets: list[str],
        naming: str = "{preset}"
    ) -> list[str]:
        """Export to multiple formats/sizes at once"""
        paths = []
        for preset in presets:
            cfg = PRESETS[preset]
            ext = cfg.format.value
            filename = naming.format(preset=preset) + f".{ext}"
            path = os.path.join(output_dir, filename)
            paths.append(self.export(image, path, preset=preset))
        return paths
```

## CLI Interface

```python
# cli.py
import click
from .dna import load_dna
from .templates import get_template
from .generators import get_generator
from .compositor import Compositor
from .export import Exporter, PRESETS

@click.group()
def cli():
    """Ray Studio - AI Marketing Asset Generator"""
    pass

@cli.command()
@click.argument("template")
@click.option("--dna", "-d", required=True, help="Path to brand DNA file")
@click.option("--output", "-o", required=True, help="Output path")
@click.option("--preset", "-p", default="instagram_post", help="Export preset")
@click.option("--format", "-f", help="Override format (png, jpeg, webp)")
@click.option("--size", "-s", help="Override size (WxH)")
@click.option("--headline", help="Headline text")
@click.option("--subheadline", help="Subheadline text")
@click.option("--cta", help="CTA button text")
@click.option("--var", multiple=True, help="Additional variables (key=value)")
@click.option("--seed", type=int, help="Random seed for reproducibility")
def generate(template, dna, output, preset, format, size, headline, subheadline, cta, var, seed):
    """Generate a marketing asset from template"""
    
    # Load DNA
    brand_dna = load_dna(dna)
    
    # Load template
    tmpl = get_template(template)
    
    # Build inputs
    inputs = {}
    if headline:
        inputs["headline"] = headline
    if subheadline:
        inputs["subheadline"] = subheadline
    if cta:
        inputs["cta"] = cta
    for v in var:
        key, value = v.split("=", 1)
        inputs[key] = value
    
    # Generate
    compositor = Compositor()
    generator = get_generator()  # Uses configured default
    
    image = compositor.render(
        template=tmpl,
        dna=brand_dna,
        inputs=inputs,
        generator=generator,
        seed=seed
    )
    
    # Export
    exporter = Exporter()
    
    export_kwargs = {}
    if format:
        export_kwargs["format"] = format
    if size:
        w, h = map(int, size.split("x"))
        export_kwargs["custom_size"] = (w, h)
    
    result_path = exporter.export(
        image=image,
        output_path=output,
        preset=preset,
        **export_kwargs
    )
    
    click.echo(f"✓ Generated: {result_path}")

@cli.command()
@click.argument("template")
@click.option("--dna", "-d", required=True)
@click.option("--output-dir", "-o", required=True)
@click.option("--presets", "-p", multiple=True, default=["instagram_post", "facebook_post", "gmn_post"])
@click.option("--headline", required=True)
def batch(template, dna, output_dir, presets, headline):
    """Generate asset in multiple formats at once"""
    
    brand_dna = load_dna(dna)
    tmpl = get_template(template)
    
    compositor = Compositor()
    generator = get_generator()
    exporter = Exporter()
    
    image = compositor.render(
        template=tmpl,
        dna=brand_dna,
        inputs={"headline": headline},
        generator=generator
    )
    
    paths = exporter.export_multi(
        image=image,
        output_dir=output_dir,
        presets=list(presets)
    )
    
    for path in paths:
        click.echo(f"✓ {path}")

@cli.command()
def presets():
    """List available export presets"""
    click.echo("Available presets:\n")
    
    categories = {
        "Social Organic": ["instagram_post", "instagram_story", "facebook_post", "twitter_post", "linkedin_post", "whatsapp_status"],
        "Local/GMN": ["gmn_post", "gmn_cover", "gmn_logo"],
        "Paid Ads": ["meta_ad_square", "meta_ad_story", "google_display_300x250", "google_display_728x90"],
        "Email": ["email_header", "email_banner"],
        "Print": ["print_a4", "print_flyer", "print_business_card"],
        "Web": ["web_hero", "web_og_image", "favicon"],
    }
    
    for cat, names in categories.items():
        click.echo(f"  {cat}:")
        for name in names:
            cfg = PRESETS[name]
            size = f"{cfg.width}x{cfg.height}" if cfg.width else "original"
            click.echo(f"    • {name}: {size} ({cfg.format.value})")
        click.echo()

@cli.command()
def templates():
    """List available templates"""
    from .templates import list_templates
    
    for tmpl in list_templates():
        click.echo(f"  • {tmpl.name}: {tmpl.description}")
```

## Usage Examples

```bash
# Generate single asset
ray-studio generate promo \
  --dna ./client/brand_dna.yaml \
  --output ./output/promo.png \
  --preset instagram_post \
  --headline "50% OFF Today!" \
  --cta "Shop Now"

# Generate for multiple platforms at once
ray-studio batch promo \
  --dna ./client/brand_dna.yaml \
  --output-dir ./output/ \
  --presets instagram_post facebook_post gmn_post meta_ad_square \
  --headline "Grand Opening!"

# Custom size/format
ray-studio generate testimonial \
  --dna ./client/brand_dna.yaml \
  --output ./output/custom.webp \
  --size 1920x1080 \
  --format webp \
  --var quote="Best product ever!" \
  --var author="John D."

# List presets
ray-studio presets

# List templates  
ray-studio templates
```

## Template Library (Initial)

Implement these Holo-inspired templates:

1. **promo** - Promotional offer with bold CTA
2. **testimonial** - Customer quote with photo
3. **before_after** - Side-by-side comparison
4. **us_vs_them** - Feature comparison
5. **stats** - Statistics/numbers highlight
6. **product_showcase** - Product with features
7. **announcement** - News/launch announcement
8. **faq** - Question + Answer format
9. **tips** - Tips/How-to carousel item
10. **quote** - Inspirational/brand quote

## Priority Order

1. Core architecture + CLI skeleton
2. Brand DNA loader + schema
3. Template engine + 3 basic templates (promo, testimonial, product)
4. AI generator integration (fal.ai)
5. Compositor (PIL-based)
6. Export system with all presets
7. Remaining templates
8. Documentation + examples

## Dependencies

```toml
[project]
dependencies = [
    "click>=8.0",
    "pillow>=10.0",
    "pydantic>=2.0",
    "httpx>=0.25",
    "pyyaml>=6.0",
    "python-dotenv>=1.0",
]

[project.optional-dependencies]
dev = ["pytest", "ruff"]
```

## Configuration

```bash
# Environment variables
FAL_API_KEY=your_fal_key
REPLICATE_API_TOKEN=your_replicate_token
RAY_STUDIO_DEFAULT_GENERATOR=fal  # or replicate
```

## Future Extensions (v2+)

- Motion graphics (Lottie/GIF)
- Video generation (Runway, Pika)
- A/B variant generation
- Performance analytics integration
- Direct platform publishing
- Batch campaign generation
