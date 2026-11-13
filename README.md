# FridgeMate 🥬

### Smart Refrigerator and Food Inventory Management System

## 📌 About the Project

**FridgeMate** is a web-based refrigerator and food inventory management system designed to help individuals and households organize, monitor, and manage the food stored in their shared refrigerator.

The system aims to reduce food waste, prevent food from expiring unnoticed, and make refrigerator management more convenient. Users can keep track of their food items, monitor expiration dates, and manage their shared refrigerator inventory through a centralized platform.

FridgeMate provides an organized and user-friendly interface that makes managing food supplies easier and more efficient.

## 🎯 Project Objectives

- Provide a centralized platform for managing refrigerator inventory.
- Help users monitor food expiration dates.
- Reduce food waste by reminding users about items nearing expiration.
- Allow multiple users to access and manage a shared refrigerator.
- Provide a convenient way to organize and track stored food items.

## ✨ Key Features

### 1. User Account Management
- User registration and login.
- Secure password handling.
- User profile management.
- Role-based access control.

### 2. Refrigerator Management
- Manage shared refrigerator information.
- Organize food items stored in the refrigerator.
- Allow authorized users to manage refrigerator members.

### 3. Food Inventory Management
- Add new food items.
- View and organize stored food products.
- Update food item information.
- Remove items that are no longer stored in the refrigerator.
- Monitor available food quantities.

### 4. Expiration Tracking
- Record expiration dates of food items.
- Identify items approaching their expiration dates.
- Help users prioritize food that should be consumed first.

### 5. Dashboard
- View an overview of refrigerator inventory.
- Monitor food items and their quantities.
- Display important expiration reminders.
- Provide quick access to frequently used features.

## 👥 User Roles

FridgeMate is designed with two primary user roles:

**Fridge Manager**
- Manage the shared refrigerator.
- Manage refrigerator members.
- Oversee the food inventory.
- Monitor food expiration information.

**Member**
- View shared refrigerator inventory.
- Add and manage food items according to their permissions.
- Monitor expiration dates.
- Update personal account information.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Django | Backend web framework |
| PostgreSQL | Relational database management |
| HTML5 | Webpage structure |
| CSS3 | Styling and layout |
| JavaScript | Frontend interactivity |
| Git and GitHub | Version control and project collaboration |

## ⚙️ Installation and Setup

Follow these steps to run FridgeMate on your local computer.

### Prerequisites

Make sure the following are installed:

- Python
- PostgreSQL
- Git
- Visual Studio Code

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate to the project folder:

```bash
cd FridgeMate
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Environment Variables

Create a `.env` file in the root directory and configure your local database credentials.

Example:

```env
SECRET_KEY=your_django_secret_key
DEBUG=True

DB_NAME=fridgemate_db
DB_USER=fridgemate_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Create and Configure the Database

Create a PostgreSQL database named:

```sql
CREATE DATABASE fridgemate_db;
```

Make sure the database credentials match your `.env` configuration.

### 6. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create an Administrator Account

```bash
python manage.py createsuperuser
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

## 📁 Project Structure

The project follows Django's application-based structure. Its general organization may look like this:

```text
FridgeMate/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
│
├── templates/
├── static/
├── media/
│
├── manage.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

*Note: The structure may change as additional applications and features are developed.*

## 🔐 Security and Data Protection

FridgeMate follows basic web application security practices:

- Passwords are securely hashed using Django authentication.
- User access is controlled through authentication and role-based permissions.
- Environment variables are used to store sensitive configuration.
- Database credentials and secret keys should not be committed to the public repository.

## 🚀 Project Status

**Development Status:** In Development

FridgeMate is being developed incrementally, beginning with account management, authentication, and role-based access control. Additional refrigerator management, inventory, and expiration tracking features will be implemented as development progresses.

## 👨‍💻 Project Information

**Project Name:** FridgeMate  
**Project Type:** Web-Based Application  
**Category:** Food Inventory and Refrigerator Management  
**Framework:** Django  
**Database:** PostgreSQL

---

*FridgeMate — Making food management smarter, easier, and more organized.*
