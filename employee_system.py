import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from decimal import Decimal, InvalidOperation

# ================== CONFIG ==================
HOST = "localhost"
POSTGRES_USER = "postgres"       # default postgres user
POSTGRES_PASSWORD = "YourPasswordHere"  # 🔴 CHANGE THIS to your PostgreSQL password
MAIN_DB_NAME = "emp"             # our project database name


# 1) INITIAL SETUP: CREATE DATABASE + TABLE IF NOT EXISTS


def init_database():
    
    print("Initializing database...")

    # Step 1: connect to 'postgres' maintenance DB
    conn = psycopg2.connect(
        host=HOST,
        database="postgres",
        user='postgres',
        password='your_password'
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    try:
        # Check if 'emp' database exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (MAIN_DB_NAME,))
        exists = cur.fetchone()
        if not exists:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(MAIN_DB_NAME)))
            print(f"Database '{MAIN_DB_NAME}' created.")
        else:
            print(f"Database '{MAIN_DB_NAME}' already exists.")
    finally:
        cur.close()
        conn.close()

    # Step 2: connect to 'emp' DB and ensure employees table
    conn2 = psycopg2.connect(
        host=HOST,
        database='emp',
        user='postgres',
        password='your_password'
    )
    cur2 = conn2.cursor()

    try:
        cur2.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                position VARCHAR(100),
                salary NUMERIC(12,2) DEFAULT 0.00
            );
        """)
        conn2.commit()
        print("Table 'employees' is ready.")
    finally:
        cur2.close()
        conn2.close()

    print("Initialization complete.\n")

# 2) CONNECTION FUNCTION


def get_connection():
    """Returns a connection to 'emp' database."""
    return psycopg2.connect(
        host=HOST,
        database='emp',
        user='postgres',
        password='your_password'
    )

# 3) HELPER: CHECK IF EMPLOYEE EXISTS


def check_employee(employee_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM employees WHERE id = %s;", (employee_id,))
        exists = cur.fetchone() is not None
        return exists
    finally:
        cur.close()
        conn.close()


# 4) ADD EMPLOYEE


def add_employee():
    emp_id = input("Enter Employee Id: ").strip()
    if not emp_id:
        print("Employee Id cannot be empty.")
        return

    if check_employee(emp_id):
        print("Employee already exists.")
        return

    name = input("Enter Employee Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    position = input("Enter Employee Position: ").strip()
    salary_str = input("Enter Employee Salary: ").strip()

    try:
        salary = Decimal(salary_str)
    except InvalidOperation:
        print("Invalid salary value.")
        return

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO employees (id, name, position, salary)
            VALUES (%s, %s, %s, %s);
        """, (emp_id, name, position, salary))
        conn.commit()
        print("✅ Employee Added Successfully")
    except Exception as e:
        print("Error while adding employee:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()



# 5) REMOVE EMPLOYEE


def remove_employee():
    emp_id = input("Enter Employee Id to remove: ").strip()

    if not check_employee(emp_id):
        print("Employee does not exist.")
        return

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM employees WHERE id = %s;", (emp_id,))
        conn.commit()
        print("✅ Employee Removed Successfully")
    except Exception as e:
        print("Error while removing employee:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()


# 6) PROMOTE EMPLOYEE (INCREASE SALARY)


def promote_employee():
    emp_id = input("Enter Employee Id to promote: ").strip()

    if not check_employee(emp_id):
        print("Employee does not exist.")
        return

    increase_str = input("Enter increase in salary: ").strip()

    try:
        increase = Decimal(increase_str)
    except InvalidOperation:
        print("Invalid amount.")
        return

    conn = get_connection()
    cur = conn.cursor()

    try:
        # Get current salary
        cur.execute("SELECT salary FROM employees WHERE id = %s;", (emp_id,))
        row = cur.fetchone()
        if not row:
            print("Employee not found unexpectedly.")
            return

        current_salary = row[0]
        new_salary = current_salary + increase

        # Update salary
        cur.execute("UPDATE employees SET salary = %s WHERE id = %s;", (new_salary, emp_id))
        conn.commit()
        print(f"✅ Employee Promoted Successfully. New Salary: {new_salary}")
    except Exception as e:
        print("Error while promoting employee:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()



# 7) DISPLAY ALL EMPLOYEES


def display_employees():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, name, position, salary FROM employees ORDER BY name;")
        rows = cur.fetchall()

        if not rows:
            print("No employees found.")
            return

        print("\n=========== Employee List ===========")
        for emp in rows:
            print("-------------------------------------")
            print("Employee Id :", emp[0])
            print("Name        :", emp[1])
            print("Position    :", emp[2])
            print("Salary      :", emp[3])
        print("-------------------------------------\n")
    except Exception as e:
        print("Error while fetching employees:", e)
    finally:
        cur.close()
        conn.close()



# 8) UPDATE EMPLOYEE DETAILS (NAME / POSITION / SALARY)


def update_employee():
    emp_id = input("Enter Employee Id to update: ").strip()

    if not check_employee(emp_id):
        print("Employee does not exist.")
        return

    print("\nWhat do you want to update?")
    print("1. Name")
    print("2. Position")
    print("3. Salary")
    choice = input("Enter your choice: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        if choice == "1":
            new_name = input("Enter new Name: ").strip()
            if not new_name:
                print("Name cannot be empty.")
                return
            cur.execute("UPDATE employees SET name = %s WHERE id = %s;", (new_name, emp_id))
            print("✅ Name updated successfully.")

        elif choice == "2":
            new_position = input("Enter new Position: ").strip()
            cur.execute("UPDATE employees SET position = %s WHERE id = %s;", (new_position, emp_id))
            print("✅ Position updated successfully.")

        elif choice == "3":
            new_salary_str = input("Enter new Salary: ").strip()
            try:
                new_salary = Decimal(new_salary_str)
            except InvalidOperation:
                print("Invalid salary.")
                return
            cur.execute("UPDATE employees SET salary = %s WHERE id = %s;", (new_salary, emp_id))
            print("✅ Salary updated successfully.")

        else:
            print("Invalid choice.")
            return

        conn.commit()

    except Exception as e:
        print("Error while updating employee:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()



# 9) SEARCH EMPLOYEE BY NAME


def search_employee():
    keyword = input("Enter name keyword to search: ").strip()
    if not keyword:
        print("Search keyword cannot be empty.")
        return

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT id, name, position, salary FROM employees "
            "WHERE name ILIKE %s ORDER BY name;",
            (f"%{keyword}%",)
        )
        rows = cur.fetchall()

        if not rows:
            print("No employees found with that name.")
            return

        print("\nSearch Results:")
        for emp in rows:
            print("------------------------")
            print("Employee Id:", emp[0])
            print("Name       :", emp[1])
            print("Position   :", emp[2])
            print("Salary     :", emp[3])
        print("------------------------")

    except Exception as e:
        print("Error while searching employees:", e)
    finally:
        cur.close()
        conn.close()



# 🔟 MENU


def menu():
    while True:
        print("\nEmployee Management System (PostgreSQL)")
        print("1. Add Employee")
        print("2. Remove Employee")
        print("3. Promote Employee")
        print("4. Display Employees")
        print("5. Update Employee Details")
        print("6. Search Employee")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_employee()
        elif choice == "2":
            remove_employee()
        elif choice == "3":
            promote_employee()
        elif choice == "4":
            display_employees()
        elif choice == "5":
            update_employee()
        elif choice == "6":
            search_employee()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid input. Try again.")



# 1️⃣1️⃣ MAIN ENTRY


if __name__ == "__main__":
    init_database()
    menu()
