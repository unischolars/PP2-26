import psycopg2
from config import load_config


def search_by_pattern():
    pattern = input("Enter search pattern (name or phone): ")
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
                rows = cur.fetchall()
                if rows:
                    print(f"\n{'ID':<5} {'First Name':<20} {'Phone':<20}")
                    print("-" * 45)
                    for row in rows:
                        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<20}")
                else:
                    print("No contacts found.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def upsert_contact():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
                conn.commit()
                print("Contact saved successfully.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def bulk_insert():
    contacts = []
    print("Enter contacts (type 'done' to finish):")
    while True:
        name = input("Name: ")
        if name.lower() == 'done':
            break
        phone = input("Phone: ")
        contacts.append((name, phone))

    names = [c[0] for c in contacts]
    phones = [c[1] for c in contacts]

    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL insert_many_contacts(%s, %s)", (names, phones))
                conn.commit()
                print("Bulk insert completed.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def paginated_query():
    page_size = int(input("How many contacts per page? "))
    page_number = int(input("Which page? "))
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (page_size, page_number))
                rows = cur.fetchall()
                if rows:
                    print(f"\n{'ID':<5} {'First Name':<20} {'Phone':<20}")
                    print("-" * 45)
                    for row in rows:
                        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<20}")
                else:
                    print("No contacts on this page.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def delete_contact():
    value = input("Enter name or phone to delete: ")
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_contact(%s)", (value,))
                conn.commit()
                print("Contact deleted successfully.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def main():
    while True:
        print("\n===== PhoneBook Menu =====")
        print("1. Search by pattern")
        print("2. Upsert contact (insert or update)")
        print("3. Bulk insert with validation")
        print("4. View contacts (paginated)")
        print("5. Delete a contact")
        print("6. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            search_by_pattern()
        elif choice == '2':
            upsert_contact()
        elif choice == '3':
            bulk_insert()
        elif choice == '4':
            paginated_query()
        elif choice == '5':
            delete_contact()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")
main()