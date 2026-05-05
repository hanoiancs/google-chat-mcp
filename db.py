import os
import sqlite3
from auth import google_people_client

db_file_path = os.path.join(os.path.dirname(__file__), "cached/chat_reader.db")
db = sqlite3.connect(db_file_path)
db.row_factory = sqlite3.Row


def init():
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id TEXT PRIMARY KEY,
            name TEXT,
            display_name TEXT,
            email TEXT
        )
        """)
    db.commit()


def get_people():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM people")
    return [dict(row) for row in cursor.fetchall()]


def search_people_by_id(id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM people WHERE id = ?", (id,))
    return dict(cursor.fetchone())


def search_people_by_ids(ids):
    cursor = db.cursor()
    query = f"SELECT * FROM people WHERE id IN ({','.join(['?']*len(ids))})"
    cursor.execute(query, ids)
    return [dict(row) for row in cursor.fetchall()]


def add_person(id, name, display_name, email):
    cursor = db.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO people (id, name, display_name, email) VALUES (?, ?, ?, ?)",
        (id, name, display_name, email),
    )
    db.commit()


def fetch_people(member_ids):
    """
    Fetch people from the database or Google People API if not found in the database.

    Args:
        member_ids: A list of member IDs to fetch.

    Returns:
        A dictionary of people with their IDs as keys.
    """
    existing_people = search_people_by_ids(member_ids)
    people_dict = {p["id"]: p for p in existing_people}
    non_existing_ids = [mid for mid in member_ids if mid not in people_dict]
    if non_existing_ids:
        search_and_insert_people(non_existing_ids)
        updated_people = search_people_by_ids(non_existing_ids)
        for p in updated_people:
            people_dict[p["id"]] = p
    return people_dict
    

def search_and_insert_people(ids):
    searched_google_people = (
        google_people_client.people()
        .getBatchGet(
            resourceNames=[f"people/{member_id}" for member_id in ids],
            personFields="names,emailAddresses",
        )
        .execute()
    )
    people = []
    for person in searched_google_people.get("responses", []):
        person_data = person.get("person", {})
        person_id = person_data.get("resourceName", "").split("/")[-1]
        names = person_data.get("names", [])
        email_addresses = person_data.get("emailAddresses", [])
        if names:
            name = names[0].get("displayName", "")
        else:
            name = ""
        if email_addresses:
            email = email_addresses[0].get("value", "")
        else:
            email = ""
        people.append((person_id, name, name, email))
    add_people(people)


def add_people(people):
    cursor = db.cursor()
    cursor.executemany(
        "INSERT OR REPLACE INTO people (id, name, display_name, email) VALUES (?, ?, ?, ?)",
        people,
    )
    db.commit()


if __name__ == "__main__":
    init()
    # add_person("123", "John Doe", "John", "john@example.com")
    # add_people([
    #     ("456", "Jane Smith", "Jane", "jane@example.com"),
    #     ("789", "Bob Johnson", "Bob", "bob@example.com"),
    # ])
    print([dict(p) for p in get_people()])
    person = dict(search_people_by_id("123"))
    print(person["email"])
    print([dict(p) for p in search_people_by_ids(["123", "456"])])
