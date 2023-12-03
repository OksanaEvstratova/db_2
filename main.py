import sqlalchemy
from models import create_tables
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale
import json

db_name = 'bookshop_db'
pg_pass = '694140'
db_port = '5432'
db_host = 'localhost'
DSN = f'postgresql://postgres:{pg_pass}@{db_host}:{db_port}/{db_name}'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r', encoding='utf-8') as bf:
    data = json.load(bf)
    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()
session.commit()

publisher_id = input("Введите ID издательства: ")
print()
q = session.query(Sale).join(Stock).join(Shop).join(Book).join(Publisher).filter(Publisher.id == publisher_id)
for s in q.all():
    print(f'{s.stock.book} | {s.stock.shop} | {"{:>4}".format(s.count*s.price)} | {s.date_sale}')

session.close()