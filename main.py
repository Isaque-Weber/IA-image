from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import httpx
import json
import re
import base64

app = FastAPI()
OPENROUTER_KEY = "api_key"

# Modelo para o endpoint que recebe URL
class ImageRequest(BaseModel):
    image_url: str

# ROTA 1: Upload de imagem local (Processa para Base64)
@app.post("/analisar-prato/")
async def analisar_prato(imagem: UploadFile = File(...)):
    # 1. Ler a imagem e converter para Base64
    image_bytes = await imagem.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    
    # Determinar o media type (mime type)
    mime_type = imagem.content_type or "image/jpeg"
    image_data_url = f"data:{mime_type};base64,{base64_image}"

    # Prompt unificado
    prompt = get_prompt()

    payload = {
        "model": "google/gemini-3-flash-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_data_url}}
                ]
            }
        ]
    }

    return await call_openrouter(payload)


# ROTA 2: Recebe URL pública (Envia URL direta)
@app.post("/analisar-prato-url/")
async def analisar_prato_url(request: ImageRequest):
    # Prompt unificado
    prompt = get_prompt()

    payload = {
        "model": "google/gemini-2.0-flash-001",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": request.image_url}}
                ]
            }
        ]
    }

    return await call_openrouter(payload)


def get_prompt():
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

async def call_openrouter(payload):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000", 
        "X-Title": "CaloriSense API"
    }

    timeout = httpx.Timeout(60.0, connect=10.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Falha na requisição OpenRouter: {str(e)}")

    # Extrair e limpar o JSON da resposta
    try:
        content = result['choices'][0]['message']['content']
        content_clean = re.sub(r"```json\s*|\s*```", "", content).strip()
        data = json.loads(content_clean)
        return data
    except (KeyError, json.JSONDecodeError) as e:
        return {
            "erro": "Falha ao processar resposta do modelo", 
            "raw_content": result.get('choices', [{}])[0].get('message', {}).get('content', ''),
            "details": str(e)
        }
