from articles.adapter import data_models
from articles.domain import entities
from backbone.adapter.abstract_data_model import MAPPER_REGISTRY


def start_mapper():
    MAPPER_REGISTRY.map_imperatively(entities.Article, data_models.article_table)
    MAPPER_REGISTRY.map_imperatively(entities.File, data_models.file_table)
    MAPPER_REGISTRY.map_imperatively(entities.Author, data_models.author_table)
    MAPPER_REGISTRY.map_imperatively(entities.ArticleAuthorAssociation,
                                     data_models.article_author_association_table)
    MAPPER_REGISTRY.map_imperatively(entities.Enumeration, data_models.enumeration_table)
    MAPPER_REGISTRY.map_imperatively(entities.Issn, data_models.issn_table)
    MAPPER_REGISTRY.map_imperatively(entities.Keyword, data_models.keyword_table)
    MAPPER_REGISTRY.map_imperatively(entities.Language, data_models.language_table)
