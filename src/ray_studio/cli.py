import click
import os
from .dna import load_dna
from .templates import get_template, list_templates
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

    click.echo(f"Generating {template}...")
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

    click.echo(f"Generating {template} for batch export...")
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
