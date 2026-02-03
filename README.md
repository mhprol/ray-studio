# Ray Studio 🎨

AI-powered marketing asset generator — Holo-inspired visual production toolkit.

## Concept

```
Brand DNA + Template + AI Generation = On-Brand Marketing Asset
```

## Features

- 🧬 **Brand DNA**: Colors, fonts, tone, audience, products
- 📐 **Template Library**: Promo, testimonial, before/after, stats, etc.
- 🤖 **AI Generation**: Flux/SDXL via fal.ai or Replicate
- 🖼️ **Compositor**: PIL-based layer composition
- 📤 **Flexible Export**: 30+ presets for any platform/format

## Export Presets

| Category | Presets |
|----------|---------|
| Social Organic | instagram_post, story, facebook, twitter, linkedin, whatsapp |
| Local/GMN | gmn_post, gmn_cover, gmn_logo |
| Paid Ads | meta_ad_square, story, google_display_* |
| Email | email_header, email_banner |
| Print | print_a4, flyer, business_card (CMYK) |
| Web | web_hero, og_image, favicon |

## Usage

```bash
# Single asset
ray-studio generate promo \
  --dna ./brand.yaml \
  --output ./promo.png \
  --preset instagram_post \
  --headline "50% OFF!"

# Multi-platform batch
ray-studio batch promo \
  --dna ./brand.yaml \
  --output-dir ./output/ \
  --presets instagram_post facebook_post gmn_post \
  --headline "Grand Opening!"

# Custom export
ray-studio generate testimonial \
  --dna ./brand.yaml \
  --output ./custom.webp \
  --size 1920x1080 \
  --format webp
```

## Part of Promethia

Ray Studio powers visual production in the Promethia marketing ecosystem.

## License

MIT
