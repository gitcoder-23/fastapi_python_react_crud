from fastapi import FastAPI
# To create Database to trace the models
from tortoise.contrib.fastapi import register_tortoise
from models import (user_pydantic, user_pydanticIn, product_pydantic, product_pydanticIn, supplier_pydantic, supplier_pydanticIn, Supplier, User)

app = FastAPI()

@app.get("/")
# def read_root():
def index():
    return {"Msg": "Go to /docs for the API documentation"}

# APIS

# @app.get("/users", response_model=List[user_pydantic])
# async def get_users():
#     response = await user_pydantic.from_queryset(User.all())
#     return {'status': 'success', 'data': response}


@app.post("/users")
async def add_user(user_info: user_pydanticIn): # type: ignore
    user_obj = await User.create(**user_info.dict(exclude_unset=True))
    response = await user_pydantic.from_tortoise_orm(user_obj)
    return {'status': 'success', 'data': response}


@app.post("/supplier")
async def add_supplier(supplier_info: supplier_pydanticIn): # type: ignore
    supplier_obj = await Supplier.create(**supplier_info.dict(exclude_unset=True))
    response = await supplier_pydantic.from_tortoise_orm(supplier_obj)
    return {'status': 'success', 'data': response}

@app.get('/supplier')
async def get_all_suppliers():
    response = await supplier_pydantic.from_queryset(Supplier.all())
    return {'status': 'success', 'data': response}

# @app.get('/supplier/{supplier_id}')
# async def get_specific_supplier(supplier_id: int):
#     response = await supplier_pydantic.from_queryset(Supplier.filter(id=supplier_id))
#     return {'status': 'success', 'data': response}

@app.get('/supplier/{supplier_id}')
async def get_specific_supplier(supplier_id: int):
    response = await supplier_pydantic.from_queryset_single(Supplier.get(id=supplier_id))
    return {'status': 'success', 'data': response}

# @app.put('/supplier/{supplier_id}')
# async def update_supplier(supplier_id: int, update_info: supplier_pydanticIn):
#     await Supplier.filter(id=supplier_id).update(**update_info.dict(exclude_unset=True))
#     response = await supplier_pydantic.from_queryset_single(Supplier.get(id=supplier_id))
#     return {'status': 'success', 'data': response}


@app.put('/supplier/{supplier_id}')
async def update_supplier(supplier_id: int, update_info: supplier_pydanticIn): # type: ignore
    supplier = await Supplier.get(id=supplier_id)
    update_info = update_info.dict(exclude_unset=True)
    supplier.name = update_info['name']
    supplier.company = update_info['company']
    supplier.email = update_info['email']
    supplier.phone = update_info['phone']

    await supplier.save()

    # response = await supplier_pydantic.from_queryset_single(Supplier.get(id=supplier_id))
    response = await supplier_pydantic.from_tortoise_orm(supplier)
    return {'status': 'success', 'data': response}


@app.delete('/supplier/{supplier_id}')
async def delete_supplier(supplier_id: int):
    # await Supplier.filter(id=supplier_id).delete()
    await Supplier.get(id=supplier_id).delete()
    return {'status': 'success', 'message': 'Supplier deleted'}

register_tortoise(
    app,
    # db_url="sqlite://db.sqlite3",
    db_url="sqlite://database.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)