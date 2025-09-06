from src.config import get_settings
from src.db.interfaces.base import BaseDatabase
from src.db.interfaces.postgresql import PostgreSQLDatabase, PostgreSQLSettings


def make_database() -> BaseDatabase:
    """Factory function to create a database instance.
    
    This function:
    1. Gets your app settings
    2. Creates database-specific configuration
    3. Creates and initializes the database
    4. Returns the ready-to-use database
    
    Factory pattern: centralizes object creation logic
    """
    # Get your app settings
    settings = get_settings()

    # Create PostgreSQL-specific configuration
    config = PostgreSQLSettings(
        database_url=settings.postgres_database_url,
        echo_sql=settings.postgres_echo_sql,
        pool_size=settings.postgres_pool_size,
        max_overflow=settings.postgres_max_overflow,
    )

    # Create and initialize the database
    database = PostgreSQLDatabase(config=config)
    database.startup()  # This connects to the database and creates tables
    return database