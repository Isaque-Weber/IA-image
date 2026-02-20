from pydantic import BaseModel
from typing import List, Optional

# --- Input Models ---
class ImageUrlRequest(BaseModel):
    image_url: str

class ImageBase64Request(BaseModel):
    image_base64: str

# --- Output Models (Entities) ---
class FoodItem(BaseModel):
    alimento: str
    preparo: str
    porcao_visual: str
    peso_estimado_g: float
    confianca: str  # "alta", "media", "baixa"

class CaloriesRange(BaseModel):
    min: float
    max: float

class FoodAnalysisResult(BaseModel):
    prato_geral: str
    itens: List[FoodItem]
    calorias_estimadas: CaloriesRange
    confianca_geral: float
    informacoes_faltantes: List[str]
