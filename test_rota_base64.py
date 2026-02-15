import httpx
import asyncio
import os
import json

async def main():
    # URL do servidor
    url_servidor = "http://127.0.0.1:8000/analisar-prato/"
    
    # Nome do arquivo local
    arquivo_local = "plato.jpeg"

    if not os.path.exists(arquivo_local):
        print(f"Erro: Arquivo '{arquivo_local}' não encontrado.")
        return

    print(f"--- Testando Rota de Upload (Base64) ---")
    print(f"Enviando arquivo: {arquivo_local}")
    print(f"Para: {url_servidor}")
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            # Enviando o arquivo via multipart/form-data
            # A chave 'imagem' deve corresponder ao nome do parâmetro no FastAPI
            files = {'imagem': open(arquivo_local, 'rb')}
            
            response = await client.post(url_servidor, files=files)
            
            if response.status_code == 200:
                print("\n✅ Sucesso! Resposta do servidor:")
                dados = response.json()
                print(json.dumps(dados, indent=2, ensure_ascii=False))
            else:
                print(f"\n❌ Erro {response.status_code}:")
                print(response.text)
                
    except Exception as e:
        print(f"\n❌ Erro de conexão: {e}")

if __name__ == "__main__":
    asyncio.run(main())
