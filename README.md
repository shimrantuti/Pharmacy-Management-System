Pharmacy Management System

I built this system to learn how real-world pharmacy inventory works.
It handles everything from adding medicines to tracking batches and processing customer orders.

---

**ER Diagram

erDiagram
    CATEGORY ||--o{ MEDICINE : "groups"
    SUPPLIER ||--o{ PURCHASEORDER : "provides"
    PURCHASEORDER ||--o{ BATCH : "receives"
    MEDICINE ||--o{ BATCH : "has_multiple"
    ORDER ||--o{ ORDER_ITEM : "contains"
    BATCH ||--o{ ORDER_ITEM : "sold_from"

    MEDICINE {
        string medicine_name
        string generic_name
    }
    BATCH {
        string batch_no
        date expiry_date
        int current_quantity
    }
    PURCHASEORDER {
        date purchase_date
        decimal total_amount
    }
    ORDER {
        string customer_name
        datetime timestamp
    }
##  Key Features

###  Inventory Management

* Manage medicines with categories and detailed descriptions
* Track **multiple batches per medicine**
* Monitor **expiry dates** to prevent selling expired stock

###  Smart Stock Handling

* Automatic **stock deduction** when an order is placed
* Real-time **current quantity tracking**
* Batch-wise stock management for better accuracy

###  Order & Billing System

* Create customer orders with multiple medicines
* Supports **multiple batches for the same medicine**
* Stores **price at the time of sale** for accurate billing

###  Supplier & Purchase Management

* Manage suppliers and their details
* Track purchase orders linked to batches
* Maintain complete **purchase history**

###  Advanced Admin Panel

* Powerful Django Admin interface
* Integrated **TabularInline** for handling multiple items in a single order
* Perform CRUD operations easily without writing SQL

---

##  Tech Stack

* **Backend:** Django, Django REST Framework
* **Database:** SQLite (can be upgraded to PostgreSQL)
* **Language:** Python
* **Admin UI:** Django Admin Panel

---

## ⚙️ Installation & Setup

### 1 Clone the repository

```bash
git clone https://github.com/shimrantuti/Pharmacy-Management-System.git
cd Pharmacy-Management-System
```

### 2️ Create virtual environment

```bash
python -m venv venv
```

### 3️ Activate virtual environment

```bash
# For Windows
venv\Scripts\activate
```

### 4️ Install dependencies

```bash
pip install -r requirements.txt
```

### 5️ Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️ Run server

```bash
python manage.py runserver
```

---

##  Admin Access

Create a superuser:

```bash
python manage.py createsuperuser
```

Then open:

```
http://127.0.0.1:8000/admin/
```

---

##  Future Improvements

* I'm currently working on adding Low Stock Alerts because it's a must-have for pharmacies.
* Working on making the Admin Dashboard even more user-friendly.
* Plan to implement REST APIs using DRF for mobile and frontend integration.
* JWT Authentication
* Frontend integration (React)
* Expiry notifications

---

## 📷 Screenshots

### Dashboard Overview
![Login Page](https://github.com/user-attachments/assets/07951ef6-c8f7-4346-b217-33a3321b8fe2)

###  Admin Login
![Pharmacy Dashboard](https://github.com/user-attachments/assets/b093a3ff-2f2f-465c-bfa7-6f9f1fb457d2)

###  Inventory & Batch Management
![Inventory Management](https://github.com/user-attachments/assets/7a129264-7016-4d4c-84e0-27b305885121)

###  Order Processing (Tabular Inline)
![Order Processing](https://github.com/user-attachments/assets/3e31e504-7200-4b8a-ad34-a7c0ed927421)


## Future Improvements

* I'm currently working on adding Low Stock Alerts because it's a must-have for pharmacies.
* Working on making the Admin Dashboard even more user-friendly.
* Plan to implement REST APIs using DRF for mobile and frontend integration.
* JWT Authentication
* Frontend integration (React)
* Expiry notifications

##  Project Highlights

* Real-world **pharmacy workflow simulation**
* Clean and normalized database design
* Scalable backend using Django REST Framework


---

## 🙌 Author

**Shimran Tuti**
Aspiring Full Stack Developer 🚀

GitHub: [https://github.com/shimrantuti](https://github.com/shimrantuti)

##  If you like this project
Give it a ⭐ on GitHub and share your feedback!

---
