from src.ports.llm_port import LLMPort
from src.domain.models import FoodAnalysisResult

class AnalyzeFoodUseCase:
    def __init__(self, llm_provider: LLMPort):
        self.llm_provider = llm_provider

    async def execute(self, image_input: str) -> FoodAnalysisResult:
        # Here we could adding logging, extra validation, caching, etc.
        return await self.llm_provider.analyze_food_image(image_input)
