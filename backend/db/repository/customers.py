from sqlalchemy.orm import Session 

from schemas.customers import CustomerCreate 
from db.models.customers import Customer 
from pydantic import EmailStr



def create_new_customer(customer:CustomerCreate, db:Session):
    customer = Customer(**customer.dict())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

def retreive_customer(id:int, db:Session):
    customer = db.query(Customer).filter(Customer.id==id).first()
    return customer


def list_customers(db: Session):
    customers = db.query(Customer).all()
    return customers


def update_customer_by_id(id:int, customer:CustomerCreate, db:Session):
    existing_customer = db.query(Customer).filter(Customer.id == id)
    if(not existing_customer.first()):
        return 0
    customer.__dict__.update()
    existing_customer.update(customer.__dict__)
    db.commit()
    return 1


def delete_customer_by_id(id:int, db:Session):
    existing_customer = db.query(Customer).filter(Customer.id == id)
    if(not existing_customer.first()):
        return 0
    existing_customer.delete(synchronize_session=False)
    db.commit()
    return 1



def checkEmailExist(email:EmailStr, db:Session):
    existing_customer = db.query(Customer).filter(Customer.email == email)
    if(not existing_customer.first()):
        return False
    else:
        return True