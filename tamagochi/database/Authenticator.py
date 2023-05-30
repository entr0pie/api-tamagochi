#!/bin/python

from typing import Dict, Tuple

from sqlite3 import connect
from bcrypt import gensalt, hashpw, checkpw

DATABASE_PATH = "database/database.db"

def authParent(user: str, password: str) -> bool:
    c = connect(DATABASE_PATH).cursor()
    
    c.execute('SELECT password FROM parent WHERE email = ?', (user,))
    user_data = c.fetchone()
    
    if user_data:
        if checkpw(password.encode('utf-8'), user_data[0]):
            return True
    
    return False

def registerParent(email: str, name: str, surname: str, password: str, genre: str) -> bool:
    password = hashPassword(password)

    conn = connect(DATABASE_PATH)
    conn.execute('INSERT INTO parent (email, name, sobrename, password, gender) VALUES (?, ?, ?, ?, ?)',
                (email, name, surname, password, genre))

    conn.commit()

    return True 

def checkPostRequest(data: Dict[str, str], required_keys: Tuple[str], optional_keys: Tuple[str]=()) -> bool:
    """Check if the content of a POST request matches with the 
    expected fields and values. 
    
    The 'data' argument refers to the JSON POST content,
    usually gotten via request.get_json() Flask method.

    The 'required_keys' is a tuple that needs to be in a  
    specific request (example: ('user', 'password'))

    The 'optional_keys' stores the optional keys available for that
    request (example: ('is_robot'))

    * Check if this function is really necessary *
    """

    all_keys = required_keys + optional_keys

    data_keys = data.keys()
    
    for r_key in required_keys:
        if r_key not in data_keys:
            return False

    for d_key in data_keys:
        if d_key not in all_keys:
            return False

    return True
