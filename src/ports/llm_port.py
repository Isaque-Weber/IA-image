from abc import ABC, abstractmethod
from src.domain.models import FoodAnalysisResult

class LLMPort(ABC):
    @abstractmethod
    async def analyze_food_image(self, image_input: str) -> FoodAnalysisResult:
        """
        Takes an image input (URL or Base64 Data URI) and returns the analyzed food data.
        """
        pass
