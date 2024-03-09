import json

import psycopg2
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os

from models import create_tables, Publisher, Book, Shop, Stock, Sale

PASSWORD = os.getenv('PASSWORD')
NAMEBASE = os.getenv('NAMEBASE')
LOGIN = os.getenv('LOGIN')

DSN = f'postgresql://{LOGIN}:{PASSWORD}@localhost:5432/{NAMEBASE}'

engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

with open("fixtures/fixtures.json", 'r', encoding='utf-8') as f:
    list_data = json.load(f)

    publishers = list_data.get("Publishers")
    books = list_data.get("Books")
    shops = list_data.get("Shops")
    stocks = list_data.get("Stocks")
    sales = list_data.get("Sales")

    data = []

    for v in publishers:
        data.append(Publisher(id=v["id"], name=v["name"]))

    for v in books:
        data.append(Book(id=v["id"], title=v["title"], publisher_id=v["publisher_id"]))

    for v in shops:
        data.append(Shop(id=v["id"], name=v["name"]))

    for v in stocks:
        data.append(Stock(id=v["id"], book_id=v["book_id"], shop_id=v["shop_id"], count=v["count"]))

    for v in sales:
        data.append(Sale(id=v["id"], price=v["price"], date_sale=v["date_sale"],
                         stock_id=v["stock_id"], count=v["count"]))

Session = sessionmaker(bind=engine)
session = Session()

session.add_all(data)
session.commit()

#code_publisher = input("Code publisher: ")
for c in session.query(Stock, Book, Shop, Sale)\
        .filter(Stock.book_id == Book.id)\
        .filter(Shop.id == Stock.shop_id)\
        .filter(Sale.stock_id == Stock.id)\
        .filter(Book.publisher_id == 1).all():
      print(f'{c[1]} | {c[2]} | {c[3]}')


session.close()

