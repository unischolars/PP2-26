import csv
import json
from connect import get_connection 


def run_sql_file(filename):
    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        cur.execute(file.read())  # read the file and run it

    conn.commit()
    cur.close()
    conn.close()
    print(f"{filename} executed successfully.")


def get_group_id(cur, group_name):
    cur.execute("SELECT id FROM groups WHERE name = %s;", (group_name,))
    group = cur.fetchone()

    if group:
        return group[0]

    # group doesnt exist so we create it
    cur.execute("INSERT INTO groups(name) VALUES(%s) RETURNING id;", (group_name,))
    return cur.fetchone()[0]


def print_rows(rows):
    if not rows:
        print("No data found.")
        return

    for row in rows:
        print(row)


def add_contact():
    # ask user for contact info
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    birthday = input("Birthday YYYY-MM-DD: ").strip()
    group_name = input("Group: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    group_id = get_group_id(cur, group_name)  # get or create the group

    cur.execute("""
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """, (name, email, birthday, group_id))

    contact_id = cur.fetchone()[0]

    # keep asking for phone numbers until user leaves it empty
    while True:
        phone = input("Phone number (empty to stop): ").strip()
        if phone == "":
            break

        phone_type = input("Type home/work/mobile: ").strip()

        cur.execute("""
            INSERT INTO phones(contact_id, phone, type)
            VALUES (%s, %s, %s);
        """, (contact_id, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()
    print("Contact added.")


def add_phone_to_contact():
    name = input("Contact name: ").strip()
    phone = input("New phone: ").strip()
    phone_type = input("Type home/work/mobile: ").strip()

    conn = get_connection()
    cur = conn.cursor()
    # call the stored procedure in the database
    cur.execute("CALL add_phone(%s, %s, %s);", (name, phone, phone_type))
    conn.commit()
    cur.close()
    conn.close()
    print("Phone added if contact exists and type is valid.")


def move_contact_to_group():
    name = input("Contact name: ").strip()
    group = input("New group: ").strip()

    conn = get_connection()
    cur = conn.cursor()
    # call the stored procedure to move the contact
    cur.execute("CALL move_to_group(%s, %s);", (name, group))
    conn.commit()
    cur.close()
    conn.close()
    print("Contact moved if contact exists.")


def show_contacts():
    conn = get_connection()
    cur = conn.cursor()
    # join all three tables to get full contact info
    cur.execute("""
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            p.phone,
            p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        ORDER BY c.id;
    """)
    print_rows(cur.fetchall())
    cur.close()
    conn.close()


def search_contacts():
    query = input("Search text: ").strip()

    conn = get_connection()
    cur = conn.cursor()
    # use the database function to search
    cur.execute("SELECT * FROM search_contacts(%s);", (query,))
    print_rows(cur.fetchall())
    cur.close()
    conn.close()


def filter_by_group():
    group = input("Group name: ").strip()

    conn = get_connection()
    cur = conn.cursor()
    # only show contacts that belong to this group
    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE g.name = %s
        ORDER BY c.name;
    """, (group,))
    print_rows(cur.fetchall())
    cur.close()
    conn.close()


def search_by_email():
    email = input("Email search: ").strip()

    conn = get_connection()
    cur = conn.cursor()
    # ilike means case insensitive, % means any characters around the input
    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        WHERE c.email ILIKE %s
        ORDER BY c.name;
    """, (f"%{email}%",))
    print_rows(cur.fetchall())
    cur.close()
    conn.close()


def sort_contacts():
    print("1 - Sort by name")
    print("2 - Sort by birthday")
    print("3 - Sort by date added")
    choice = input("Choose: ").strip()

    # only allow these columns to avoid sql injection
    allowed_orders = {
        "1": "c.name",
        "2": "c.birthday",
        "3": "c.created_at"
    }

    order = allowed_orders.get(choice)
    if order is None:
        print("Invalid choice.")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT c.name, c.email, c.birthday, g.name, c.created_at
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY {order};
    """)
    print_rows(cur.fetchall())
    cur.close()
    conn.close()


def paginated_contacts():
    page = 0
    limit = 5  # show 5 contacts per page

    while True:
        conn = get_connection()
        cur = conn.cursor()
        # pass limit and current page number to the database function
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, page + 1))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        print(f"\nPage {page + 1}")
        print_rows(rows)

        command = input("next / prev / quit: ").strip().lower()
        if command == "next":
            page += 1
        elif command == "prev":
            page = max(0, page - 1)  # dont go below page 0
        elif command == "quit":
            break
        else:
            print("Invalid command.")


def import_from_csv():
    filename = input("CSV filename: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)  # reads each row as a dictionary
        for row in reader:
            group_id = get_group_id(cur, row["group"])

            # if name already exists then update their info instead of failing
            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (name) DO UPDATE
                SET email = EXCLUDED.email,
                    birthday = EXCLUDED.birthday,
                    group_id = EXCLUDED.group_id
                RETURNING id;
            """, (row["name"], row["email"], row["birthday"], group_id))

            contact_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s);
            """, (contact_id, row["phone"], row["type"]))

    conn.commit()
    cur.close()
    conn.close()
    print("CSV imported.")


def export_to_json():
    filename = input("JSON filename: ").strip()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.id;
    """)
    contacts = cur.fetchall()

    result = []
    for contact in contacts:
        contact_id = contact[0]
        cur.execute("SELECT phone, type FROM phones WHERE contact_id = %s;", (contact_id,))
        phones = cur.fetchall()

        result.append({
            "name": contact[1],
            "email": contact[2],
            "birthday": str(contact[3]) if contact[3] else None,  # convert date to string
            "group": contact[4],
            "phones": [{"phone": p[0], "type": p[1]} for p in phones]
        })

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)  # write pretty json

    cur.close()
    conn.close()
    print("Exported to JSON.")


def import_from_json():
    filename = input("JSON filename: ").strip()

    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    conn = get_connection()
    cur = conn.cursor()

    for item in data:
        # check if this contact already exists
        cur.execute("SELECT id FROM contacts WHERE name = %s;", (item["name"],))
        existing = cur.fetchone()

        if existing:
            print(f"Contact {item['name']} already exists.")
            choice = input("skip or overwrite? ").strip().lower()

            if choice == "skip":
                continue
            elif choice == "overwrite":
                cur.execute("DELETE FROM contacts WHERE name = %s;", (item["name"],))
            else:
                print("Invalid choice, skipped.")
                continue

        group_id = get_group_id(cur, item["group"])

        cur.execute("""
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """, (item["name"], item["email"], item["birthday"], group_id))

        contact_id = cur.fetchone()[0]

        # insert all phones from the json
        for phone in item["phones"]:
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s);
            """, (contact_id, phone["phone"], phone["type"]))

    conn.commit()
    cur.close()
    conn.close()
    print("JSON imported.")


def delete_contact():
    name = input("Contact name to delete: ").strip()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE name = %s;", (name,))
    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted if it existed.")


def menu():
    while True:  # keep showing the menu until user exits
        print("\n--- PHONEBOOK MENU ---")
        print("1. Create tables")
        print("2. Create procedures/functions")
        print("3. Add contact")
        print("4. Add phone to contact")
        print("5. Move contact to group")
        print("6. Show all contacts")
        print("7. Search contacts")
        print("8. Filter by group")
        print("9. Search by email")
        print("10. Sort contacts")
        print("11. Pagination")
        print("12. Import from CSV")
        print("13. Export to JSON")
        print("14. Import from JSON")
        print("15. Delete contact")
        print("16. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            run_sql_file("schema.sql")
        elif choice == "2":
            run_sql_file("procedures.sql")
        elif choice == "3":
            add_contact()
        elif choice == "4":
            add_phone_to_contact()
        elif choice == "5":
            move_contact_to_group()
        elif choice == "6":
            show_contacts()
        elif choice == "7":
            search_contacts()
        elif choice == "8":
            filter_by_group()
        elif choice == "9":
            search_by_email()
        elif choice == "10":
            sort_contacts()
        elif choice == "11":
            paginated_contacts()
        elif choice == "12":
            import_from_csv()
        elif choice == "13":
            export_to_json()
        elif choice == "14":
            import_from_json()
        elif choice == "15":
            delete_contact()
        elif choice == "16":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()