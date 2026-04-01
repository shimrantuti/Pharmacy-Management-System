## PHARMACY-MANAGEMENT-SYSTEM


![Python](https://img.shields.io/badge/python-3.13-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/django-6.0-green?logo=django&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-yellow)
![GitHub stars](https://img.shields.io/github/stars/shimrantuti/Pharmacy-Management-System?style=social)

. A real-world pharmacy workflow simulation built with Django & DRF.

. This project simulates a real‑world pharmacy workflow, built to strengthen my backend and database design skills.
  
. It handles everything from adding medicines to tracking batches, handling low stock status and processing customer         orders.

---


### Database Schema Design

![ER Diagram](https://github.com/user-attachments/assets/68c89bd8-0149-44c8-a54e-d4c627939ac1)

👉 [View interactiveDatabase Schema Design here](https://dbdiagram.io/d/69c2eeeefb2db18e3bf62206)



##  Key Features

###  Inventory Management

. Manage medicines with categories and detailed descriptions

. Track **multiple batches per medicine**

. Monitor **expiry dates** to prevent selling expired stock

###  Smart Stock Handling

. Automatic **stock deduction** when an order is placed.

. Real-time **current quantity tracking**.

. Batch-wise stock management for better accuracy.

###  Order & Billing System

. Create customer orders with multiple medicines.

. Supports **multiple batches for the same medicine**.

. Stores **price at the time of sale** for accurate billing.

###  Supplier & Purchase Management

. Manage suppliers and their details.

. Track purchase orders linked to batches.

. Maintain complete **purchase history**.

###  Advanced Admin Panel

. Powerful Django Admin interface.

. Integrated **TabularInline** for handling multiple items in a single order.

. Perform CRUD operations easily without writing SQL.

---

### Low Stock Alert

. Instant Visibility: Use of emojis (✅, ⚠️, ❌) allows for a quick "at-a-glance" check of inventory levels.

. Proactive Ordering: The Low Stock Alert (⚠️) ensures you restock before a medicine completely runs out.

. Automated Safety: It automatically hides expired batches, ensuring only safe-to-sell stock is shown.

. Zero Manual Work: The status updates itself in real-time, removing the risk of human calculation errors.

. Better Customer Service: Staff can instantly see what is Out of Stock (❌), preventing them from promising unavailable    items.



##  Tech Stack

. **Backend:** Django, Django REST Framework.

. **Database:** SQLite (can be upgraded to PostgreSQL).

. **Language:** Python.

. **Admin UI:** Django Admin Panel.

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




## Future Improvements

. Working on making the Admin Dashboard even more user-friendly.

. Plan to make low stock alert more effective

. Plan to implement REST APIs using DRF for mobile and frontend integration.

. JWT Authentication

. Frontend integration (React)

. Expiry notifications

##  Project Highlights

. Real-world **pharmacy workflow simulation**

. Clean and normalized database design

. Scalable backend using Django REST Framework


---

🛠️TECH STACK AND SKILL

. Backend: Python , Django , Django REST Framework (DRF).

. Database: SQLite, ER Modeling, Database Normalization (1NF, 2NF, 3NF).

. Frontend (Basics): HTML, CSS(Customizing Django Admin UI),Javascript(Basic).

. DevOps & Tools: Git, GitHub, VS Code, Postman (API Testing).

. Learning Goal (Current): Integrating JavaScript/React for a dynamic frontend      


## 🙌 Author

**Shimran Tuti**
Aspiring Full Stack Developer 🚀

GitHub: [https://github.com/shimrantuti](https://github.com/shimrantuti)

##  If you like this project
Give it a ⭐ on GitHub and share your feedback!

---
