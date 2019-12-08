import mysql.connector
import json


my_formula = "INSERT INTO transactions (date, description, value, balance, type) VALUES (%s, %s, %s, %s, %s)"
# Array of tuples
transaction_array = [("2020/01/31", "pints", 5.00, 10.00, "Banking"), ("2019/12/31", "food", 5.00, 12.99, "Eating")]

# With dates, from csv, I will have to flip them as year goes first, month, day


def connect_to_database():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="cashr"  # this specifies the database we are using (none of the defaults, our own)
    )

    return mydb


def get_cursor(mydb):
    # Cursor is used as the tool to communicate with the database
    return mydb.cursor()


def create_db():
    my_db = connect_to_database()
    my_cursor = get_cursor(my_db)

    my_cursor.execute("CREATE DATABASE cashr")  # database name is cashr
    print("cashr database created")


def show_dbs():
    my_db = connect_to_database()
    my_cursor = get_cursor(my_db)

    print("About to show list of databases")
    my_cursor.execute("SHOW DATABASES")
    for db in my_cursor:
        print(db)
    print("List of databases")
    # Note there are some default databases but cashr is the one we care about


def create_table():
    my_db = connect_to_database()
    my_cursor = get_cursor(my_db)

    print("Attempting to create table")
    my_cursor.execute(
        "CREATE TABLE transactions (date DATE, description VARCHAR(255), value FLOAT, balance FLOAT, type VARCHAR(255))")
    print("Table created")


def show_tables():
    my_db = connect_to_database()
    my_cursor = get_cursor(my_db)

    print("About to show list of tables in cashr database object")
    my_cursor.execute("SHOW TABLES")
    for tb in my_cursor:
        print(tb)
    print("List of tables")


def drop_table():
    my_db = connect_to_database()
    my_cursor = get_cursor(my_db)

    my_cursor.execute("DROP TABLE transactions")


def add_transaction(balance, date, description, type, value):
    my_db = connect_to_database()
    my_cursor = get_cursor(my_db)

    transaction_tuple = [(date, description, value, balance, type)]

    my_cursor.executemany(my_formula, transaction_tuple)
    my_db.commit()  # Save changes to the table/database


def get_transactions():
    my_db = connect_to_database()
    my_cursor = get_cursor(my_db)

    my_cursor.execute("SELECT * FROM transactions")
    row_headers = [x[0] for x in my_cursor.description]  # this will extract row headers
    rv = my_cursor.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json_data


def get_data_with_condition():
    my_db = connect_to_database()
    my_cursor = get_cursor(my_db)

    my_cursor.execute("SELECT * FROM transactions WHERE type = 'Banking'")
    my_results = my_cursor.fetchall()
    for row in my_results:
        print(row)


def update_transaction():
    my_db = connect_to_database()
    my_cursor = get_cursor(my_db)

    my_cursor.execute("UPDATE transaction SET type = 'Beer' WHERE type = 'bob'")
    my_db.commit()
    # Note tutorial 6 also talks about limiting if thats something of interest to have on my front end
