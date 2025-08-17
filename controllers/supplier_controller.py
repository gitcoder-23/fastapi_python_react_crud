from fastapi import APIRouter
from models import ( supplier_pydantic, supplier_pydanticIn, Supplier)

router = APIRouter(
    prefix="/supplier",
    tags=["Supplier"]
)


@router.post("/")
async def add_supplier(supplier_info: supplier_pydanticIn): # type: ignore
    supplier_obj = await Supplier.create(**supplier_info.dict(exclude_unset=True))
    response = await supplier_pydantic.from_tortoise_orm(supplier_obj)
    return {'status': 'success', 'data': response}

@router.get("/")
async def get_all_suppliers():
    response = await supplier_pydantic.from_queryset(Supplier.all())
    return {'status': 'success', 'data': response}

# @app.get('/supplier/{supplier_id}')
# async def get_specific_supplier(supplier_id: int):
#     response = await supplier_pydantic.from_queryset(Supplier.filter(id=supplier_id))
#     return {'status': 'success', 'data': response}

@router.get("/{supplier_id}")
async def get_specific_supplier(supplier_id: int):
    response = await supplier_pydantic.from_queryset_single(Supplier.get(id=supplier_id))
    return {'status': 'success', 'data': response}

# @app.put('/supplier/{supplier_id}')
# async def update_supplier(supplier_id: int, update_info: supplier_pydanticIn):
#     await Supplier.filter(id=supplier_id).update(**update_info.dict(exclude_unset=True))
#     response = await supplier_pydantic.from_queryset_single(Supplier.get(id=supplier_id))
#     return {'status': 'success', 'data': response}


@router.put("/{supplier_id}")
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


@router.delete("/{supplier_id}")
async def delete_supplier(supplier_id: int):
    # await Supplier.filter(id=supplier_id).delete()
    await Supplier.get(id=supplier_id).delete()
    return {'status': 'success', 'message': 'Supplier deleted'}