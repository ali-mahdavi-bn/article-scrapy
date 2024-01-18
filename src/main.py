from contextlib import asynccontextmanager

from fastapi import FastAPI

from articles.domain.mapper import start_mapper as article_mapper
from articles.entrypoints.routes import router as article_route
from backbone.adapter.abstract_data_model import MAPPER_REGISTRY
from backbone.infrastructure.databases.postgres_connection import DEFAULT_ENGIN


@asynccontextmanager
async def lifespan(app: FastAPI):
    article_mapper()
    MAPPER_REGISTRY.metadata.create_all(DEFAULT_ENGIN)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(article_route)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
