import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CUSTOMER (
            CUSTOMER_ID integer PRIMARY KEY AUTOINCREMENT,
            NAME TEXT NOT NULL,
            LAST_NAME TEXT NOT NULL,
            BIRTHDATE TEXT NOT NULL,
            DOCUMENT_TYPE TEXT NOT NULL,
            DOCUMENT_NUMBER INTEGER,
            TAX_STATUS TEXT NOT NULL,
            CONSTRAINT CUSTOMER_DOCUMENT_NUMBER_unique UNIQUE ('DOCUMENT_NUMBER')
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CONTRACT (
            CONTRACT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            CUSTOMER_ID INTEGER,
            DESCRIPTION TEXT,
            START_DATE TEXT,
            END_DATE TEXT,
            FOREIGN KEY(CUSTOMER_ID) REFERENCES CUSTOMER(CUSTOMER_ID)
        )
    ''')

    # Creamos la tabla de bancos 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS BANKS (
            BANK_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT,
            UNIQUE (BANK_ID)
        )
    ''')

    # Creamos la tabla de se seguros
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS INSURANCE (
            RISK_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT,
            UNIQUE (RISK_ID)
        )
    ''')

        # Creamos la tabla de marcas de autos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS BRANDS (
            BRAND_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT,
            UNIQUE (BRAND_ID)
        )
    ''')
    conn.commit()
    conn.close()

