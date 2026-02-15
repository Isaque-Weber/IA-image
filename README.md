# Projeto de Análise Nutricional de Pratos

Este projeto utiliza a API da OpenRouter (Google Gemini) para analisar imagens de pratos de comida e estimar calorias e macronutrientes.

## Pré-requisitos

- Python 3.10+
- Um arquivo `.env` ou variável de ambiente com `OPENROUTER_KEY` (Opcional, já definido no código para teste).

## Instalação

```bash
pip install fastapi uvicorn httpx python-multipart
```

## Executando o Servidor

Para iniciar o servidor FastAPI, execute o seguinte comando no terminal:

```bash
uvicorn main:app --reload --port 8000
```

O servidor estará rodando em `http://127.0.0.1:8000`.

## Testando as Rotas

### 1. Rota de Upload de Imagem (Processamento Local para Base64)

Esta rota recebe um arquivo de imagem local (`multipart/form-data`), converte para Base64 no servidor e envia para a IA.

**Endpoint:** `POST /analisar-prato/`

**Para testar:**
Execute o script Python de teste:
```bash
python test_rota_base64.py
```
*Certifique-se de que o arquivo `plato.jpeg` existe na mesma pasta.*

### 2. Rota de URL Pública (Envio Direto)

Esta rota recebe um objeto JSON contendo a URL pública da imagem e envia diretamente para a IA.

**Endpoint:** `POST /analisar-prato-url/`

**Payload:**
```json
{
  "image_url": "https://upload.wikimedia.org/wikipedia/commons/..."
}
```

**Para testar:**
Execute o script Python de teste:
```bash
python test_rota_url.py
```

---
**Notas:**
- A chave da API está *hardcoded* no arquivo `main.py` para facilitar os testes iniciais. Em produção, use variáveis de ambiente.
- O modelo utilizado é o `google/gemini-2.0-flash-001`.
