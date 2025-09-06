from src.db.factory import make_database
from sqlalchemy import text

try:
    database = make_database()
    print("✅ Database connection successful!")
    
    # Test a session
    with database.get_session() as session:
        result = session.execute(text("SELECT 1")).scalar()
        print(f"✅ Session test successful: {result}")
        
    database.teardown()
    print("✅ Database teardown successful!")
    
except Exception as e:
    print(f"❌ Database test failed: {e}")