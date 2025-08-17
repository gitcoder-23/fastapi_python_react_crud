from fastapi import FastAPI
# To create Database to trace the models
from tortoise.contrib.fastapi import register_tortoise
from models import (user_pydantic, user_pydanticIn, product_pydantic, product_pydanticIn, supplier_pydantic, supplier_pydanticIn, Supplier, User)
from controllers.supplier_controller import router as supplier_router  # <-- fix
from controllers.user_controller import router as user_router  # <-- fix
from controllers.product_controller import router as product_router  # <-- fix

app = FastAPI()

@app.get("/")
# def read_root():
def index():
    return {"Msg": "Go to /docs for the API documentation"}

# APIS
# Register supplier routes
app.include_router(supplier_router)

# Register user routes
app.include_router(user_router)

# Register Product routes
app.include_router(product_router)

register_tortoise(
    app,
    # db_url="sqlite://db.sqlite3",
    db_url="sqlite://database.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)