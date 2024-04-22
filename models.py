from pydantic import BaseModel, Field, EmailStr, PastDate, field_validator
import databases
import sqlalchemy


DATABASE_URL = "sqlite:///mydatabase.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


class UserIn(BaseModel):
    firstname: str = Field(..., max_length=30)
    secondname: str = Field(max_length=30)
    email: EmailStr = Field(..., max_length=50)
    password: str = Field (..., min_length=5, max_length=50) 


class User(UserIn):
    id: int


class ProductIn(BaseModel):
    name: str = Field(..., max_length=50, unique=True)
    description: str = Field(..., max_length=200)
    price: float = Field(...)

    class Config:
        orm_mode = True

    @field_validator('price')
    def validate_price(cls, value):
        if value <= 0:
            raise ValueError("Price must be a positive number")
        return value


class Product(ProductIn):
    id: int


class OrderIn(BaseModel):
    id_user: int = User
    id_product: int = Product
    date: PastDate
    status: str = Field(..., max_length=50)

    class Config:
        orm_mode = True


class Order(OrderIn):
    id: int


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('firstname', sqlalchemy.String(30)),
    sqlalchemy.Column('secondname', sqlalchemy.String(30)),
    sqlalchemy.Column('email', sqlalchemy.String(50)),
    sqlalchemy.Column('password', sqlalchemy.String(50)),
)

products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(50)),
    sqlalchemy.Column("description", sqlalchemy.String(200)),
    sqlalchemy.Column("price", sqlalchemy.Float()),
)

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("id_user", sqlalchemy.Integer, sqlalchemy.ForeignKey(users.c.id), nullable=False),
    sqlalchemy.Column("id_product", sqlalchemy.Integer, sqlalchemy.ForeignKey(products.c.id), nullable=False),
    sqlalchemy.Column("date", sqlalchemy.Date()),
    sqlalchemy.Column("status", sqlalchemy.String(20)),
)