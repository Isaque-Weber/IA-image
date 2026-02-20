from fastapi import FastAPI, Request
from src.api.routes import router as food_router
import time

app = FastAPI(title="CaloriSense API Clean Arch")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(f"Rastreador de Latência: {process_time:.4f}s para {request.url.path}")
    return response

app.include_router(food_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
