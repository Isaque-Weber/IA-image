import httpx
import asyncio
import base64
import json
import os

async def main():
    # URL do servidor
    url_servidor = "http://127.0.0.1:8000/analisar-prato-base64/"
    
    # Nome do arquivo local para converter e enviar como string
    arquivo_local = "prato-frango.jpg"

    if not os.path.exists(arquivo_local):
        print(f"Erro: Arquivo '{arquivo_local}' não encontrado.")
        return

    print(f"--- Testando Rota de Base64 String ---")
    print(f"Lendo e convertendo arquivo: {arquivo_local}")
    
    with open(arquivo_local, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    # Payload no formato JSON
    payload = {
        "image_base64": encoded_string
    }
    
    print(f"Enviando para: {url_servidor}")
    
    import time
    start_time = time.time()
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url_servidor, json=payload)
            
            end_time = time.time()
            latency = end_time - start_time
            print(f"⏱️ Latência: {latency:.2f} segundos")
            
            if response.status_code == 200:
                print("\n✅ Sucesso! Resposta do servidor:")
                dados = response.json()
                print(json.dumps(dados, indent=2, ensure_ascii=False))
            else:
                print(f"\n❌ Erro {response.status_code}:")
                # print(response.text) # Uncomment if you want to see full error text
                try:
                    print(json.dumps(response.json(), indent=2))
                except:
                    print(response.text)

    except Exception as e:
        print(f"\n❌ Erro de conexão: {e}")

if __name__ == "__main__":
    asyncio.run(main())
