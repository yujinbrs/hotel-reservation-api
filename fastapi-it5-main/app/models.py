"""Data models used to validate API input and output."""

from pydantic import BaseModel, Field


class ReservationInput(BaseModel):
    """Fields students can send when creating or updating a record."""

    name: str = Field(min_length=1)
    contact_number: str = Field(min_length=7)
    room_number: int = Field(ge=1)

    @staticmethod
    def list_reservations(database_connection):
        with database_connection() as connection:
            rows = connection.execute(
                "SELECT room_number, name, contact_number FROM reservations ORDER BY room_number"
            ).fetchall()
        return [rows]

    @staticmethod
    def create_reservation(reservation_input, database_connection):
        with database_connection() as connection:
            connection.execute(
                "INSERT INTO reservations (room_number, name, contact_number) VALUES (?, ?, ?)",
                (reservation_input.room_number, reservation_input.name, reservation_input.contact_number),
            )
            row = connection.execute(
                "SELECT room_number, name, contact_number FROM reservations WHERE room_number = ?",
                (reservation_input.room_number,),
            ).fetchone()
        return row

    @staticmethod
    def get_reservation(room_number, database_connection):
        with database_connection() as connection:
            row = connection.execute(
                "SELECT room_number, name, contact_number FROM reservations WHERE room_number = ?",
                (room_number,),
            ).fetchone()
        return row

    @staticmethod
    def update_reservation(room_number, reservation_input, database_connection):
        with database_connection() as connection:
            connection.execute(
                "UPDATE reservations SET name = ?, contact_number = ? WHERE room_number = ?",
                (reservation_input.name, reservation_input.contact_number, room_number),
            )
            row = connection.execute(
                "SELECT room_number, name, contact_number FROM reservations WHERE room_number = ?",
                (room_number,),
            ).fetchone()
        return row

    @staticmethod
    def delete_reservation(room_number, database_connection):
        with database_connection() as connection:
            connection.execute(
                "DELETE FROM reservations WHERE room_number = ?",
                (room_number,),
            )

class Reservation(ReservationInput):
    """A reservation record returned by the API."""
    pass