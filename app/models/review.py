from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Review(Base):
    """
    SQLAlchemy ORM model for the 'reviews' table
    """
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key referencing the 'books' table
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False, index=True) 
    
    # Assuming user_id will come from the authenticated user]
    user_id = Column(Integer, index=True, nullable=False) 
    
    review_text = Column(Text)
    rating = Column(Integer) # Typically 1-5

    # Define the relationship to the Book model (for easy back-reference)
    # back_populates allows us to access reviews from the book object
    book = relationship("Book", back_populates="reviews") 
    
    def __repr__(self):
        return f"<Review(book_id={self.book_id}, rating={self.rating})>"
