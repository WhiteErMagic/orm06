import json

import psycopg2
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os

from models import create_tables, Publisher, Book, Shop, Stock, Sale

os.environ['PASSWORD'] = '1234'
os.environ['NAMEBASE'] = 'mybase'
os.environ['LOGIN'] = 'postgres'

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
        data.append(Book(id=v["id"], title=v["title"], id_publisher=v["id_publisher"]))

    for v in shops:
        data.append(Shop(id=v["id"], name=v["name"]))

    for v in stocks:
        data.append(Stock(id=v["id"], id_book=v["id_book"], id_shop=v["id_shop"], count=v["count"]))

    for v in sales:
        data.append(Sale(id=v["id"], price=v["price"], date_sale=v["date_sale"],
                         id_stock=v["id_stock"], count=v["count"]))

Session = sessionmaker(bind=engine)
session = Session()

session.add_all(data)
session.commit()


def get_shops(shop):
    query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)\
            .select_from(Shop)\
            .join(Stock)\
            .join(Book) \
            .join(Publisher) \
            .join(Sale)

    if shop.isdigit():
        result = query.filter(Shop.id == shop).all()
    else:
        result = query.filter(Shop.name == shop).all()

    for c in result:
        print(f'{c[0]: <40} | {c[1]: <10} | {c[2]: <8} | {c[3].strftime("%d-%m-%Y")}')

    session.close()


if __name__ == '__main__':
    shop = input('Магазин: ')
    get_shops(shop)