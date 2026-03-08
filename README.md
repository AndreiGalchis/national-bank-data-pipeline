# National Bank of Romania Data Pipeline

A backend system that retrieves and processes exchange rate data from the
National Bank of Romania (BNR) official XML feed.

The project implements a simple ETL pipeline to collect the data, transform it,
store it in a relational database and expose it through a REST API.


# Features

- ETL pipeline (Extract, Transform, Load)
- Retrieval of BNR exchange rates XML feed
- Data transformation and validation
- Storage in relational database
- REST API built using FastAPI
- Currency conversion service
- Alert system for exchange rate movements related to RON
- Data quality validation
- Pipeline metrics tracking
- Unit tests for ETL layers

Users can set alerts by specifying a currency and a percentage
threshold. When the exchange rate changes beyond the threshold
(increase or decrease), the system sends an email notification including 
the percentage change of the exchange rate.


# Architecture

The system implements a basic data pipeline architecture:
Data Source (BNR XML Feed) -> Extract -> Transform -> Load (in the Database) -> FastAPI


# Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite (designed with SQLAlchemy ORM for easy migration to PostgreSQL if needed)
- Requests
- XML parsing (xmltodict)
- Pytest

## How To Run

1.Create and activate virtual environment

From the project root (`Project/`):

powershell:
python -m venv venv
.\venv\Scripts\Activate.ps1

2.Install dependencies

powershell:
cd backend
python -m pip install -r requirements.txt
python -m pip install pytest

3.Configure environment variables (for email alerts)

Create backend/.env which contains:

SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password

4.Start API server

From backend/:

powershell:
uvicorn main:app --reload

Open docs in browser:

http://127.0.0.1:8000/docs

API endpoints:

- POST /api/update/exchange-rates - runs ETL pipeline and checks alerts
- GET /api/rates/latest - latest saved rates
- GET /api/convert - currency conversion based on latest rates
- POST /api/create-alerts - create alert
- GET /api/get-user-alerts - list alerts for user
- DELETE /api/delete-alert - delete alert





