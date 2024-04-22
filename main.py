from typing import List
from fastapi import FastAPI
from models import User, UserIn, Product, ProductIn, Order, OrderIn, users, products, orders, database, engine, metadata

app = FastAPI()
metadata.create_all(engine)


@app.get("/users/", response_model=List[User])
async def all_users():
    query = users.select()
    return await database.fetch_all(query)

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)
   
@app.post("/users/", response_model=int)
async def add_user(user: UserIn):
    query = users.insert().values(**user.model_dump())
    new_id = await database.execute(query)
    return new_id

@app.put("/users/{user_id}", response_model=User)
async def edit_user(user_id: int, user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**user.model_dump())
    await database.execute(query)
    return await get_user(user_id)

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'msg': "success"}

@app.get("/products/", response_model=List[Product])
async def read_products():
    query = products.select()
    return await database.fetch_all(query)


@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await database.fetch_one(query)


@app.post("/products/", response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values(**product.model_dump())
    last_record_id = await database.execute(query)
    return {**product.model_dump(), "id": last_record_id}


@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, new_product: ProductIn):
    query = products.update().where(products.c.id == product_id).values(**new_product.model_dump())
    await database.execute(query)
    return {**new_product.model_dump(), "id": product_id}


@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {'message': 'product deleted'}


@app.get("/orders/", response_model=List[Order])
async def read_orders():
    query = orders.select()
    # query = orders.select().join(users)
    return await database.fetch_all(query)


@app.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)  #.join(products, products.c.id == orders.c.id_user)
    return await database.fetch_one(query)


@app.post("/orders/", response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(**order.model_dump())
    last_record_id = await database.execute(query)
    return {**order.model_dump(), "id": last_record_id}


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.model_dump())
    await database.execute(query)
    return {**new_order.model_dump(), "id": order_id}


@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'order deleted'}