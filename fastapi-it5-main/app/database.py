"""SQLite connection and table setup."""

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

DATABASE_FILE = Path(__file__).resolve().parent.parent / "hotel.db"


@contextmanager
def database_connection() -> Iterator[sqlite3.Connection]:
    """Open a database connection and always close it after the operation."""

    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database() -> None:
    """Create the reservations table the first time the app runs."""

    with database_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS reservations (
                room_number INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                contact_number TEXT NOT NULL
            )
            """
        )
