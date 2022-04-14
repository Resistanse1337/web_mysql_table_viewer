from enum import Enum
from pydantic import BaseModel


class ColumnsEnum(Enum):
    name = "name"
    quantity = "quantity"
    distance = "distance"
    date = "date"


class OrderEnum(Enum):
    desc = "DESC"
    asc = "ASC"


class WhereConditionsEnum(Enum):
    less = "<"
    more = ">"
    equal = "="
    contains = "LIKE"


class UsersTableSortParams(BaseModel):
    column_to_order: ColumnsEnum = None
    order_value: OrderEnum = None
    column_to_where: ColumnsEnum = None
    where_condition: WhereConditionsEnum = None
    where_value: str = None
    page_num: int = 1


if __name__ == "__main__":
    print([i.name for i in ColumnsEnum])





