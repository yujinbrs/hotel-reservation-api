"""Create the FastAPI app and connect its route modules."""

from fastapi import FastAPI

from app.database import database_connection, initialize_database
from app.models import Reservation, ReservationInput

app = FastAPI(title="Hotel Reservation")


@app.get("/")
def home():
    return {"message": "Welcome! Visit /docs to try the API."}


@app.get("/reservations")
def get_reservations():
    result = Reservation.list_reservations(database_connection=database_connection)
    return {"reservations": result}


@app.get("/reservations/{room_number}")
def get_reservation(room_number: int):
    result = Reservation.get_reservation(
        room_number=room_number, database_connection=database_connection
    )
    return {"reservation": result}


@app.post("/reservation")
def create_reservation(reservation: ReservationInput):
    result = Reservation.create_reservation(
        reservation_input=reservation, database_connection=database_connection
    )
    return {"reservation": result}


@app.put("/reservation/{room_number}")
def edit_reservation(room_number: int, reservation: ReservationInput):
    result = Reservation.update_reservation(
        room_number=room_number,
        reservation_input=reservation,
        database_connection=database_connection,
    )
    return {"reservation": result}


@app.delete("/reservation/{room_number}")
def delete_reservation(room_number: int):
    Reservation.delete_reservation(
        room_number=room_number, database_connection=database_connection
    )
    return {"message": "Reservation deleted successfully"}


initialize_database()
