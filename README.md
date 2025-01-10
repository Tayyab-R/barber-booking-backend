# Barber Booking Backend

This repository contains the backend system for a barber booking application built using Python Django REST Framework.

# Features

- API endpoints to manage barbers, slots, and bookings.

- PostgreSQL integration using Docker for seamless database management.

- Scalable backend architecture ready for future enhancements.

# Requirements

- Python version: 3.12.7

- Database: PostgreSQL (via Docker)

- Environment Variables: Configure .env file as shown below.

# Setup Instructions

1. Clone the Repository

` git clone https://github.com/yourusername/barber-booking-backend.git
cd barber-booking-backend 
`

2. Set Up the PostgreSQL Database with Docker

Ensure you have Docker installed. Run the following command to set up a PostgreSQL container:

` docker run --name barber-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
`

3. Create a Virtual Environment

` python -m venv venv `

4. Activate the Virtual Environment

On Linux/macOS:

`source venv/bin/activate `

On Windows:

` venv\Scripts\activate `

5. Install Dependencies

After activating the virtual environment, install the required packages:

` pip install -r requirements.txt `

Environment Variables

There is a .env file in the root of the project and add the following configurations:

` POSTGRES_DB='postgres'
POSTGRES_USER='postgres'
POSTGRES_PASSWORD='postgres'
HOST='localhost'
PORT=5432 `

# Notes

This project is still under development and requires improvements.

Future updates will include better API endpoints, enhanced error handling, and additional features.

Contributions are welcome!



