import mysql.connector


# import argparse

# Make use of argparse to make edits to the database
my_formula = "INSERT INTO transactions (date, description, value, balance, type) VALUES (%s, %s, %s, %s, %s)"
# Array of tuples
transaction_array = [("2020/01/31", "pints", 5.00, 10.00, "Banking"), ("2019/12/31", "food", 5.00, 12.99, "Eating")]

# With dates, from csv, I will have to flip them as year goes first, month, day


def create_database():
    print("Testing connection to database")

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="cashr"  # this specifies the database we are using (none of the defaults, our own)
    )

    print(mydb)

    return mydb


def create_cursor(mydb):
    # Cursor is used as the tool to communicate with the database
    my_cursor = mydb.cursor()
    return my_cursor


def create_db(my_cursor):
    my_cursor.execute("CREATE DATABASE cashr")  # database name is cashr
    print("cashr database created")


def show_dbs(my_cursor):
    print("About to show list of databases")
    my_cursor.execute("SHOW DATABASES")
    for db in my_cursor:
        print(db)
    print("List of databases")
    # Note there are some default databases but cashr is the one we care about


def create_table(my_cursor):
    print("Attempting to create table")
    my_cursor.execute(
        "CREATE TABLE transactions (date DATE, description VARCHAR(255), value FLOAT, balance FLOAT, type VARCHAR(255))")
    print("Table created")


def show_tables(my_cursor):
    print("About to show list of tables in cashr database object")
    my_cursor.execute("SHOW TABLES")
    for tb in my_cursor:
        print(tb)
    print("List of tables")


def drop_table(my_cursor):
    my_cursor.execute("DROP TABLE transactions")


def add_transaction(my_cursor, my_db):
    my_cursor.executemany(my_formula, transaction_array)
    my_db.commit()  # Save changes to the table/database


def get_data(my_cursor):
    my_cursor.execute("SELECT * FROM transactions")
    my_results = my_cursor.fetchall()  # Gets all the values from the last executed statement
    for row in my_results:
        print(row)


def get_data_with_condition(my_cursor):
    my_cursor.execute("SELECT * FROM transactions WHERE type = 'Banking'")
    my_results = my_cursor.fetchall()
    for row in my_results:
        print(row)


def update_transaction(my_cursor, my_db):
    my_cursor.execute("UPDATE transaction SET type = 'Beer' WHERE type = 'bob'")
    my_db.commit()
    # Note tutorial 6 also talks about limiting if thats something of interest to have on my front end


if __name__ == "__main__":
    my_db = create_database()
    my_cursor = create_cursor(my_db)
    # create_db(my_cursor)
    # show_dbs(my_cursor)
    # create_table(my_cursor)
    # drop_table(my_cursor)
    # show_tables(my_cursor)
    # add_transaction(my_cursor, my_db)
    get_data(my_cursor)
    # get_data_with_condition(my_cursor)
    # update_transaction(my_cursor, my_db)
