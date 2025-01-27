from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)  
    name = Column(String, nullable=False)              
    description = Column(String, nullable=True)       
    price = Column(Integer, nullable=False)            

    # Foreign key linking to User
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    # Relationship with User
    creator = relationship("User", back_populates="products") 
    def __repr__(self):
        return f"<Product id={self.id} name={self.name} price={self.price}>"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)  
    name = Column(String, nullable=False)              
    email = Column(String, nullable=False, unique=True)  
    password = Column(String, nullable=False)          

    # Relationship with Product
    products = relationship('Product', back_populates="creator", cascade="all, delete")  # Cascade deletion

    def __repr__(self):
        return f"<User id={self.id} name={self.name} email={self.email}>"
