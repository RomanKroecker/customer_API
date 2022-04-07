from sqlalchemy import Column, Integer, String, Boolean


from db.base_class import Base


class Customer(Base):
    id = Column(Integer, primary_key=True,index=True)
    lastname  = Column(String, unique=False, nullable=False)
    firstname = Column(String, unique=False, nullable=False)
    street = Column(String, unique=False, nullable=True)
    postcode = Column(String, unique=False, nullable=True)
    city = Column(String, unique=False, nullable=True)
    email = Column(String, nullable=False, unique=True, index=True)
    phone = Column(String, unique=False, nullable=True)