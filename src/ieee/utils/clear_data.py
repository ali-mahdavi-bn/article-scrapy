import json
from uuid import uuid4

from ieee.domain.detail import DetailPage, DetailAuthors, DetailIssn, DetailKeyword


def clear_data_ieee(response, article_text) -> DetailPage:
    second_script_content = response.css('script:nth-of-type(5)::text').get()
    link_article = response.url
    content = extract_data(second_script_content)
    return process_usable_data(content=content, link_article=link_article, article_text=article_text)


def extract_data(content: str) -> str:
    start_index = content.find('={')
    return content[start_index:]


def process_usable_data(content: str, link_article: str, article_text: str) -> DetailPage:
    data = json.loads(content[1:].strip()[:-1])
    uuid = uuid4()
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
            article_id=uuid,
            format=issn.get("format"),
            value=issn.get("value"))
        for issn in data.get("issn", [])]

    keyword = [
        DetailKeyword(type=keyword.get("type"), keyword=kwd)
        for keyword in data.get("keywords", [])
        for kwd in keyword.get("kwd", [])
    ]
    detail_page = DetailPage(
        uuid=uuid,
        title=data.get("title"),
        link_article=link_article,
        article_text=article_text,
        displayPublicationTitle=data.get("displayPublicationTitle"),
        abstract=data.get("abstract"),
        publicationDate=data.get("publicationDate"),
        fundingName=data.get("fundingName"),
        confLoc=data.get("confLoc"),
        volume=data.get("volume"),
        issue=data.get("issue"),
        articleId=data.get("articleId"),
        insertDate=data.get("insertDate"),
        publisher=data.get("publisher"),
        authors=authors,
        issn=issn,
        keywords=keyword,
    )

    return detail_page
