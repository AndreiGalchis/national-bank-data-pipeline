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
- PostgreSQL / SQLite
- Requests
- XML parsing (xmltodict)







