# Ray Studio AI Manual

> **Design Principle: Progressive Disclosure**
> This manual is structured for AI agents. Load ONLY what you need.

## Level 1 - Quick Reference

| Intent | Command | Minimal Example |
| :--- | :--- | :--- |
| **Generate Single Asset** | `ray-studio generate <template>` | `ray-studio generate promo --dna brand.yaml --output out.png --headline "Sale!"` |
| **Batch Generate** | `ray-studio batch <template>` | `ray-studio batch promo --dna brand.yaml --output-dir ./out --presets instagram_post facebook_post --headline "Sale!"` |
| **List Templates** | `ray-studio templates` | `ray-studio templates` |
| **List Export Presets** | `ray-studio presets` | `ray-studio presets` |
| **Figma Status** | `ray-studio figma status` | `ray-studio figma status --channel <id>` |
| **Figma Scan Text** | `ray-studio figma scan-text` | `ray-studio figma scan-text <node_id> --channel <id>` |
| **Init Project** | `ray-studio figma init` | `ray-studio figma init "My Project"` |

---

## Level 2 - Detailed Usage

### Core Commands

#### `generate`
Generate a single marketing asset from a template.

**Arguments:**
- `TEMPLATE`: Template name (e.g., `promo`, `testimonial`).

**Options:**
- `--dna, -d PATH`: Path to Brand DNA YAML file (Required).
- `--output, -o PATH`: Output file path (Required).
- `--preset, -p NAME`: Export preset (Default: `instagram_post`).
- `--format, -f TYPE`: Override format (`png`, `jpeg`, `webp`).
- `--size, -s WxH`: Override size (e.g., `1080x1350`).
- `--headline TEXT`: Headline text input.
- `--subheadline TEXT`: Subheadline text input.
- `--cta TEXT`: CTA button text input.
- `--var KEY=VALUE`: Additional template variables.
- `--seed INT`: Random seed for reproducibility.

#### `batch`
Generate assets for multiple platforms simultaneously.

**Arguments:**
- `TEMPLATE`: Template name.

**Options:**
- `--dna, -d PATH`: Path to Brand DNA YAML file (Required).
- `--output-dir, -o PATH`: Output directory (Required).
- `--presets, -p NAME`: List of presets (Default: `instagram_post`, `facebook_post`, `gmn_post`).
- `--headline TEXT`: Headline text input (Required).

#### `presets`
List all available export presets with their dimensions and formats.

#### `templates`
List all available templates with descriptions.

### Figma Integration
Bridge-based integration for Figma document manipulation.

#### `figma status`
Check connection to Figma bridge.
- `--channel, -c ID`: Channel ID from Figma plugin (Required).
- `--host IP`: Bridge host IP (Default: `172.17.0.1`).
- `--port PORT`: Bridge port (Default: `3055`).

#### `figma info`
Get document metadata.
- Same options as `status`.

#### `figma scan-text`
Scan text nodes under a specific node.
- `NODE_ID`: Target node ID.
- Same options as `status`.

#### `figma set-text`
Modify text content of a node.
- `TARGET`: Node ID or Template Path.
- `TEXT`: New text content.
- `--is-path`: Treat TARGET as a template path (e.g., "Frame 1/Text").

#### `figma init`
Initialize `Ray/figma-project.json`.
- `NAME`: Project name.
- `--path PATH`: Config file path.

### Templates Reference

#### `promo`
Promotional offer with bold CTA.
- **Inputs:**
    - `headline` (Required): Main text.
    - `subheadline`: Secondary text.
    - `cta` (Default: "Shop Now"): Button text.

#### `product_showcase`
Product showcase with features list.
- **Inputs:**
    - `product_name` (Required): Name of product.
    - `product_image` (Required): Path to product image.
    - `features` (Required): List of features (newline separated).
    - `cta` (Default: "Buy Now"): Button text.

#### `testimonial`
Customer quote with photo.
- **Inputs:**
    - `quote` (Required): Customer quote.
    - `author` (Required): Customer name.

### Brand DNA Schema (YAML)
Located in `src/ray_studio/dna/schema.py`.

```yaml
brand:
  name: str
  tagline: str
  colors:
    primary: str (hex)
    secondary: str (hex)
    accent: str (hex)
    background: str (hex)
    text: str (hex)
  fonts:
    heading: str
    body: str
    accent: str
  tone: str (e.g., professional, playful)
  expression: str (maps to visual style)
  logo:
    primary: path
    white: path (optional)
    icon: path (optional)

audience:
  description: str
  pain_points: [str]
  desires: [str]

products:
  - name: str
    description: str
    image: path
    price: str (optional)

content:
  hashtags: [str]
  cta_phrases: [str]
```

### Compositor & Layers
Based on `src/ray_studio/compositor/`.

**Layer Types:**
- `background`: Solid color, gradient, image, or `ai_generate`.
- `logo`: Brand logo from DNA.
- `text`: Text content with font/color/size.
- `cta_button`: Button with background/text.
- `image`: Static image from path.

**Common Properties:**
- `position`: `top-left`, `center`, `bottom-right`, `below_previous`, etc.
- `size`: `[width, height]` (can use percentages or "auto").
- `margin`, `padding`, `border_radius`.
- `font`, `color`, `background` (can reference DNA values like `dna.brand.colors.primary`).

### Generators
Backend configuration for AI generation.

**Fal.ai (Flux)**
- **Env Var:** `FAL_API_KEY`
- **Models:** `flux/schnell` (fast), `flux/dev` (quality).
- **Style:** Uses `dna.brand.tone` or `dna.brand.expression` to enhance prompts.

### Export Presets
Located in `src/ray_studio/export/presets.py`.

| Category | Presets |
| :--- | :--- |
| **Social Organic** | `instagram_post`, `instagram_story`, `instagram_reel_cover`, `facebook_post`, `facebook_story`, `twitter_post`, `linkedin_post`, `pinterest_pin`, `tiktok_cover`, `youtube_thumbnail`, `whatsapp_status` |
| **Local/GMN** | `gmn_post`, `gmn_cover`, `gmn_logo` |
| **Paid Ads** | `meta_ad_square`, `meta_ad_story`, `meta_ad_landscape`, `google_display_*` (300x250, 728x90, 160x600, 320x50) |
| **Email** | `email_header`, `email_banner` |
| **Print** | `print_a4`, `print_flyer`, `print_business_card` (CMYK, TIFF) |
| **Web** | `web_hero`, `web_og_image`, `favicon` |
| **Raw** | `raw_png`, `raw_tiff` |

---

## Level 3 - Patterns and Combinations

### Multi-Platform Campaign
Generate assets for Instagram, Facebook, and Google My Business from a single brief.

```bash
ray-studio batch promo \
  --dna ./client_dna.yaml \
  --output-dir ./campaign_assets/ \
  --presets instagram_post facebook_post gmn_post \
  --headline "Summer Sale Ends Soon!"
```

### Brand DNA + Template + AI Pipeline
1.  **Load DNA:** `brand.tone` ("minimal"), `brand.colors.primary` ("#000000").
2.  **Select Template:** `promo`.
3.  **AI Generation:**
    - Background layer has `source: ai_generate`.
    - Prompt template: "Modern abstract background, {dna.brand.tone} style..."
    - Resolved Prompt: "Modern abstract background, minimal style, #000000 and ... color scheme"
    - Generator calls Fal.ai with resolved prompt.
4.  **Composition:** Text and Logo layers are composited over the generated background using DNA fonts and colors.

### Figma Import Workflow
1.  **Initialize:** `ray-studio figma init "New Campaign"`
2.  **Connect:** Ensure Figma plugin is running and get Channel ID.
3.  **Scan:** `ray-studio figma scan-text <frame_node_id> --channel <id>`
4.  **Update:** Use `set-text` to populate Figma templates with content generated by Promethia/LLM.

```bash
# Update headline in Figma
ray-studio figma set-text "Frame 1/Headline" "New AI Headline" --is-path --channel 12345
```

### Promethia Integration
Ray Studio acts as the visual production engine within Promethia.
- **Input:** Brief from Iris/Nina (Strategy Agents).
- **Process:**
    1.  Selects best template based on brief.
    2.  Generates copy (Headline/CTA).
    3.  Calls `ray-studio generate`.
- **Output:** Final assets ready for publishing.
