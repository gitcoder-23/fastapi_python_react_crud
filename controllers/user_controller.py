from fastapi import APIRouter
from models import ( user_pydantic, user_pydanticIn, User)

router = APIRouter(
    prefix="/users",
    tags=["User"]
)




# @app.get("/users", response_model=List[user_pydantic])
# async def get_users():
#     response = await user_pydantic.from_queryset(User.all())
#     return {'status': 'success', 'data': response}


@router.post("/")
async def add_user(user_info: user_pydanticIn): # type: ignore
    user_obj = await User.create(**user_info.dict(exclude_unset=True))
    response = await user_pydantic.from_tortoise_orm(user_obj)
    return {'status': 'success', 'data': response}


@router.get("/")
async def get_all_users():
    response = await user_pydantic.from_queryset(User.all())
    return {'status': 'success', 'data': response}

@router.get("/{user_id}")
async def get_specific_user(user_id: int):
    response = await user_pydantic.from_queryset_single(User.get(id=user_id))
    return {'status': 'success', 'data': response}




@router.delete("/{user_id}")
async def delete_user(user_id: int):
    # await User.filter(id=user_id).delete()
    await User.get(id=user_id).delete()
    return {'status': 'success', 'message': 'User deleted'}