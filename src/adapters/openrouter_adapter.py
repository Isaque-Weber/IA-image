import httpx
import json
import re
from fastapi import HTTPException
from src.ports.llm_port import LLMPort
from src.domain.models import FoodAnalysisResult, FoodItem, CaloriesRange
from src.core.config import settings

class OpenRouterAdapter(LLMPort):
    def _get_prompt(self):
        return """
        Analise esta imagem de comida e retorne um JSON com a estimativa nutricional.
        O formato deve ser EXATAMENTE este:
        {
          "prato_geral": "Descrição do prato",
          "itens": [
            {
              "alimento": "Nome do alimento",
              "preparo": "Detalhes do preparo",
              "porcao_visual": "Estimativa visual",
              "peso_estimado_g": 0,
              "confianca": "alta/media/baixa"
            }
          ],
          "calorias_estimadas": { "min": 0, "max": 0 },
          "confianca_geral": 0.0, # 0 a 1
          "informacoes_faltantes": []
        }
        """

    async def analyze_food_image(self, image_input: str) -> FoodAnalysisResult:
        # print(f"DEBUG: Analyzing image input: {image_input[:50]}...") 
        prompt = self._get_prompt()
        
        # O usuário solicitou explicitamente testar o envio DIRETO da URL
        # sem processamento local, para evitar a latência de download/upload do nosso servidor.
        
        payload = {
            "model": settings.MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_input}}
                    ]
                }
            ]
        }

        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000", 
            "X-Title": settings.APP_TITLE
        }

        timeout = httpx.Timeout(60.0, connect=10.0)

        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.post(
                    settings.OPENROUTER_URL,
                    headers=headers,
                    json=payload
                )
                if response.status_code != 200:
                    error_detail = await response.aread()
                    print(f"OpenRouter Error: {error_detail.decode('utf-8')}") # Log para o terminal
                    raise HTTPException(status_code=response.status_code, detail=f"OpenRouter Error: {error_detail.decode('utf-8')}")
                
                result = response.json()
            except httpx.HTTPError as e:
                # O HTTPException acima já vai capturar os status codes de erro
                if isinstance(e, HTTPException):
                    raise e
                raise HTTPException(status_code=500, detail=f"Falha na requisição OpenRouter: {str(e)}")

        # Parse Logic
        try:
            content = result['choices'][0]['message']['content']
            content_clean = re.sub(r"```json\s*|\s*```", "", content).strip()
            data = json.loads(content_clean)
            
            # Validation via Pydantic
            return FoodAnalysisResult(**data)
            
        except (KeyError, json.JSONDecodeError, Exception) as e:
            # Fallback or concise error handling
            raise HTTPException(status_code=500, detail=f"Falha ao processar resposta do modelo: {str(e)}")
