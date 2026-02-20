# Arquitetura do Projeto CaloriSense

Este projeto foi refatorado seguindo os princípios da **Clean Architecture** (Arquitetura Limpa) para garantir a separação de responsabilidades, testabilidade e manutenção.

## Estrutura de Diretórios

```
src/
├── core/           # Configurações globais (variáveis de ambiente, constantes)
├── domain/         # Regras de Negócio Enterprise (Entidades e Modelos)
├── ports/          # Interfaces (Abstrações) para serviços externos (Inversão de Dependência)
├── use_cases/      # Regras de Negócio da Aplicação (Orquestração)
├── adapters/       # Implementações concretas das Interfaces (Infrastructure)
└── api/            # Camada de Interface com o Usuário (Framework Web)
```

## Detalhes das Camadas

1.  **Domain (`src/domain`)**:
    *   Contém os modelos Pydantic (`FoodAnalysisResult`, `FoodItem`, etc.) que representam os dados centrais da aplicação.
    *   Não depende de nenhuma outra camada externa.

2.  **Ports (`src/ports`)**:
    *   Define interfaces (Abstract Base Classes) como `LLMPort`.
    *   Permite que a aplicação core (Use Cases) não dependa de implementações concretas (como OpenRouter ou OpenAI), mas sim de abstrações.

3.  **Use Cases (`src/use_cases`)**:
    *   Contém a lógica da aplicação, como `AnalyzeFoodUseCase`.
    *   Coordena o fluxo de dados: recebe o input, chama o provedor de IA (via porta), e retorna o resultado formatado.

4.  **Adapters (`src/adapters`)**:
    *   Contém a implementação real das interfaces definidas em `ports`.
    *   Exemplo: `OpenRouterAdapter` implementa `LLMPort` usando a biblioteca `httpx` para fazer chamadas HTTP reais.

5.  **API (`src/api`)**:
    *   Definição das rotas FastAPI.
    *   Responsável apenas por receber a requisição HTTP, instanciar o Use Case (com injeção de dependência) e retornar a resposta.

6.  **Core (`src/core`)**:
    *   Configurações centrais como chaves de API e URLs.

## Fluxo de Execução

1.  O cliente chama `POST /analisar-prato-url/`.
2.  O **Controller** (`src/api/routes.py`) recebe a requisição.
3.  O Controller instancia o **AnalyzeFoodUseCase**, injetando o **OpenRouterAdapter**.
4.  O **Use Case** executa a lógica de análise chamando `analyze_food_image` no adaptador.
5.  O **Adapter** faz a requisição externa para a OpenRouter e retorna os dados brutos.
6.  O Adapter converte os dados brutos para a Entidade de Domínio `FoodAnalysisResult`.
7.  O resultado volta pelo Use Case até a API, que retorna o JSON para o cliente.
