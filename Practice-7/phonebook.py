import psycopg2
import csv
from config import load_config


# Create Table

def create_table():
    command = """
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL UNIQUE
        )
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(command)
                conn.commit()
                print("Table created successfully.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


#insert cvs
def insert_from_csv(s=r"C:\Users\rozao\Pop\work\Practice-7\contacts.csv"):
    sql = "INSERT INTO phonebook(first_name, phone) VALUES(%s, %s) ON CONFLICT (phone) DO NOTHING"
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open(s, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        cur.execute(sql, (row['first_name'], row['phone']))
                conn.commit()
                print("Contacts inserted from CSV successfully.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


# Insert from Console
def insert_from_console():
    first_name = input("Enter first name: ")
    phone = input("Enter phone number: ")

    sql = "INSERT INTO phonebook(first_name, phone) VALUES(%s, %s) ON CONFLICT (phone) DO NOTHING"
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (first_name, phone))
                conn.commit()
                print(f"Contact '{first_name}' added successfully.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


# 4. Update Contact
def update_contact():
    print("Search contact to update:")
    search = input("Enter current first name or phone: ")

    print("What do you want to update?")
    print("1. First name")
    print("2. Phone number")
    choice = input("Enter choice (1 or 2): ")

    if choice == '1':
        new_value = input("Enter new first name: ")
        sql = "UPDATE phonebook SET first_name = %s WHERE first_name = %s OR phone = %s"
    elif choice == '2':
        new_value = input("Enter new phone number: ")
        sql = "UPDATE phonebook SET phone = %s WHERE first_name = %s OR phone = %s"
    else:
        print("Invalid choice.")
        return

    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (new_value, search, search))
                conn.commit()
                if cur.rowcount > 0:
                    print("Contact updated successfully.")
                else:
                    print("No contact found.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


# 5. Query / Search Contacts
def query_contacts():
    print("Search by:")
    print("1. First name")
    print("2. Phone prefix")
    print("3. Show all")
    choice = input("Enter choice (1, 2, or 3): ")

    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                if choice == '1':
                    name = input("Enter name to search: ")
                    cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s", (f'%{name}%',))
                elif choice == '2':
                    prefix = input("Enter phone prefix to search: ")
                    cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (f'{prefix}%',))
                elif choice == '3':
                    cur.execute("SELECT * FROM phonebook ORDER BY first_name")
                else:
                    print("Invalid choice.")
                    return

                rows = cur.fetchall()
                if rows:
                    print(f"\n{'ID':<5} {'First Name':<20} {'Phone':<20}")
                    for row in rows:
                        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<20}")
                else:
                    print("No contacts found.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

# 6. Delete Contact
def delete_contact():
    print("Delete by:")
    print("1. First name")
    print("2. Phone number")
    choice = input("Enter choice (1 or 2): ")

    if choice == '1':
        value = input("Enter first name to delete: ")
        sql = "DELETE FROM phonebook WHERE first_name = %s"
    elif choice == '2':
        value = input("Enter phone number to delete: ")
        sql = "DELETE FROM phonebook WHERE phone = %s"
    else:
        print("Invalid choice.")
        return

    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (value,))
                conn.commit()
                if cur.rowcount > 0:
                    print("Contact deleted successfully.")
                else:
                    print("No contact found.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


# Main Menu
def main():
    create_table()
    while True:
        print("\n===== PhoneBook Menu =====")
        print("1. Insert contacts from CSV")
        print("2. Insert contact from console")
        print("3. Update a contact")
        print("4. Search contacts")
        print("5. Delete a contact")
        print("6. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            insert_from_csv()
        elif choice == '2':
            insert_from_console()
        elif choice == '3':
            update_contact()
        elif choice == '4':
            query_contacts()
        elif choice == '5':
            delete_contact()
        elif choice == '6':
            break
        else:
            print("Invalid choice, try again.")

main()