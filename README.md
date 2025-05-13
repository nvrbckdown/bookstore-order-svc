## API Documentation

### Orders Endpoints

#### POST /api/v1/orders
- Create a new order
- Request body:
  ```json
  {
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "items": [
      {
        "book_id": 1,
        "book_title": "Pride and Prejudice",
        "quantity": 2,
        "price": 9.99
      }
    ]
  }
  ```

#### GET /api/v1/orders/{order_id}
- Get an order by ID

#### GET /api/v1/orders
- Get all orders with pagination
- Query parameters:
  - skip: Number of orders to skip (default: 0)
  - limit: Number of orders to return (default: 10, max: 100)

#### PUT /api/v1/orders/{order_id}
- Update an order status
- Request body:
  ```json
  {
    "status": "confirmed"
  }
  ```

#### DELETE /api/v1/orders/{order_id}
- Delete an order

#### GET /api/v1/orders/customer/{customer_email}
- Get all orders by customer email

## Running the Service

### Using Docker
```bash
# Build and run with Docker Compose
docker-compose up --build

# Run only the order service (after starting MongoDB)
docker build -t order-service .
docker run -p 8001:8001 order-service
```

### Using Python directly
```bash
uvicorn app.main:app --reload --port 8001
```

The service will be available at `http://localhost:8001`

## API Documentation
Once running, the interactive API documentation is available at:
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

## Communication with Book Service

The order service communicates with the book service to verify that books exist before creating orders. Make sure the book service is running and accessible at the URL specified in the `BOOK_SERVICE_URL` environment variable.# bookstore-order-svc
