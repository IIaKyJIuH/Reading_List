from enum import StrEnum


class KindEnum(StrEnum):
    BOOK = "book"
    ARTICLE = "article"


class StatusEnum(StrEnum):
    PLANNED = "planned"
    READING = "reading"
    DONE = "done"


class PriorityEnum(StrEnum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


class ItemSorting(StrEnum):
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    PRIORITY = "priority"
