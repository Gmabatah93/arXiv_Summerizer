"""
IMPLEMENTATION LAYER

- The concrete PostgreSQL implementation:
"""

import logging
from contextlib import contextmanager
from typing import Generator, Optional

from pydantic import Field
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from src.db.interfaces.base import BaseDatabase

logger = logging.getLogger(__name__)


class PostgreSQLSettings(BaseSettings):
    """PostgreSQL-specific configuration settings."""
    
    database_url: str = Field(
        default="postgresql://rag_user:rag_password@localhost:5432/rag_db",
        description="PostgreSQL database URL"
    )
    echo_sql: bool = Field(default=False, description="Enable SQL query logging")
    pool_size: int = Field(default=20, description="Database connection pool size")
    max_overflow: int = Field(default=0, description="Maximum pool overflow")

    class Config:
        env_prefix = "POSTGRES_"  # Environment variables start with POSTGRES_


# This creates the base class for all our database models
Base = declarative_base()


class PostgreSQLDatabase(BaseDatabase):
    """PostgreSQL database implementation.
    
    This class implements the BaseDatabase interface for PostgreSQL.
    It handles all the low-level database operations.
    """
    
    def __init__(self, config: PostgreSQLSettings):
        """Initialize with PostgreSQL configuration."""
        self.config = config
        self.engine: Optional[Engine] = None                 # SQLAlchemy engine
        self.session_factory: Optional[sessionmaker] = None  # Factory for creating sessions

    def startup(self) -> None:
        """Initialize the database connection and create tables."""
        try:
            # Log connection attempt
            logger.info(f"Connecting to PostgreSQL...")
            
            # Create the database engine
            self.engine = create_engine(
                self.config.database_url,
                echo=self.config.echo_sql,           # Log SQL queries if enabled
                pool_size=self.config.pool_size,     # Connection pool size
                max_overflow=self.config.max_overflow, # Additional connections
                pool_pre_ping=True,                  # Test connections before use
            )

            # Create session factory
            self.session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)

            # Test the connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))  # Simple test query
                logger.info("Database connection test successful")

            # Create tables if they don't exist
            Base.metadata.create_all(bind=self.engine)
            logger.info("PostgreSQL database initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize PostgreSQL database: {e}")
            raise

    def teardown(self) -> None:
        """Close the database connection."""
        if self.engine:
            self.engine.dispose()  # Close all connections
            logger.info("PostgreSQL database connections closed")

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Get a database session with automatic cleanup.
        
        Context manager ensures the session is properly closed even if an error occurs.
        """
        if not self.session_factory:
            raise RuntimeError("Database not initialized. Call startup() first.")

        session = self.session_factory()
        try:
            yield session  # Give the session to the caller
        except Exception:
            session.rollback()  # Undo any changes if there's an error
            raise
        finally:
            session.close()  # Always close the session