import uvicorn
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import providers as main_providers
from src.routes.routes import bank_route, office_route, user_route
from src.services.providers import ServiceProvider


def create_app() -> FastAPI:
    app = FastAPI(debug=True, title="Specification Subject")
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
    app.include_router(bank_route)
    app.include_router(office_route)
    app.include_router(user_route)

    container = make_async_container(
        main_providers.DbSettingProvider(),
        main_providers.AsyncDatabaseProvider(),
        ServiceProvider(),
    )
    setup_dishka(container, app)
    return app


if __name__ == "__main__":
    uvicorn.run(create_app(), host="0.0.0.0", port=8001)
