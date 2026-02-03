from .formats import ExportConfig, ImageFormat, ColorSpace

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
