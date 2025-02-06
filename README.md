# Fast Barber

This is a Barber Salon app built with FastAPI, SQLAlchemy. It allows users to manage barbers, their available hours, and customer bookings. WIP.

## Prerequisites

Before you start, make sure you have the following installed:

- Bash
- Python 3.8 or later
- pip (Python package installer)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/fast-barber.git
    cd fast-barber
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Starting the App

To start the app, run the following command:

```bash
cmod -x ./start.sh
./start.sh
```

This will start the FastAPI app, and it will be available at http://127.0.0.1:8000 by default.

## Accessing the FastAPI Documentation for testing

Once the app is running, you can access the FastAPI interactive documentation at:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc UI: http://127.0.0.1:8000/redoc

These interfaces allow you to test the API endpoints directly from the browser.

## Database

The app uses SQLite as the database and stores the data in ./db/barbershop.db.

The following tables are used:

- users: Stores users of the system.
- barbers: Stores barber information.
- available_hours: Stores the available working hours for each barber.
- bookings: Stores the customer appointments.

## Testing the API Endpoints

1. Add a Barber

To add a new barber, make a POST request to /barbers/ with a JSON body:

Example request:

```bash
curl -X 'POST' \
'http://127.0.0.1:8000/barbers/' \
-H 'Content-Type: application/json' \
-d '{
"name": "John Hairy"
}' 
```

This will add a new barber named "John Hairy".

2. Add Available Hours for a Barber

Once you have added a barber, you can set their available working hours by sending a POST request to /barbers/{barber_id}/available_hours/

Example request:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/barbers/1/available_hours/' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "day_of_week": "Monday",
    "start_time": "09:00:00",
    "end_time": "17:00:00"
  },
  {
    "day_of_week": "Tuesday",
    "start_time": "09:00:00",
    "end_time": "17:00:00"
  }
]'
```

This will set the working hours for the barber with ID 1.

3. Create a Booking

To create a booking, send a POST request to /bookings/

Example request:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/bookings/' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "John Doe",
  "barber_id": 1,
  "appointment_time": "2025-02-04T14:30"
}'

```

This will create an appointment for the user "John Doe" with the barber ID 1 at 14:30 on February 4th, 2025.

4. View Bookings

You can view all bookings by navigating to http://127.0.0.1:8000/bookings/ in your browser or using a GET request:

```bash
curl -X 'GET' 'http://127.0.0.1:8000/bookings/'
```

This will show a list of all bookings, including the username, barber name, and appointment time.

5. Running Tests

If you want to run tests, you can create test cases using FastAPI's test client or any testing framework of your choice.

6. Scripts

### Create Database Tables

If you need to create the database tables manually, you can use the create_tables() function:

```python
python -c "from package.models import create_tables"
```

This will create the necessary tables in the barbershop.db database.

## License

This project is licensed under the MIT License.


### Key Points in the `README.md`:

- **Installation Instructions**: Instructions to clone the repository and install dependencies.
- **Starting the App**: How to run the FastAPI app and access the API.
- **API Documentation**: Direct links to the Swagger and ReDoc UI for testing endpoints.
- **Adding Barbers, Available Hours, and Bookings**: Example commands for adding a barber, setting their available hours, and creating an appointment.
- **Create Tables Script**: Instructions for manually creating the database tables.
