import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    books = relationship('Book', back_populates='publishers')


class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), unique=True)
    publisher_id = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publishers = relationship(Publisher, back_populates='books')
    stocks = relationship('Stock', back_populates='books')

    def __str__(self):
        return self.title


class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    stocks = relationship('Stock', back_populates='shops')

    def __str__(self):
        return self.name

class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    book_id = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    shop_id = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer)

    books = relationship('Book', back_populates='stocks')
    shops = relationship('Shop', back_populates='stocks')
    sales = relationship('Sale', back_populates='stocks')


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric(15,2))
    date_sale = sq.Column(sq.Date)
    stock_id = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer)

    stocks = relationship('Stock', back_populates='sales')

    def __str__(self):
        return str(self.price) + " | " + str(self.date_sale)


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)