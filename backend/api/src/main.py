from fastapi import FastAPI, Request
import uvicorn

from receptionata import receptionata_router

app = FastAPI()
app.include_router(receptionata_router, prefix="/receptionata")

# Global variable to store the last request
last_request = None

# For debugging purposes - logging of all incoming requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    global last_request
    last_request = f"Incoming request: {request.method} {request.url}"
    print(last_request)
    response = await call_next(request)
    return response

@app.get("/last_request")
async def get_last_request():
    return {"last_request": last_request}

def main():
    uvicorn.run(
        app=app,
        loop="uvloop",
        port=8080,
        host="0.0.0.0",
    )

if __name__ == "__main__":
    main()
