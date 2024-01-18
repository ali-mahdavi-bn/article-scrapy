from articles.domain.entities import Article, Language
from unit_of_work import UnitOfWork


def view_get_article(language, article_id, uow: UnitOfWork):
    with uow:
        # get an article with uuid and  language
        lan = uow.session.query(Language).filter(Language.name == language).first()
        article = uow.session.query(Article).filter(Article.uuid == article_id,
                                                    Article.language_id == lan.id).all()
        return article
