from typing import List
from uuid import uuid4

from ieee.domain.detail import DetailPage, DetailAuthors
from ieee.domain.entities import AuthorEntity
from unit_of_work import UnitOfWork


def make_list_authors(detail_page_ieee: DetailPage, uow: UnitOfWork) -> List[AuthorEntity]:
    authors = detail_page_ieee.authors
    if not authors:
        return []

    author_list = generate_author_list(authors=authors, uow=uow)

    return author_list


def generate_author_list(authors: List[DetailAuthors], uow):
    author_list = []

    for author_data in authors:
        author = uow.author.find_by_authorsId(author_data.id)

        if not author:
            author = create_author_entity(author_data)

        author_list.append(author)

    return author_list


def create_author_entity(author_data):
    author = AuthorEntity()
    author.uuid = uuid4()
    author.authorsId = author_data.id
    author.firstname = author_data.firstName
    author.lastname = author_data.lastName
    author.affiliation = author_data.affiliation

    bio = author_data.bio
    if bio is not None:
        author.bio = bio

    return author
