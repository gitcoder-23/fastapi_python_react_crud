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


@router.put("/{product_id}")
async def update_product(product_id: int, update_info: product_pydanticIn): # type: ignore
    product = await Product.get(id=product_id)
    update_info = update_info.dict(exclude_unset=True)
    product.name = update_info['name']
    product.description = update_info['description']
    product.quantity_in_stock = update_info['quantity_in_stock']
    product.quantity_sold = update_info['quantity_sold']
    product.unit_price = update_info['unit_price']
    product.revenue += update_info['quantity_sold'] * update_info['unit_price']

    await product.save()

    response = await product_pydantic.from_tortoise_orm(product)
    return {'status': 'success', 'data': response}


@router.delete("/{product_id}")
async def delete_product(product_id: int):
    await Product.filter(id=product_id).delete()
    return {'status': 'success', 'message': 'Product deleted'}


# Product by supplier id
@router.post("/product/{supplier_id}")
async def add_products_by_supplier(supplier_id: int, product_details: product_pydanticIn ): # type: ignore
    supplier = await Supplier.get(id=supplier_id)
    product_details = product_details.dict(exclude_unset=True)
    product_details['revenue'] += product_details['quantity_sold'] * product_details['unit_price']
    product_obj = await Product.create(**product_details, supplied_by=supplier)
    response = await product_pydantic.from_tortoise_orm(product_obj)
    return {'status': 'success', 'data': response}

