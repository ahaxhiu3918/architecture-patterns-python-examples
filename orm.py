from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import registry, relationship # from mapper to registry
import model

Base = declarative_base()
mapper_registry = registry() # https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html


class Order(Base):
    id = Column(Integer, primary_key=True)

class OrderLine(Base):
    id = Column(Integer, primary_key=True)
    sku = Column(String(250))
    qty = Integer
    order_id = Column(Integer, ForeignKey('order.id'))
    order = relationship(Order)


order_lines = Table(
    'order_lines', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('sku', String(255)),
    Column('qty', Integer, nullable=False),
    Column('orderid', String(255)),
)

def start_mappers():
    lines_mapper = mapper_registry.map_imperatively(model.OrderLine, order_lines)