import time
from typing import List

from articles.domain.entities import Article
from backbone.infrastructure.log._logger import Logger
from constant import Language
from unit_of_work import UnitOfWork
from utils.public.translator import Translator


def _fetch_article_language_en(page_size, page_number, uow):
    offset = (page_number - 1) * page_size
    article = uow.session.query(Article).order_by(Article.id).where(Article.language_id == Language.EN.value).limit(
        page_size) \
        .offset(offset).all()
    return article


def _translate_content_article(article: Article) -> Article:
    text = Translator.translating_long_text(article.content_of_article)
    article.content_of_article = text
    article.language_id = Language.FA.value
    return article


def _get_articles_and_translating_long_text(uow: UnitOfWork) -> List[Article]:
    page_number = 1
    page_size = 10
    articles_obj = []
    while True:
        articles = _fetch_article_language_en(page_size=page_size, page_number=page_number, uow=uow)
        if not articles:
            break
        page_number += 1

        for article in articles:
            article = _translate_content_article(article)
            articles_obj.append(article)

    return articles_obj


def article_translate_to_fa_worker():
    uow = UnitOfWork()
    while True:
        try:
            with uow:
                articles = _get_articles_and_translating_long_text(uow)
                print(articles)
                if articles:
                    uow.session.bulk_save_objects(articles)
                    uow.commit()
            time.sleep(300)
        except Exception as e:
            Logger.info(e)
            uow.session.rollback()
            uow.session.close()
            time.sleep(300)
