from typing import Any, Optional


class Pagination:

    def __init__(self, page, per_page, total, items: Optional[Any]):
        self.page = page
        self.per_page = per_page
        self.total = total
        self.items = items
        self.pages = self.total // self.per_page + 1

    def to_dict(self):
        return {
            "page": self.page,
            "per_page": self.per_page,
            "total": self.total,
            "pages": self.pages,
            "items": self.items
        }