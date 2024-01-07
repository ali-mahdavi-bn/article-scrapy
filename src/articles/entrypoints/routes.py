from fastapi import APIRouter

from articles.bootstrap import bootstrap
from articles.service_layer.query.view.get_article import view_get_article

router = APIRouter(prefix="/account", tags=["account"])
bus = bootstrap()


@router.get("/{language:str}/article/{article_id:str}")
def get_article(language: str, article_id: str):
    return view_get_article(language=language, article_id=article_id, uow=bus.uow)
