from articles.domain.entities import Article, Language, ArticleAuthorAssociation
from unit_of_work import UnitOfWork


def view_all_article(language, author_id, pagination, start_page, end_page, uow: UnitOfWork):
    with uow:
        # get all article with language
        lan = uow.session.query(Language).filter(Language.name == language).first()
        article = uow.session.query(Article).filter(
            Article.language_id == lan.id)

        # filter
        if author_id:
            article_authors_association = uow.session.query(ArticleAuthorAssociation.article_id).filter(
                ArticleAuthorAssociation.author_id == author_id).all()
            uuid_authors = (article_author_association[0] for article_author_association in article_authors_association)
            article = article.filter(Article.uuid.in_(uuid_authors))

        if start_page:
            article = article.filter(Article.start_page >= start_page)
        if end_page:
            article = article.filter(Article.end_page <= end_page)

        # pagination
        article = article.order_by(
            pagination.sql_order_by(Article)).limit(pagination.limit).offset(pagination.offset).all()

        return article
