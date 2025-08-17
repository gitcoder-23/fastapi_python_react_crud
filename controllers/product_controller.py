
from fastapi import APIRouter
from models import (Product, product_pydantic, product_pydanticIn, Supplier)

router = APIRouter(
    prefix="/products",
    tags=["Product"]
)


@router.post("/")
async def add_product(product_info: product_pydanticIn): # type: ignore
    product_obj = await Product.create(**product_info.dict(exclude_unset=True))
    response = await product_pydantic.from_tortoise_orm(product_obj)
    return {'status': 'success', 'data': response}

@router.get("/")
async def get_all_products():
    response = await product_pydantic.from_queryset(Product.all())
    return {'status': 'success', 'data': response}

@router.get("/{product_id}")
async def get_specific_product(product_id: int):
    response = await product_pydantic.from_queryset_single(Product.get(id=product_id))
    return {'status': 'success', 'data': response}


# @router.put("/{product_id}")
# async def update_product(product_id: int, update_info: product_pydanticIn): # type: ignore
#     product = await Product.get(id=product_id)
#     update_info = update_info.dict(exclude_unset=True)
#     product.name = update_info['name']
#     product.description = update_info['description']
#     product.quantity_in_stock = update_info['quantity_in_stock']
#     product.quantity_sold = update_info['quantity_sold']
#     product.unit_price = update_info['unit_price']
#     product.revenue += update_info['quantity_sold'] * update_info['unit_price']

#     await product.save()

#     response = await product_pydantic.from_tortoise_orm(product)
#     return {'status': 'success', 'data': response}

@router.put("/{product_id}")
async def update_product(product_id: int, update_info: product_pydanticIn):  # type: ignore
    product = await Product.get(id=product_id)
    payload = update_info.dict(exclude_unset=True)

    # Use current values as defaults and coerce types
    product.name = payload.get("name", product.name)
    product.description = payload.get("description", product.description)

    product.quantity_in_stock = int(payload.get("quantity_in_stock", product.quantity_in_stock))
    product.quantity_sold     = int(payload.get("quantity_sold", product.quantity_sold))
    product.unit_price        = int(payload.get("unit_price", product.unit_price))  # paise

    # Recompute revenue deterministically (no +=)
    product.revenue = product.quantity_sold * product.unit_price

    await product.save()
    response = await product_pydantic.from_tortoise_orm(product)
    return {"status": "success", "data": response}



@router.delete("/{product_id}")
async def delete_product(product_id: int):
    await Product.filter(id=product_id).delete()
    return {'status': 'success', 'message': 'Product deleted'}


# Product by supplier id
@router.post("/{supplier_id}")
async def add_products_by_supplier(supplier_id: int, product_details: product_pydanticIn):  # type: ignore
    supplier = await Supplier.get(id=supplier_id)
    payload = product_details.dict(exclude_unset=True)

    # Expect paise in the payload; coerce to int
    payload["unit_price"] = int(payload.get("unit_price", 0))
    payload["quantity_sold"] = int(payload.get("quantity_sold", 0))

    # Do NOT compute revenue here; model save() will compute it
    payload.pop("revenue", None)

    product_obj = await Product.create(**payload, supplied_by=supplier)
    response = await product_pydantic.from_tortoise_orm(product_obj)
    return {"status": "success", "data": response}



# @router.post("/product/{supplier_id}")
# async def add_products_by_supplier(supplier_id: int, product_details: product_pydanticIn ): # type: ignore
#     supplier = await Supplier.get(id=supplier_id)
#     product_details = product_details.dict(exclude_unset=True)
#     product_details['revenue'] += product_details['quantity_sold'] * product_details['unit_price']
#     product_obj = await Product.create(**product_details, supplied_by=supplier)
#     response = await product_pydantic.from_tortoise_orm(product_obj)
#     return {'status': 'success', 'data': response}

