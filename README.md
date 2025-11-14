# Employee-Management-System-Python-PostgreSQL

Employee Management System (Python + PostgreSQL)

A database-driven Employee Management System built using **Python** and **PostgreSQL**, providing full CRUD operations with additional features like promotions and search functionality. 
This project demonstrates backend application development, database integration, and structured program logic.

🧾 Features
| Feature | Description |
|---------|-------------|
| ➕ Add Employee | Inserts a new employee record |
| ❌ Remove Employee | Deletes an employee by ID |
| ⬆ Promote Employee | Increases salary |
| 📋 Display Employees | Shows all employee records |
| ✏ Update Employee Details | Edit name, role, or salary |
| 🔍 Search Employee | Search employees by name |
| 🗄 Auto-create Database & Table | Creates DB & table if not found |

🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python |
| Database | PostgreSQL |
| Library | psycopg2 |
| Architecture | CLI Desktop App |

📂 Project Structure
Employee-Management-System-Python-PostgreSQL/
│
├── employee_system.py # Main application
└── README.md # Documentation

yaml
Copy code

 🚀 How to Run This Project

### 1️⃣ Install Dependencies
```bash
pip install psycopg2-binary
2️⃣ Update Database Credentials
Inside employee_system.py, update:

python
Copy code
POSTGRES_PASSWORD = "your_password_here"
3️⃣ Run Application
bash
Copy code
python employee_system.py
