from articles.domain.entities import Article, File
from articles.spider.dto.article import ArticlePageDTO, ArticleDTO
from articles.spider.service.make_list_article_author import make_group_article_author
from articles.spider.service.make_list_authors import make_group_authors
from articles.spider.service.make_list_issn import make_group_issn
from articles.spider.service.make_list_keyword import make_group_keyword
from unit_of_work import UnitOfWork


def create_article_and_dependencies(detail_page: ArticlePageDTO):
    with UnitOfWork() as uow:
        list_object_entities = []
        authors = make_group_authors(detail_page, uow)
        issn = make_group_issn(detail_page)
        keyword = make_group_keyword(detail_page)

        list_object_entities.extend(authors)
        list_object_entities.extend(issn)
        list_object_entities.extend(keyword)

        file = File.create(source=detail_page.uuid, path=detail_page.path, format="pdf")
        article_dto = ArticleDTO.add(detail_page, authors=authors)
        article = Article.create(article_dto,
                                 format="pdf")
        list_object_entities.append(file)
        list_object_entities.append(article)
        uow.session.add_all(list_object_entities)
        uow.commit()

    with UnitOfWork() as uow:
        list_object_entities = []
        article_authors = make_group_article_author(authors, detail_page)
        list_object_entities.extend(article_authors)
        uow.session.bulk_save_objects(list_object_entities)

        uow.commit()

    pass
