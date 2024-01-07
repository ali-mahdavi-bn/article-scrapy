import time
from typing import List
from uuid import uuid4

from articles.domain.entities.author import Author
from articles.spider.dto.article import ArticlePageDTO, DetailAuthors
from unit_of_work import UnitOfWork


def make_group_authors(detail_page_ieee: ArticlePageDTO, uow: UnitOfWork) -> List[Author]:
    authors = detail_page_ieee.authors
    if not authors:
        return []

    author_list = generate_author_list(authors=authors, uow=uow)

    return author_list


def generate_author_list(authors: List[DetailAuthors], uow):
    author_list = []
    for author_data in authors:
        author = uow.author.find_by_authors_id(author_data.id)

        if not author:
            author = create_author_entity(author_data)

        author_list.append(author)

    return author_list


def create_author_entity(author_data):
    author = Author()
    author.uuid = uuid4()
    author.authors_id = author_data.id
    author.first_name = author_data.firstName
    author.last_name = author_data.lastName
    author.affiliation = author_data.affiliation

    bio = author_data.bio
    if bio is not None:
        author.bio = bio

    return author
