
# Project Currency Exchange

## Setup Instructions

1. Clone the repository or extract the zip file.
2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Set up environment variables for sensitive data:
   ```
   export CURRENCYBEACON_API_KEY=your_api_key
   ```
4. Run migrations and start the server:
   ```
   python manage.py migrate
   python manage.py runserver
   ```
5. Access the admin interface at `/admin` (create a superuser using `python manage.py createsuperuser`).

6. Use the Postman collection to test APIs.

## Features
- Currency and Exchange Rate management.
- Dynamic provider integration (CurrencyBeacon).
- REST APIs for CRUD, conversion, and historical data.
- Asynchronous task setup (requires Celery).

## Postman Collection
The Postman collection is included in the root folder as `postman_collection.json`.
    
