from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any, Optional, Union

class Layout(BaseModel):
    type: str = "stack"  # stack, grid, overlay, split
    direction: Optional[str] = "vertical"
    padding: Optional[int] = 0

class Layer(BaseModel):
    type: str # background, logo, text, cta_button
    source: Optional[str] = None
    content: Optional[str] = None
    prompt_template: Optional[str] = None
    position: Optional[str] = None
    size: Optional[Union[int, List[Union[int, str]]]] = None
    margin: Optional[int] = 0
    margin_top: Optional[int] = 0
    margin_bottom: Optional[int] = 0
    padding: Optional[Union[int, List[int]]] = None
    font: Optional[str] = None
    color: Optional[str] = None
    background: Optional[str] = None
    max_width: Optional[Union[str, int]] = None
    border_radius: Optional[int] = 0
    # Allow extra fields for flexibility
    model_config = ConfigDict(extra="allow")

class InputDefinition(BaseModel):
    type: str
    required: bool = True
    example: Optional[str] = None
    default: Optional[Any] = None

class Template(BaseModel):
    name: str
    description: str
    category: str
    layout: Layout
    layers: List[Layer]
    inputs: Dict[str, InputDefinition]
