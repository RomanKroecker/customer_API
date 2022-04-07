from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.orm import Session 

from db.session import get_db 
from db.models.customers import Customer 
from schemas.customers import CustomerCreate, ShowCustomer
from db.repository.customers import create_new_customer, retreive_customer, list_customers, update_customer_by_id, delete_customer_by_id, checkEmailExist
from typing import List


router = APIRouter() 



@router.post("/create-customer",response_model=ShowCustomer)
def create_customer(customer:CustomerCreate, db:Session=Depends(get_db)):
    if checkEmailExist(email=customer.email, db=db):
        raise HTTPException(status_code=400, detail="Email already exists")
    customer = create_new_customer(customer=customer, db=db)
    return customer



@router.get("/get/{id}", response_model=ShowCustomer)
def retreive_customer_by_id(id:int, db:Session = Depends(get_db)):
    customer = retreive_customer(id=id, db=db)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail=f"Customer with id {id} does not exist")
    return customer



@router.get("/all")
def retreive_all_customers(db:Session = Depends(get_db)):
    customers = list_customers(db=db)
    return customers 



@router.put("/update/{id}")
def update_customer(id:int, customer:CustomerCreate, db:Session=Depends(get_db)):
    message = update_customer_by_id(id=id, customer=customer, db=db)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Customer with id {id} does not exist")
    return { "detail":"Successfully updated data"}



@router.delete("/delete/{id}")
def delete_customer(id:int, db:Session=Depends(get_db)):
    message = delete_customer_by_id(id=id, db=db)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Customer with id {id} does not exist")
    return {"detail":"Successfully deleted the customer"}

