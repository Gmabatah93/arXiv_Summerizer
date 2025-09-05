from abc import ABC, abstractmethod
from typing import Any, ContextManager, Dict, List, Optional
from sqlalchemy.orm import Session


class BaseDatabase(ABC):
    """Abstract base class for database operations.
    
    This is like a contract - any database class must implement these methods.
    ABC = Abstract Base Class - you can't create an instance of this class directly.
    """
    
    @abstractmethod
    def startup(self) -> None:
        """Initialize the database connection.
        
        This method must be implemented by any concrete database class.
        It's where we establish the connection to the database.
        """
        pass

    @abstractmethod
    def teardown(self) -> None:
        """Close the database connection.
        
        Clean up resources when the app shuts down.
        """
        pass

    @abstractmethod
    def get_session(self) -> ContextManager[Session]:
        """Get a database session.
        
        A session is like a conversation with the database.
        ContextManager means it automatically handles opening/closing.
        """
        pass


class BaseRepository(ABC):
    """Abstract base class for data access operations.
    
    Repository pattern: separates data access logic from business logic.
    This makes your code more testable and maintainable.
    """
    
    def __init__(self, session: Session):
        """Initialize with a database session."""
        self.session = session

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Any:
        """Create a new record in the database."""
        pass

    @abstractmethod
    def get_by_id(self, record_id: Any) -> Optional[Any]:
        """Get a record by its ID."""
        pass

    @abstractmethod
    def update(self, record_id: Any, data: Dict[str, Any]) -> Optional[Any]:
        """Update a record by ID."""
        pass

    @abstractmethod
    def delete(self, record_id: Any) -> bool:
        """Delete a record by ID."""
        pass

    @abstractmethod
    def list(self, limit: int = 100, offset: int = 0) -> List[Any]:
        """List records with pagination."""
        pass