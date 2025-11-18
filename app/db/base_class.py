from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr

# The base class which stores a description of the database table 
@as_declarative()
class Base:
    """Base class which provides automated table name
    and allows for type hinting with a mapped_column object."""
    
    @declared_attr
    def __tablename__(cls) -> str:
        # Generate table name automatically from class name (e.g., 'Book' -> 'book')
        return cls.__name__.lower()

    id: Any
    __name__: str