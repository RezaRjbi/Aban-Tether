# Aban-Tether Code Challenge

Aban-Tether is a Django-based project built as part of a code challenge. It implements a cryptocurrency exchange API that allows users to register purchase orders, process transactions atomically, manage currency balances, and manage exchanges.

## Overview

This project demonstrates various aspect of a  RESTful APIs using Django and Django REST Framework including:
- Currency management
- Exchange order creation, retrieval, updating, and deletion
- Transaction management with atomic operations
- testing using DRF’s APITestCase

## Features

- **User Management:** Secure user authentication and authorization.
- **Exchange Operations:** Endpoints for listing, buying, selling, and managing exchange orders.
- **Transaction Processing:** Ensures atomicity when updating user balances and registering exchanges.
- **Testing:** API tests covering successful operations, error conditions, and edge cases.

## Technology Stack

- **Python 3.12**
- **Django**
- **Django REST Framework**
- **PostgreSQL**
- **Docker & Docker Compose** (for containerized development)

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Docker and Docker Compose (optional, for containerized setup)
- PostgreSQL (or any other supported database)

### Local Development Setup

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/RezaRjbi/Aban-Tether.git
    cd Aban-Tether
    ```

2. **Create a Virtual Environment & Install Dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Configure the Database:**
    Update your `settings.py`.

4. **Apply Migrations:**
    ```bash
    python manage.py migrate
    ```

5. **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```

6. **Run the Test Suite:**
    ```bash
    python manage.py test
    ```

### Using Docker

- **Start Services with Docker Compose:**
    ```bash
    docker-compose up -d
    ```


## API Documentation

The API is built using Django REST Framework. Key endpoints include:

- **Exchange Endpoints:**
  - `GET /exchange/` – List all exchanges for the authenticated user.
  - `POST /exchange/buy/` – Place a buy order.
  - `POST /exchange/sell/` – Place a sell order.
  - `GET /exchange/{id}/` – Retrieve details of a specific exchange order.
  - `PUT/PATCH /exchange/{id}/` – Update an exchange order.
  - `DELETE /exchange/{id}/` – Delete an exchange order.

For more detailed API usage, please refer to the Postman collection file (`ABN.postman_collection.json`).
