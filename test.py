from sqlalchemy import create_engine, inspect
import sys

DB_USER = "hsbc"
DB_PASSWORD = "hsbc"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "hsbc"

# Create connection string
connection_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(f"Attempting to connect to: {connection_string}")

try:
    engine = create_engine(connection_string)
    
    # Test the connection
    with engine.connect() as conn:
        print("Database connection successful!")
    
    if __name__ == "__main__":
        inspector = inspect(engine)

        # List all schemas
        schemas = inspector.get_schema_names()
        print("Schemas in the database:")
        for schema in schemas:
            print(f" - {schema}")

        # List all tables in public schema
        print("\nTables in 'public' schema:")
        tables = inspector.get_table_names(schema='public')
        for table in tables:
            print(f" - {table}")

        # Optional: list tables in all schemas
        print("\nTables in all schemas:")
        for schema in schemas:
            tables = inspector.get_table_names(schema=schema)
            for table in tables:
                print(f"{schema}.{table}")

except Exception as e:
    print(f"Database connection failed: {e}")
    print("\nTroubleshooting steps:")
    print("1. Make sure PostgreSQL container is running: docker ps")
    print("2. Check if psycopg2 is installed: pip install psycopg2-binary")
    print("3. Verify database is accessible: psql -h localhost -p 5432 -U hsbc -d hsbc")
    print("4. If running script in Docker, use container name as host instead of localhost")
    sys.exit(1)