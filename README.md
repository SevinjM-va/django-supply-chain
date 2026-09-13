# Warehouse Management System

A REST API for automated warehouse management built with Django and Django REST Framework.

## Project Overview

The system allows suppliers to add products to warehouses and consumers to take products from warehouses.

The application provides role-based access control and JWT authentication.

## Main Features

* User registration and authentication
* JWT-based authentication
* Supplier and consumer roles
* Warehouse management
* Product management
* Adding products to warehouse stock
* Taking products from warehouse stock
* Stock quantity validation
* Role-based permissions
* Automated API tests

## Technologies

* Python
* Django
* Django REST Framework
* Simple JWT
* SQLite
* REST API

## API Endpoints

| Method   | Endpoint               | Description              |
| -------- | ---------------------- | ------------------------ |
| POST     | `/api/register/`       | Register a new user      |
| POST     | `/api/login/`          | Get JWT tokens           |
| POST     | `/api/token/refresh/`  | Refresh JWT token        |
| GET/POST | `/api/warehouses/`     | Manage warehouses        |
| GET/POST | `/api/products/`       | Manage products          |
| POST     | `/api/stocks/supply/`  | Add products to stock    |
| POST     | `/api/stocks/consume/` | Take products from stock |

## User Roles

### Supplier

A supplier can add products to warehouse stock.

### Consumer

A consumer can take products from warehouse stock.

The system prevents consumers from adding products and prevents users from taking more products than are currently available.

## Installation

Clone the repository:

```bash
git clone https://github.com/SevinjM-va/django-supply-
```
