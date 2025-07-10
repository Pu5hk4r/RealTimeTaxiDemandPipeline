# storage/init_db.py
import psycopg2
from psycopg2 import sql
from utils.config import DB_CONFIG
from utils.logger import get_logger

logger = get_logger(__name__)

def initialize_database():
    """Create database and tables if they don't exist"""
    try:
        # Connect to default postgres database to create our DB
        admin_conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            port=DB_CONFIG['port']
        )
        admin_conn.autocommit = True

        with admin_conn.cursor() as cur:
            # Check if database exists
            cur.execute("SELECT 1 FROM pg_database WHERE datname=%s", (DB_CONFIG['database'],))
            exists = cur.fetchone()

            if not exists:
                cur.execute(sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(DB_CONFIG['database'])
                ))
                logger.info(f"Created database {DB_CONFIG['database']}")

        admin_conn.close()

        # Now create tables
        app_conn = psycopg2.connect(**DB_CONFIG)
        with app_conn.cursor() as cur:
            with open('storage/schema.sql', 'r') as f:
                cur.execute(f.read())
            app_conn.commit()
            logger.info("Database schema initialized")

    except psycopg2.Error as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    finally:
        if 'admin_conn' in locals() and admin_conn:
            admin_conn.close()
        if 'app_conn' in locals() and app_conn:
            app_conn.close()

if __name__ == "__main__":
    initialize_database()