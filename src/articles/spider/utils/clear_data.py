import json
from uuid import uuid4

from articles.spider.dto.article import ArticlePageDTO, DetailAuthors, DetailIssn, DetailKeyword
from articles.spider.utils.file import save_file_in_minio
from crawl.backbon.helpers.response import Response


def clear_data_ieee(response: Response, article_text="") -> ArticlePageDTO:
    second_script_content = response.css('script:nth-of-type(5)::text').get()
    link_article = response.url
    content = extract_data(second_script_content)
    return process_data(content=content, link_article=link_article, content_of_article=article_text, response=response)


def extract_data(content: str) -> str:
    start_index = content.find('={') if content else 0
    return content[start_index:] if start_index else ""


def process_data(content: str, link_article: str, content_of_article: str, response) -> ArticlePageDTO:
    data = json.loads(content[1:].strip()[:-1])
    uuid_article = uuid4()
    uuid_file = uuid4()
    authors = [
        DetailAuthors(
            id=author.get("id"),
            firstName=author.get("firstName"),
            lastName=author.get("lastName"),
            orcid=author.get("orcid"),
            bio=((author.get("bio")).get("p"))[0] if author.get("bio") else "",
            affiliation=(author.get("affiliation"))[0]
        )
        for author in data.get("authors", [])
    ]
    issn = [
        DetailIssn(
            article_id=uuid_article,
            format=issn.get("format"),
            value=issn.get("value"))
        for issn in data.get("issn", [])]

    keyword = [
        DetailKeyword(type=keyword.get("type"), keyword=kwd)
        for keyword in data.get("keywords", [])
        for kwd in keyword.get("kwd", [])
    ]

    path_minio = save_file_in_minio(response=response)
    detail_page = ArticlePageDTO(
        uuid=uuid_article,
        title=data.get("title"),
        path=path_minio,
        date_of_conference=data.get("displayPublicationDate"),
        link_article=link_article,
        content_of_article=content_of_article,
        published_in=data.get("displayPublicationTitle"),
        start_page=data.get("startPage"),
        end_page=data.get("end_page"),
        abstract=data.get("abstract"),
        publication_date=data.get("publicationDate"),
        conf_loc=data.get("confLoc"),
        article_id=data.get("articleId"),
        insert_date=data.get("insertDate"),
        publisher=data.get("publisher"),
        authors=authors,
        issn=issn,
        doi=data.get("doi"),
        keywords=keyword,
    )

    return detail_page
