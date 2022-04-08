from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.orm import Session 
from sqlalchemy import desc, asc

from db.session import get_db 
from db.models.customers import Customer 
from schemas.customers import CustomerCreate, ShowCustomer
from db.repository.customers import create_new_customer, retreive_customer, list_customers, update_customer_by_id, delete_customer_by_id, checkEmailExist
from typing import List
from pydantic import EmailStr
from typing import Optional
from operator import attrgetter
from core.filter import Filter


router = APIRouter() 



@router.post("/create-customer",response_model=ShowCustomer)
def create_customer(customer:CustomerCreate, db:Session=Depends(get_db)):
    if checkEmailExist(email=customer.email, db=db) != -1:
        raise HTTPException(status_code=400, detail="Email already exists")
    customer = create_new_customer(customer=customer, db=db)
    return customer



@router.get("/get_id/{id}", response_model=ShowCustomer)
def retreive_customer_by_id(id:int, db:Session = Depends(get_db)):
    customer = retreive_customer(var=id, db=db)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail=f"Customer with id {id} does not exist")
    return customer


@router.get("/get_email/{email}", response_model=ShowCustomer)
def retreive_customer_by_email(email:EmailStr, db:Session = Depends(get_db)):
    customer = retreive_customer(var=email, db=db)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail=f"Customer with email {email} does not exist")
    return customer





# @router.get("/all")
# def retreive_all_customers(db:Session = Depends(get_db)):
#     customers = list_customers(db=db)
#     return customers 


@router.get("/all")
def retreive_all_customers(db:Session = Depends(get_db), itemsPerPage:int=None, page:Optional[int]=0, order_by:Optional[str]=None, 
                           sortType:Optional[str]="asc", filter_by:Optional[str]=None, filter_val:Optional[str]=None, filterType:Optional[str]="equals"):
    # Get all customers
    customers = list_customers(db=db)
    
    # Sort
    if(order_by):
        if(hasattr(Customer(), order_by)):
            if(sortType=="asc"):
                customers.sort(key=attrgetter(order_by))
            else:
                customers.sort(key=attrgetter(order_by), reverse=True)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Customer has no attribute \'{order_by}\'")
            
    
    # Filter
    if(filter_by):
        # call method by name
        customers = getattr(Filter(), filterType)(customers, filter_by, filter_val)
        
    
    
    # Paging
    if(itemsPerPage):
        customers = customers[(page)*itemsPerPage:(page+1)*itemsPerPage]
    return customers 


@router.put("/update/{id}")
def update_customer(id:int, customer:CustomerCreate, db:Session=Depends(get_db)):
    ex_id = checkEmailExist(email=customer.email, db=db)
    
    if ex_id > -1 and id != ex_id:
        raise HTTPException(status_code=400, detail="Email already exists")
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


