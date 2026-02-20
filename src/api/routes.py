from fastapi import APIRouter, File, UploadFile, Depends
import base64
from src.domain.models import ImageUrlRequest, ImageBase64Request, FoodAnalysisResult
from src.adapters.openrouter_adapter import OpenRouterAdapter
from src.use_cases.analyze_food import AnalyzeFoodUseCase

router = APIRouter()

# Dependency Injection Helper (Manual for now, could be framework-based)
def get_analyze_food_use_case() -> AnalyzeFoodUseCase:
    adapter = OpenRouterAdapter()
    return AnalyzeFoodUseCase(adapter)

@router.post("/analisar-prato-arquivo/", response_model=FoodAnalysisResult)
async def analisar_prato_arquivo(
    imagem: UploadFile = File(...),
    use_case: AnalyzeFoodUseCase = Depends(get_analyze_food_use_case)
):
    image_bytes = await imagem.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    mime_type = imagem.content_type or "image/jpeg"
    image_data_url = f"data:{mime_type};base64,{base64_image}"
    
    return await use_case.execute(image_data_url)

@router.post("/analisar-prato-url/", response_model=FoodAnalysisResult)
async def analisar_prato_url(
    request: ImageUrlRequest,
    use_case: AnalyzeFoodUseCase = Depends(get_analyze_food_use_case)
):
    return await use_case.execute(request.image_url)

@router.post("/analisar-prato-base64/", response_model=FoodAnalysisResult)
async def analisar_prato_base64(
    request: ImageBase64Request,
    use_case: AnalyzeFoodUseCase = Depends(get_analyze_food_use_case)
):
    if not request.image_base64.startswith("data:"):
         # Default logic
         image_data_url = f"data:image/jpeg;base64,{request.image_base64}"
    else:
        image_data_url = request.image_base64
        
    return await use_case.execute(image_data_url)
