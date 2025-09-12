from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from uvicorn import run

from app.api import (
    generate_user_id_router, translator_router, show_history_router
)
from app.core import lifespan


def create_app(testing: bool = False) -> FastAPI:
    """Фабрика для создания приложения"""
    app = FastAPI(
        title="Translator-ULTRA",
        default_response_class=ORJSONResponse,
        lifespan=lifespan
    )

    if testing:
        app.state.testing = True

    app.include_router(generate_user_id_router)
    app.include_router(translator_router)
    app.include_router(show_history_router)

    return app


app = create_app()


if __name__ == '__main__':
    run(
        app="app.main:app", port=8000, host="127.0.0.1",
        reload=False, use_colors=True
    )
