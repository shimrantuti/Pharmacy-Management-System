## PHARMACY-MANAGEMENT-SYSTEM


![Python](https://img.shields.io/badge/python-3.13-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/django-6.0-green?logo=django&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-yellow)
![GitHub stars](https://img.shields.io/github/stars/shimrantuti/Pharmacy-Management-System?style=social)

A backend-focused Pharmacy Management System built with Django and Django REST Framework (DRF) to simulate real-world pharmacy inventory, batch management, sales, purchasing, and order workflows.

The system is designed around accurate stock tracking, batch-level inventory control, expiry management, role-based access, and transaction-safe operations.

🚧 Current Status: Backend development is largely complete. React frontend integration is the next development phase.



📌 Overview

Managing medicines is more complex than simply storing a medicine name and quantity.

A real pharmacy may have:

Multiple batches of the same medicine

Different expiry dates

Different quantities across batches

Changing stock after every sale

Customer orders with different statuses

Expired inventory that should not be sold

Different permissions for administrators and sellers

This project models these workflows through a RESTful Django backend with business rules enforced at the application level.


🗃️ Database Design

The system uses a relational database design centered around medicines, batches, suppliers, purchases, and orders.

Main entities

Category

   │
   └── Medicine
   
          │
          └── Batch
          
                 │
                 └── SalesOrderItem
                 
                          │
                          └── Order

Supplier

   │
   └── PurchaseOrder
   
          │
          └── PurchaseInvoice

The database design focuses on:

Relationships between entities

Batch-level inventory tracking

Historical transaction data

Normalized data storage

Referential integrity


### Database Schema Design

![ER Diagram](https://github.com/user-attachments/assets/68c89bd8-0149-44c8-a54e-d4c627939ac1)

👉 [View interactiveDatabase Schema Design here](https://dbdiagram.io/d/69c2eeeefb2db18e3bf62206)



##  Key Features

✨ Key Features

🔐 Authentication & Authorization

JWT-based authentication using Django REST Framework Simple JWT

Protected API endpoints

Role-based access using Django Groups

Separate permissions for ADMIN and SELLER

Sellers can access permitted inventory data without receiving administrative operations

Admin-only expired-batch disposal

💊 Medicine Management

Create and manage medicines

Organize medicines using categories

Store generic name and description

Configure medicine-specific low-stock thresholds

Track total usable stock across batches

📦 Batch-Level Inventory

Multiple batches can belong to the same medicine

Track:

Batch number

Manufacturing date

Expiry date

Purchase price

MRP

Current quantity

Inventory status

Maintain batch-level stock accuracy

Prevent expired batches from being used for sales

📊 Smart Stock Management

The system dynamically identifies:

🟢 Available stock

⚠️ Low-stock medicines

❌ Out-of-stock medicines

⏳ Batches expiring soon

🔴 Expired batches

Expired stock is not counted as usable inventory.

🧾 Sales & Order Management

Orders follow a controlled lifecycle:

DRAFT
  │
  ├── COMPLETED
  │
  └── CANCELLED

The system supports:

Customer name and phone number

Multiple medicines in an order

Multiple batches for the same medicine

Automatic stock deduction

Automatic bill calculation

Sale-time price storage

Order cancellation with stock restoration

Protection against modifying completed/cancelled orders

Protection against changing customer information after order creation

🔄 Multi-Batch Stock Allocation

When a requested quantity cannot be fulfilled from one batch, the system can allocate stock across multiple valid batches.

Example:

Requested: 18 units

Batch A → 10 units
Batch B → 8 units
------------------
Total    → 18 units

Only non-expired batches with available stock are considered.

Batch selection is performed according to expiry order to help prioritize batches with earlier expiry dates.

🗑️ Expired Inventory Disposal

Expired stock can remain in the database for historical purposes while being removed from active inventory.

Inventory follows:

ACTIVE → DISPOSED

Expired batches with remaining stock appear in the expired-batch dashboard

Only ADMIN users can dispose of expired inventory

Disposal does not delete the database record

Historical inventory information is preserved

🏭 Supplier & Purchase Management

Manage suppliers

Create purchase orders

Track purchase invoices

Associate purchased stock with batches

Maintain purchase history

📄 API Pagination

Large API responses use DRF pagination.

Current default:

Page size: 10

This keeps inventory and dashboard responses manageable as the dataset grows.

🧠 Important Business Rules

The backend enforces several rules instead of relying only on the frontend.

Stock cannot become negative

Before selling or modifying an item, the system verifies available batch quantity.

Expired medicines cannot be sold

Only batches whose expiry date is later than the current date are considered usable.

Expired stock does not count as available stock

A medicine is considered out of stock when it has no usable quantity in any non-expired batch.

Completed orders are protected

Once an order is completed, its items cannot be modified.

Cancelled orders are protected

Cancelled orders cannot be modified again.

Customer information is immutable

Customer name and phone number cannot be changed after order creation.

Sale price is preserved

price_at_sale stores the medicine price used during the transaction so that historical billing remains accurate even if the batch MRP changes later.

⚙️ Transaction-Safe Inventory Operations

Inventory changes are handled carefully to prevent inconsistent stock.

The project uses:

transaction.atomic()

select_for_update()

Django F() expressions

These are used for operations such as:

Selling stock

Updating order items

Changing batches

Restoring stock after cancellation

Deleting order items

Multi-batch stock allocation

This helps ensure that related database changes succeed or fail together and reduces the risk of incorrect stock updates during concurrent operations.

📊 Dashboard APIs

The backend provides dedicated endpoints for important inventory conditions.

Endpoint

Purpose

/inventory/batch/out_of_stock/

Medicines with no usable stock

/inventory/batch/expiring_soon/

Batches expiring within 30 days

/inventory/batch/expired/

Expired batches with remaining active stock

/inventory/batch/{id}/dispose/

Admin-only expired-batch disposal

These results are calculated dynamically from the current inventory state.


🛠️ Tech Stack

Category

Technology

Language

Python

Backend

Django 6.0.3

API

Django REST Framework 3.16.1

Authentication

Simple JWT

Database

SQLite

Admin Interface

Django Admin

API Testing

Postman

Version Control

Git & GitHub

Development

VS Code

📁 Project Structure

Pharmacy-Management-System/
│
├── core/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── inventory/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   ├── urls.py
│   └── migrations/
│
├── manage.py
├── requirements.txt
├── README.md
└── db.sqlite3

🚀 Installation & Setup

1. Clone the repository

git clone https://github.com/shimrantuti/Pharmacy-Management-System.git
cd Pharmacy-Management-System

2. Create a virtual environment

python -m venv venv

3. Activate the virtual environment

Windows

venv\Scripts\activate

Linux / macOS

source venv/bin/activate

4. Install dependencies

pip install -r requirements.txt

5. Apply migrations

python manage.py migrate

6. Create an administrator

python manage.py createsuperuser

7. Start the development server

python manage.py runserver

The application will be available at:

http://127.0.0.1:8000/

🔑 Admin Panel

Open:

http://127.0.0.1:8000/admin/

Use the superuser credentials created during setup.

Django Admin can be used to manage core pharmacy data and inspect database records during development.

🧪 API Testing

The REST API can be tested using tools such as Postman.

Authentication flow:

Login
  ↓
Receive JWT access token
  ↓
Send token with protected requests
  ↓
Access permitted API resources

Example authorization header:

Authorization: Bearer <access_token>



## 📷 Screenshots

### Admin Login
![Admin Login](https://github.com/user-attachments/assets/f0fb515a-d2af-4374-8705-5b9c3b338fec)

### Pharmacy Dashboard
![Pharmacy Dashboard](https://github.com/user-attachments/assets/e80ea1f0-8449-44c9-885e-36992a897018)

### Inventory & Batch Management
![Inventory Management](https://github.com/user-attachments/assets/9f87e9e2-df11-44ef-98d9-0a05de6042d4)

### Add Medicine
![Add Medicine](https://github.com/user-attachments/assets/49d3db65-1958-4024-8e20-bd145cf6fdc2)

### Medicine List & Low Stock Alert
![Medicine List](https://github.com/user-attachments/assets/e6500908-79d9-41d4-b33f-70a76f8dde52)

### Purchase Detail Entry
![Purchase Detail](https://github.com/user-attachments/assets/1bfcf224-844c-49a3-b6cf-8a0a63eaa6f7)



🔍 Technical Challenges & Solutions

1. Preventing Incorrect Stock Updates

Problem

Simple stock updates can produce incorrect quantities when multiple database operations affect the same batch.

Solution

The project uses:

transaction.atomic()
select_for_update()
F()

to make stock-changing operations safer and transaction-aware.

2. Selling One Medicine From Multiple Batches

Problem

A requested quantity may exceed the stock available in the selected batch.

Solution

The backend checks subsequent valid batches and allocates the requested quantity across them while maintaining individual batch records.

3. Restoring Stock After Order Cancellation

Problem

Cancelling an order must return its sold quantities to the correct batches.

Solution

The system restores each order item's quantity to its associated batch inside a database transaction.

4. Preventing Expired Stock From Being Sold

Problem

A medicine can still have quantity remaining after its expiry date.

Solution

Sales operations check batch expiry before allocation and only consider valid, non-expired stock.

5. Preserving Historical Sale Prices

Problem

The current MRP of a batch may change after a sale.

Solution

The system stores:

price_at_sale

on every SalesOrderItem.

This keeps historical billing independent of future price changes.

6. Preserving Expired Inventory History

Problem

Deleting expired batches would remove useful historical information.

Solution

Instead of deleting the record, the system changes:

ACTIVE → DISPOSED

This keeps the database history while removing the batch from active inventory.

7. Role-Based Inventory Operations

Problem

Every authenticated user should not be able to perform administrative inventory actions.

Solution

Custom DRF permission classes restrict operations based on authentication and Django Groups.

For example:

SELLER
  ├── View permitted inventory
  ├── View expired batches
  └── Cannot dispose expired stock

ADMIN
  ├── Inventory management
  └── Dispose expired stock

📌 Current Development Status

Completed

Django backend

Django REST Framework APIs

JWT authentication

Role-based permissions

Medicine management

Category management

Supplier management

Purchase management

Batch-level inventory

Multi-batch sales allocation

Automatic stock deduction

Stock restoration on cancellation

Order lifecycle management

Expiry management

Out-of-stock API

Expiring-soon API

Expired-batch API

Admin-only batch disposal

API pagination

In Progress

React frontend

Frontend dashboard

Frontend role-based UI

API integration with React

Planned

Swagger / OpenAPI documentation

Automated backend tests

PostgreSQL configuration

Dockerization

Production deployment

🔮 Future Improvements

Possible future enhancements include:

PostgreSQL for production database workloads

Docker-based development and deployment

Automated testing with Django/DRF test suites

Swagger/OpenAPI documentation

Improved search and filtering

Barcode / QR-based inventory operations

Advanced analytics dashboard

Demand forecasting

Expiry and stock trend analysis

Production deployment

🎯 Project Highlights

This project focuses on backend engineering and real-world business logic, rather than only CRUD operations.

Key learning areas include:

REST API design

Database modeling

Django ORM

DRF serializers and viewsets

JWT authentication

Role-based authorization

Transaction management

Concurrency-aware stock updates

Inventory business rules

Batch-level stock management

API pagination

Git and GitHub workflow   


## 🙌 Author

B.Tech Computer Science & Engineering
BIT Mesra

GitHub: [https://github.com/shimrantuti](https://github.com/shimrantuti)

##  If you like this project
Give it a ⭐ on GitHub and share your feedback!

---
