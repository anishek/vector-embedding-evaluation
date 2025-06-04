from typing import List, Dict, Any
import psycopg2
from psycopg2.extras import execute_values
import os


# PostgreSQL connection parameters from environment variables
DB_NAME = os.environ.get("POSTGRES_DB", "anishek")
DB_USER = os.environ.get("POSTGRES_USER", "admin")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "")
DB_HOST = os.environ.get("POSTGRES_HOST", "localhost")
DB_PORT = os.environ.get("POSTGRES_PORT", "5432")


class PostgresManager:
    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        """Establish connection to PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
            )
            print("Successfully connected to PostgreSQL database")
        except Exception as e:
            print(f"Error connecting to PostgreSQL database: {e}")
            raise

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")

    def insert_embeddings(
        self, location: str, embedding: List[float], text_content: str
    ):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO e5_large_instruct (location, embedding, text_content) VALUES (%s, %s, %s)",
                    (location, embedding.tolist(), text_content),
                )
                self.conn.commit()
        except Exception as e:
            print(f"Error inserting embedding: {e}")
            self.conn.rollback()
            raise

    def insert_embeddings_batch(self, data: List[Dict[str, Any]]):
        try:
            with self.conn.cursor() as cur:
                execute_values(
                    cur,
                    "INSERT INTO e5_large_instruct (location, embedding, text_content) VALUES %s",
                    [
                        (
                            item["location"],
                            item["embedding"].tolist(),
                            item["text_content"],
                        )
                        for item in data
                    ],
                )
                self.conn.commit()
        except Exception as e:
            print(f"Error inserting embeddings batch: {e}")
            self.conn.rollback()
            raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
