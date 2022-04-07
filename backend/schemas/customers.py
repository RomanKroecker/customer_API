from typing import Optional 
from pydantic import BaseModel, EmailStr


class CustomerBase(BaseModel):
    lastname : str 
    firstname : str
    email : EmailStr 
    street : Optional[str] = None 
    postcode : Optional[str] = None 
    city : Optional[str] = None 
    phone : Optional[str] = None 


class CustomerCreate(CustomerBase):
    lastname : str
    firstname : str 
    email : EmailStr 


class ShowCustomer(CustomerBase):
    lastname : str
    firstname : str
    email : EmailStr  
    street : Optional[str]
    postcode : Optional[str]
    city : Optional[str]
    phone : Optional[str]
    
    class Config():
        orm_mode = True