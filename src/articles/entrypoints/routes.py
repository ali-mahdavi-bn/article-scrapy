from uuid import UUID

from fastapi import APIRouter

from articles.bootstrap import bootstrap
from articles.service_layer.query.view.get_all_article import view_all_article
from articles.service_layer.query.view.get_article import view_get_article
from backbone.api.dependencies import PaginateParam

router = APIRouter(prefix="/account", tags=["account"])
bus = bootstrap()
from fastapi import Depends


@router.get("/{language:str}/article/{article_id:str}")
def get_article(language: str, article_id: str):
    return view_get_article(language=language, article_id=article_id, uow=bus.uow)


@router.get("/{language:str}/article/")
def get_article(language: str, pagination=Depends(PaginateParam), author_id: UUID = None, start_page: int = None,
                end_page: int = None):
    return view_all_article(language=language, pagination=pagination,
                            author_id=author_id, start_page=start_page, end_page=end_page,
                            uow=bus.uow)
