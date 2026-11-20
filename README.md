# FridgeMate 🥬

### Smart Refrigerator and Food Inventory Management System

## 📌 About the Project

**FridgeMate** is a web-based refrigerator and food inventory management system designed to help individuals and households organize, monitor, and manage the food stored in their shared refrigerator.

The system aims to reduce food waste, prevent food from expiring unnoticed, and make refrigerator management more convenient. Users can track food items across storage zones, monitor quantities and expiration dates, and manage their refrigerator inventory through a centralized platform.

FridgeMate provides an organized and user-friendly interface that makes managing food supplies easier and more efficient.

## 🎯 Project Objectives

- Provide a centralized platform for managing refrigerator inventory.
- Help users organize items by storage zone (`Fridge`, `Freezer`, and `Pantry / Door`) and monitor quantities and expiration dates.
- Reduce food waste by helping households track stored items before they expire.
- Enforce role-based access control between **Fridge Managers** and **Members**.
- Provide a clean, validated workflow for creating, viewing, updating, and removing food items.

## ✨ Key Features

### 1. User Account Management & Role-Based Access
- User registration, login, and logout.
- Secure password hashing via Django authentication.
- User profile management with contact details and profile photo upload.
- Role-based routing and access control (`Fridge Manager` vs. `Member`).

### 2. Core Feature — Fridge Item Tracking (Food Inventory CRUD)
- **Create:** Add new fridge items (`/fridge-items/add/`) with item name, category, storage zone (`Fridge`, `Freezer`, `Pantry / Door`), quantity, unit, and optional expiration date.
- **Read & Filter:** View tracked food items on the **Food inventory** page (`/fridge-items/`) with storage zone filtering and role-scoped visibility (`Member` views own items; `Fridge Manager` oversees items across users).
- **Update:** Edit existing item details (`/fridge-items/<pk>/edit/`) with server-side validation (non-empty item name, quantity greater than zero, valid zone choices).
- **Delete:** Remove consumed or discarded items (`/fridge-items/<pk>/delete/`) through a confirmation prompt.

### 3. Role-Specific Dashboards
- **Manager Dashboard (`/manager-dashboard/`):** Overview of household inventory and member oversight tools.
- **Member Dashboard (`/member-dashboard/`):** Personal food inventory summary and quick access to add or manage fridge items.

### 4. Expiration Tracking (In Progress)
- Record optional expiration dates per food item.
- Planned upcoming increments: automated expiration status badges, near-expiry alerts, and search/multi-criteria filtering.

## 👥 User Roles

FridgeMate supports two primary user roles:

**Fridge Manager**
- Oversee food inventory across users (`view`, `edit`, and `delete` fridge items).
- Access the Manager Dashboard and administrative tools.
- Manage shared refrigerator operations and household members.

**Member**
- Add new food items to personal inventory.
- View, edit, and delete their own stored food items.
- Monitor item quantities, storage zones, and expiration dates.
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

- Python 3.11+
- PostgreSQL
- Git

### 1. Clone the Repository

```bash
git clone [https://github.com/danemanueldiaquino/FridgeMate-Diaquino-Dan-G5.git](https://github.com/danemanueldiaquino/FridgeMate-Diaquino-Dan-G5.git)
cd FridgeMate-Diaquino-Dan-G5