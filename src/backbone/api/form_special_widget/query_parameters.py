from typing import List, Union
from uuid import UUID

from fastapi import Query

from backbone.api.dependencies import PaginateParam


class FormSpecialWidgetFilter:
    def __init__(self, title: str = None, ids: List[Union[int, UUID]] = Query(None)):
        self.title = title
        self.ids = ids

    def make_query(self, url: str, pagination: PaginateParam):
        url = url + f"?offset={pagination.offset}&limit={pagination.limit}&sort_by={pagination.sort_by}&order={pagination.order}"
        if url.__contains__("?"):
            if self.title:
                url = url + f"&title={self.title}"
            if self.ids and len(self.ids) > 0:
                for _id in self.ids:
                    url = url + f"&ids={_id}"
        else:
            if self.title:
                url = url + f"?title={self.title}"
                if self.ids and len(self.ids) > 0:
                    for _id in self.ids:
                        url = url + f"&ids={_id}"
            else:
                if self.ids and len(self.ids) > 0:
                    url = url + f"?ids={self.ids.pop()}"
                    for _id in self.ids:
                        url = url + f"&ids={_id}"

        return url
