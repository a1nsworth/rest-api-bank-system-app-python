import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.bank import bank_route, office_route

app = FastAPI(debug=True, title="Specification Subject")
app.include_router(bank_route)
app.include_router(office_route)

origins = (
    "http://0.0.0.0",
    "http://0.0.0.0:8001",
    "http://localhost",
    "http://localhost:8001",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app)
