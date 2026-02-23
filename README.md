# 🍽️ CaloriSense API

API REST para análise nutricional de pratos via visão computacional com IA. O serviço recebe uma imagem de um prato de comida (por upload de arquivo, URL pública ou Base64) e retorna estimativas de calorias e macronutrientes estruturadas em JSON.

O projeto foi construído com **FastAPI** seguindo os princípios de **Clean Architecture**, garantindo separação de responsabilidades, testabilidade e facilidade de manutenção.

---

## 🏛️ Arquitetura

O projeto segue a **Arquitetura Limpa (Clean Architecture)**, dividida nas seguintes camadas:

```
src/
├── core/        # Configurações globais (variáveis de ambiente, constantes)
├── domain/      # Entidades e Modelos Pydantic (regras de negócio)
├── ports/       # Interfaces abstratas (Inversão de Dependência)
├── use_cases/   # Orquestração da lógica de negócio
├── adapters/    # Implementações concretas (OpenRouter/LLM)
└── api/         # Rotas FastAPI (camada de interface)
```

> Para mais detalhes, consulte o arquivo [`ARCHITECTURE.md`](./ARCHITECTURE.md).

---

## 🤖 Modelo de IA

- **Provedor:** [OpenRouter](https://openrouter.ai/)
- **Modelo:** `google/gemini-3-flash-preview`

---

## 📋 Pré-requisitos

- Python **3.10+**
- Conta na [OpenRouter](https://openrouter.ai/) com uma chave de API válida

---

## ⚙️ Instalação

**1. Clone o repositório e entre na pasta:**
```bash
git clone <url-do-repositorio>
cd PythonProject
```

**2. (Recomendado) Crie e ative um ambiente virtual:**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
```

**3. Instale as dependências:**
```bash
pip install fastapi uvicorn httpx python-multipart python-dotenv pydantic
```

**4. Configure as variáveis de ambiente:**

Crie um arquivo `.env` na raiz do projeto:
```env
OPENROUTER_API_KEY=sua_chave_aqui
```

---

## 🚀 Executando o Servidor

```bash
uvicorn main:app --reload --port 8000
```

O servidor estará disponível em `http://127.0.0.1:8000`.

A documentação interativa (Swagger UI) pode ser acessada em `http://127.0.0.1:8000/docs`.

---

## 📡 Endpoints

### `POST /analisar-prato-arquivo/`
Recebe um arquivo de imagem via `multipart/form-data`. O servidor converte a imagem para Base64 internamente antes de enviar para a IA.

**Content-Type:** `multipart/form-data`

| Campo    | Tipo   | Descrição                         |
|----------|--------|-----------------------------------|
| `imagem` | `File` | Arquivo de imagem (JPEG, PNG...) |

**Teste:**
```bash
python test_rota_base64.py
```

---

### `POST /analisar-prato-url/`
Recebe um objeto JSON com a URL pública de uma imagem. A URL é enviada diretamente para a IA sem download intermediário.

**Content-Type:** `application/json`

```json
{
  "image_url": "https://upload.wikimedia.org/wikipedia/commons/..."
}
```

**Teste:**
```bash
python test_rota_url.py
```

---

### `POST /analisar-prato-base64/`
Recebe um objeto JSON com a string Base64 da imagem. Aceita tanto Base64 puro quanto o formato Data URL completo (`data:image/jpeg;base64,...`).

**Content-Type:** `application/json`

```json
{
  "image_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

> Se a string não começar com `data:`, o sistema adiciona automaticamente o prefixo `data:image/jpeg;base64,`.

**Teste:**
```bash
python test_rota_base64_string.py
```

---

## 📦 Estrutura da Resposta (JSON)

Todos os endpoints retornam o mesmo modelo `FoodAnalysisResult`:

```json
{
  "prato_geral": "Frango grelhado com arroz e salada",
  "itens": [
    {
      "alimento": "Frango grelhado",
      "preparo": "Grelhado sem pele",
      "porcao_visual": "1 filé médio",
      "peso_estimado_g": 150.0,
      "confianca": "alta"
    }
  ],
  "calorias_estimadas": {
    "min": 420.0,
    "max": 580.0
  },
  "confianca_geral": 0.85,
  "informacoes_faltantes": ["quantidade exata de azeite utilizado"]
}
```

| Campo                  | Tipo     | Descrição                                              |
|------------------------|----------|--------------------------------------------------------|
| `prato_geral`          | `string` | Descrição geral do prato identificado                  |
| `itens`                | `array`  | Lista de alimentos individuais identificados           |
| `calorias_estimadas`   | `object` | Faixa calórica (`min` e `max`) em kcal                |
| `confianca_geral`      | `float`  | Confiança geral da análise (0.0 a 1.0)                |
| `informacoes_faltantes`| `array`  | Informações que limitaram a precisão da estimativa     |

---

## 🧪 Scripts de Teste

| Script                       | Rota Testada                  | Método de Envio          |
|------------------------------|-------------------------------|--------------------------|
| `test_rota_base64.py`        | `/analisar-prato-arquivo/`    | Upload de arquivo local  |
| `test_rota_url.py`           | `/analisar-prato-url/`        | URL pública da imagem    |
| `test_rota_base64_string.py` | `/analisar-prato-base64/`     | String Base64 no JSON    |

> Certifique-se de que o servidor está rodando antes de executar qualquer script.

---

## 📁 Arquivos do Projeto

```
.
├── main.py                      # Ponto de entrada da aplicação FastAPI
├── src/
│   ├── core/config.py           # Configurações e variáveis de ambiente
│   ├── domain/models.py         # Modelos Pydantic (Entidades)
│   ├── ports/llm_port.py        # Interface abstrata para o LLM
│   ├── use_cases/analyze_food.py# Caso de uso principal
│   ├── adapters/openrouter_adapter.py # Integração com a OpenRouter
│   └── api/routes.py            # Definição das rotas FastAPI
├── test_rota_base64.py          # Teste: upload de arquivo
├── test_rota_base64_string.py   # Teste: envio por Base64 string
├── test_rota_url.py             # Teste: envio por URL
├── ARCHITECTURE.md              # Documentação da arquitetura
├── .env                         # Variáveis de ambiente (não versionado)
└── .gitignore
```

---

## 🔒 Segurança

- **Nunca** suba o arquivo `.env` para o repositório. Ele já está incluído no `.gitignore`.
- Em produção, utilize um gerenciador de segredos adequado (ex: AWS Secrets Manager, Azure Key Vault).
