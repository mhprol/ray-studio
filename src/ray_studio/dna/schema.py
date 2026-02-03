from pydantic import BaseModel
from typing import List, Optional

class Colors(BaseModel):
    primary: str
    secondary: str
    accent: str
    background: str
    text: str

class Fonts(BaseModel):
    heading: str
    body: str
    accent: str

class Logo(BaseModel):
    primary: str
    white: Optional[str] = None
    icon: Optional[str] = None

class BrandIdentity(BaseModel):
    name: str
    tagline: str
    colors: Colors
    fonts: Fonts
    tone: str
    expression: str
    logo: Logo

class Audience(BaseModel):
    description: str
    pain_points: List[str]
    desires: List[str]

class Product(BaseModel):
    name: str
    description: str
    image: str
    price: Optional[str] = None

class ContentStrategy(BaseModel):
    hashtags: List[str]
    cta_phrases: List[str]

class BrandDNA(BaseModel):
    brand: BrandIdentity
    audience: Audience
    products: List[Product]
    content: ContentStrategy
