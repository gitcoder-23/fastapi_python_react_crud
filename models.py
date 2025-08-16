from tortoise.models import Model
from tortoise import  fields
from tortoise.contrib.pydantic import pydantic_model_creator

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50)
    email = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    def __str__(self):
        return self.username

    class Meta:
        table = "users"
        ordering = ["-created_at"]

class Product(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, nullable=False)
    # description = fields.TextField()
    quantity_in_stock = fields.IntField(default=0)
    quantity_sold = fields.IntField(default=0)
    unit_price = fields.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    revenue = fields.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    supplied_by = fields.ForeignKeyField("models.Supplier", related_name="goods_supplied", null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        table = "products"
        ordering = ["-created_at"]


class Supplier(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    company = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100)
    phone = fields.CharField(max_length=15, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        table = "suppliers"
        ordering = ["-created_at"]


# Create Pydentic Models
user_pydantic = pydantic_model_creator(User, name="User")
user_pydanticIn = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)

product_pydantic = pydantic_model_creator(Product, name="Product")
product_pydanticIn = pydantic_model_creator(Product, name="ProductIn", exclude_readonly=True)

supplier_pydantic = pydantic_model_creator(Supplier, name="Supplier")
supplier_pydanticIn = pydantic_model_creator(Supplier, name="SupplierIn", exclude_readonly=True)
