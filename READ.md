E-Commerce API — 2-Week Project Flow
Overall architecture
                    ┌─────────────────┐
                    │   React Client  │
                    └────────┬────────┘
                             │ HTTP
                             ▼
                    ┌─────────────────┐
                    │    FastAPI      │
                    │      API        │
                    └────────┬────────┘
                             │
             ┌───────────────┼────────────────┐
             ▼               ▼                ▼
        ┌─────────┐     ┌──────────┐    ┌──────────┐
        │ MySQL   │     │  Redis   │    │ M-Pesa   │
        │ Database│     │  Cache   │    │   API    │
        └─────────┘     └──────────┘    └──────────┘
WEEK 1 — Build the Core Backend
🟢 Day 1 — Project Setup & Architecture

Learn:

FastAPI project structure
Routers
Environment variables
Database configuration
Dependency management

Create:

ecommerce_api/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   │
│   ├── routers/
│   ├── services/
│   └── utils/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
Goal

Get:

GET /

working and connected to MySQL.

🟢 Day 2 — Database Design

Design the relationships before writing lots of code.

Tables
users
categories
products
cart_items
orders
order_items
payments
reviews

Understand:

User
 │
 ├── Cart Items
 │
 ├── Orders
 │     └── Order Items
 │            └── Product
 │
 └── Reviews
        └── Product

Category
   │
   └── Products

Order
   │
   └── Payment
Goal

Create the SQLAlchemy models and understand why each relationship exists.

🟢 Day 3 — Authentication

Build:

POST /auth/register
POST /auth/login
GET  /auth/me

Learn:

Password hashing
JWT
OAuth2
Authentication dependencies
User roles

Roles:

customer
admin
Goal

A user can register → login → receive JWT → access protected endpoints.

🟢 Day 4 — Categories & Products

Build:

POST   /categories
GET    /categories
POST   /products
GET    /products
GET    /products/{id}
PUT    /products/{id}
DELETE /products/{id}

Learn:

CRUD
Pydantic schemas
Relationships
Foreign keys
Validation

Add filtering:

/products?category=electronics
/products?search=phone
/products?min_price=1000&max_price=50000
🟢 Day 5 — Product Listing Properly

Now make the product API feel realistic.

Add:

Pagination
/products?page=1&limit=10
Search
/products?search=iphone
Category filtering
/products?category_id=3
Sorting
/products?sort=price

Learn:

Query parameters
SQLAlchemy filtering
Pagination
Efficient queries
Database indexes
🟢 Day 6 — Shopping Cart

Build:

POST   /cart/items
GET    /cart
PUT    /cart/items/{id}
DELETE /cart/items/{id}

Example:

User
 ↓
Add iPhone
 ↓
Cart
 ├── iPhone × 2
 ├── Mouse × 1
 └── Keyboard × 1

Calculate:

subtotal
quantity
total
Important concept

Don't trust the frontend to tell you the final price.

The backend should calculate it.

🟢 Day 7 — Orders

Now turn the cart into an order.

POST /orders
GET  /orders
GET  /orders/{id}

Flow:

Cart
 ↓
Checkout
 ↓
Create Order
 ↓
Create Order Items
 ↓
Calculate Total
 ↓
Clear Cart
 ↓
Order = PENDING

Order status:

PENDING
PAID
PROCESSING
SHIPPED
DELIVERED
CANCELLED
End of Week 1 🎯

You should have:

Authentication       ✅
Users                ✅
Categories           ✅
Products             ✅
Search               ✅
Filtering            ✅
Pagination           ✅
Cart                 ✅
Orders               ✅

At this point you already have a legitimate E-Commerce backend.

WEEK 2 — Advanced Backend Features
🔵 Day 8 — Order Management

Now introduce admin functionality.

Admin can:

GET /admin/orders
PUT /admin/orders/{id}/status

Example:

PENDING
   ↓
PAID
   ↓
PROCESSING
   ↓
SHIPPED
   ↓
DELIVERED

Learn:

Role-based authorization
Admin dependencies
Business rules
Preventing customers from accessing admin endpoints
🔵 Day 9 — Product Reviews & Ratings

Build:

POST /products/{id}/reviews
GET  /products/{id}/reviews

Example:

Product: iPhone 15

Rating:
★★★★★ 4.7

Reviews:
John:    ★★★★★
Mary:    ★★★★☆
Peter:   ★★★★★

Add rules:

User must be authenticated
User cannot review the same product twice
Rating must be between 1 and 5

Learn:

Constraints
Aggregations
Relationships
Business validation
🔵 Day 10 — M-Pesa Integration

This is one of the biggest days.

Build:

POST /payments/stk-push

Flow:

Customer
   ↓
Checkout
   ↓
Create Order
   ↓
Request STK Push
   ↓
Customer enters M-Pesa PIN
   ↓
M-Pesa processes payment
   ↓
Callback → Your API
   ↓
Verify payment
   ↓
Order = PAID

Create:

payments

with information such as:

id
order_id
amount
phone_number
checkout_request_id
merchant_request_id
status
created_at

We'll use sandbox mode, not real money.

🔵 Day 11 — Redis Caching

Now bring in something you've already been studying.

Cache:

GET /products
GET /categories
GET /products/{id}

Flow:

Request
   ↓
Redis?
 ┌─┴─┐
YES  NO
 │    │
 ▼    ▼
Return MySQL
       │
       ▼
      Redis

Learn:

Cache-aside
Cache expiration
Cache invalidation
Why caching helps
Avoiding stale data

Example:

GET /products

First request → MySQL
Second request → Redis
Third request → Redis
🔵 Day 12 — Security & Error Handling

This day makes the project feel professional.

Add:

Validation
Invalid price
Invalid email
Invalid rating
Invalid quantity
Authorization
Customer ≠ Admin
Error handling
404 → Product not found
401 → Not authenticated
403 → Not authorized
400 → Invalid request
409 → Conflict
Security

Check:

Password hashing
JWT expiration
.env
CORS
SQL injection protection
Sensitive information in responses
🔵 Day 13 — Testing + Documentation

Test the API properly.

Test:

Register
Login
Products
Categories
Cart
Orders
Reviews
Payments
Admin

Use:

Swagger
Postman
pytest

Document the project:

README.md

Include:

Project description
Features
Technologies
Installation
Environment variables
Database setup
API endpoints
Authentication
M-Pesa setup
Running the application
🔵 Day 14 — Final Integration & Deployment

This is the final day.

Connect everything:

React
  ↓
FastAPI
  ↓
MySQL
  ↓
Redis
  ↓
M-Pesa

Then prepare:

Docker
GitHub
Environment variables
Production configuration
Deployment

Final API structure:

/auth
/users

/categories
/products

/cart

/orders
/payments

/reviews

/admin
🎯 What You'll Have After 2 Weeks

Your final project will look something like:

                    E-COMMERCE SYSTEM
                           │
          ┌────────────────┼────────────────┐
          │                │                │
       Customer          Admin           Payment
          │                │                │
          ▼                ▼                ▼
      Products        Dashboard          M-Pesa
          │                │                │
          ▼                ▼                ▼
         Cart          Products          STK Push
          │             Orders            Callback
          ▼                │                │
        Order ◄────────────┴────────────────┘
          │
          ▼
       Reviews
🚀 Skills you'll gain

By the end, you'll have practiced:

Backend

FastAPI
REST APIs
Routers
Dependencies
JWT authentication
RBAC

Database

MySQL
SQLAlchemy
Foreign keys
Relationships
Transactions
Indexing
Aggregations

Advanced

Redis
Caching
Payment APIs
Webhooks/callbacks
API security
Testing

Architecture

Services
Routers
Schemas
Models
Utilities
Environment configuration

DevOps

Git/GitHub
Docker
Deployment

And importantly, we'll not rush through the 14 days. Each day can follow this pattern:

CONCEPT
   ↓
DESIGN
   ↓
IMPLEMENT
   ↓
TEST
   ↓
UNDERSTAND