from fastapi import FastAPI
# To create Database to trace the models
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

@app.get("/")
# def read_root():
def index():
    return {"Msg": "Hello World"}

register_tortoise(
    app,
    # db_url="sqlite://db.sqlite3",
    db_url="sqlite://database.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)