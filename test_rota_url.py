import httpx
import asyncio
import json

async def main():
    # URL do servidor
    url_servidor = "http://127.0.0.1:8000/analisar-prato-url/"
    
    # URL publica para envio
    url_publica = "https://upload.wikimedia.org/wikipedia/commons/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg"
    
    print(f"--- Testando Rota de URL (Direta) ---")
    print(f"Enviando URL: {url_publica}")
    print(f"Para: {url_servidor}")
    
    # Payload no formato JSON
    payload = {
        "image_url": url_publica
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url_servidor, json=payload)
            
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
