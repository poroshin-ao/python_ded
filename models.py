import sqlite3

def open_connect():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    return connection, cursor

def close_connect(connection):
    connection.commit()
    connection.close()


#user#

def set_user(vk_id, name, fam):
    exec = "INSERT INTO USERS(vk_id, name, fam) VALUES (@0, @1, @2)"

    connection, cursor = open_connect()

    cursor.execute(exec, [vk_id, name, fam])

    close_connect(connection)

def get_user_by_id(vk_id):
    exec = "SELECT name, fam FROM USERS WHERE vk_id = @0"

    connection, cursor = open_connect()

    cursor.execute(exec, [vk_id])
    data = cursor.fetchone()

    close_connect(connection)
    return data

def delete_user_by_id(vk_id):
    exec = "DELETE FROM USERS WHERE vk_id = @0"

    connection, cursor = open_connect()

    cursor.execute(exec, [vk_id])

    close_connect(connection)

def get_alluser():
    exec = "SELECT vk_id, name, fam FROM USERS"

    connection, cursor = open_connect()

    cursor.execute(exec)
    data = cursor.fetchall()

    close_connect(connection)
    return data

#prefer

def set_prefer(vk_id, text):
    exec = "INSERT INTO PREFERS(vk_id, pref) VALUES (@0, @1)"

    connection, cursor = open_connect()

    cursor.execute(exec, [vk_id, text])

    close_connect(connection)

def get_prefer_by_id(vk_id):
    exec = "SELECT pref FROM PREFERS WHERE vk_id = @0"

    connection, cursor = open_connect()

    cursor.execute(exec, [vk_id])
    data = cursor.fetchone()

    close_connect(connection)
    return data

def delete_prefer_by_id(vk_id):
    exec = "DELETE FROM PREFERS WHERE vk_id = @0"

    connection, cursor = open_connect()

    cursor.execute(exec, [vk_id])

    close_connect(connection)


#present

def set_present(vk_id1, vk_id2):
    exec = "INSERT INTO PRESENTS(from_id, to_id) VALUES (@0, @1)"

    connection, cursor = open_connect()

    cursor.execute(exec, [vk_id1, vk_id2])

    close_connect(connection)

def get_present_by_id(vk_id):
    exec = "SELECT to_id FROM PRESENTS WHERE from_id = @0"

    connection, cursor = open_connect()

    cursor.execute(exec, [vk_id])
    data = cursor.fetchone()

    close_connect(connection)
    return data

def get_frompresent_by_id(vk_id):
    exec = "SELECT from_id FROM PRESENTS WHERE to_id = @0"

    connection, cursor = open_connect()

    cursor.execute(exec, [vk_id])
    data = cursor.fetchone()

    close_connect(connection)
    return data

def delete_present_by_id(vk_id):
    exec = "DELETE FROM PRESENTS WHERE from_id = @0"

    connection, cursor = open_connect()

    cursor.execute(exec, [vk_id])

    close_connect(connection)


#givers
def set_giver(vk_id):
    exec = "INSERT INTO GIVERS(vk_id) VALUES (@0)"

    connection, cursor = open_connect()

    cursor.execute(exec, [vk_id])

    close_connect(connection)

def get_giver_by_id(vk_id):
    exec = "SELECT vk_id FROM GIVERS WHERE vk_id = @0"

    connection, cursor = open_connect()

    cursor.execute(exec, [vk_id])
    data = cursor.fetchone()

    close_connect(connection)
    return data
