import dataclasses
from typing import Optional, List
from uuid import UUID
from itertools import product


@dataclasses.dataclass
class DetailKeyword:
    type: Optional[str]
    keyword: Optional[str]

@dataclasses.dataclass
class DetailAuthors:
    id: Optional[int]
    firstName: Optional[str]
    lastName: Optional[str]
    affiliation: Optional[str]
    bio: Optional[str]
    orcid: Optional[str]


@dataclasses.dataclass
class DetailIssn:
    article_id: Optional[UUID]
    format: Optional[str]
    value: Optional[str]


@dataclasses.dataclass
class DetailPage:
    uuid: Optional[UUID]
    title: Optional[str]
    link_article: Optional[str]
    article_text: Optional[str]
    displayPublicationTitle: Optional[str]
    abstract: Optional[str]
    publicationDate: Optional[str]
    fundingName: Optional[str]
    confLoc: Optional[str]
    publisher: Optional[str]
    insertDate: Optional[str]
    articleId: Optional[int]
    volume: Optional[int]
    issue: Optional[int]
    authors: List[DetailAuthors] = dataclasses.field(default_factory=list)
    issn: List[DetailIssn] = dataclasses.field(default_factory=list)
    keywords: List[DetailKeyword] = dataclasses.field(default_factory=list)
