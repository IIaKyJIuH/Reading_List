from enum import IntEnum, StrEnum, auto


class KindEnum(StrEnum):
    BOOK = "book"
    ARTICLE = "article"


class StatusEnum(StrEnum):
    PLANNED = "planned"
    READING = "reading"
    DONE = "done"


class PriorityEnum(IntEnum):
    LOW = auto()
    NORMAL = auto()
    HIGH = auto()


class ItemSorting(StrEnum):
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    PRIORITY = "priority"
