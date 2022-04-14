import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from db import UsersDb
from models import UsersTableSortParams, ColumnsEnum, WhereConditionsEnum


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request, "fieldnames": [f.name for f in ColumnsEnum],
                                       "conditions": [f.value for f in WhereConditionsEnum]})


@app.post("/get_data")
def get_data(data: UsersTableSortParams):
    users_db = UsersDb()
    data = users_db.get_sorted(
        column_to_order=data.column_to_order.value, order_value=data.order_value.value,
        column_to_where=data.column_to_where.value, where_condition=data.where_condition.value,
        where_value=data.where_value, offset=users_db.one_page * (data.page_num-1)
    )
    pages_count = users_db.count()
    users_db.close_connection()

    return JSONResponse(content={"users": data, "total_pages": pages_count, "per_one_page": users_db.one_page})


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)




