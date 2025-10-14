from flask import Flask, request, jsonify
import sqlite3

from models import init_db

app = Flask(__name__)
init_db()

@app.route('/')
def home():
    return "<h1>Bienvenido a HSS Backend</h1><p>API funcionando correctamente.</p>"

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

#@app.route('/customer', methods=['POST'])
#def crear_cliente():
#    data = request.get_json()
#    conn = get_db_connection()
#    cursor = conn.cursor()
#    cursor.execute('INSERT INTO CUSTOMER (CUSTOMER_ID, NAME, LAST_NAME, BIRTHDATE, DOCUMENT_TYPE, DOCUMENT_NUMBER, TAX_STATUS) VALUES (?, ?, ?, ?, ?, ?, ?)', 
#                   (data['CUSTOMER_ID'], data['NAME'], data['LAST_NAME'], data['BIRTHDATE'], data['DOCUMENT_TYPE'], data['DOCUMENT_NUMBER'], data['TAX_STATUS']))
#    conn.commit()
#    conn.close()
#    return jsonify({'mensaje': 'Cliente creado'}), 201

@app.route('/customer', methods=['POST'])
def crear_clientes():
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({'error': 'Se esperaba una lista de clientes'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    for cliente in data:
        try:
            cursor.execute(
                '''INSERT INTO CUSTOMER 
                   (CUSTOMER_ID, NAME, LAST_NAME, BIRTHDATE, DOCUMENT_TYPE, DOCUMENT_NUMBER, TAX_STATUS) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (
                    cliente['CUSTOMER_ID'],
                    cliente['NAME'],
                    cliente['LAST_NAME'],
                    cliente['BIRTHDATE'],
                    cliente['DOCUMENT_TYPE'],
                    cliente['DOCUMENT_NUMBER'],
                    cliente['TAX_STATUS']
                )
            )
        except Exception as e:
            conn.rollback()
            conn.close()
            return jsonify({'error': f'Error al insertar cliente: {str(e)}'}), 500

    conn.commit()
    conn.close()
    return jsonify({'mensaje': 'Clientes creados correctamente'}), 201

@app.route('/customer/<int:customer_id>', methods=['DELETE'])
def eliminar_cliente(customer_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verificamos si el cliente existe
    cursor.execute('SELECT * FROM CUSTOMER WHERE CUSTOMER_ID = ?', (customer_id,))
    cliente = cursor.fetchone()

    if cliente is None:
        conn.close()
        return jsonify({'error': 'Cliente no encontrado'}), 404

    # Eliminamos el cliente
    cursor.execute('DELETE FROM CUSTOMER WHERE CUSTOMER_ID = ?', (customer_id,))
    conn.commit()
    conn.close()

    return jsonify({'mensaje': f'Cliente con ID {customer_id} eliminado correctamente'}), 200

@app.route('/customer', methods=['GET'])
def listar_cliente():
    conn = get_db_connection()
    CUSTOMER = conn.execute('SELECT * FROM CUSTOMER').fetchall()
    conn.close()
    return jsonify([dict(row) for row in CUSTOMER])

@app.route('/contract', methods=['POST'])
def crear_contrato():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO CONTRACT (CONTRACT_ID, CUSTOMER_ID, DESCRIPTION, START_DATE, END_DATE) VALUES (?, ?, ?, ?, ?)',
                    (data['CUSTOMER_ID'], data['DESCRIPTION'], data['START_DATE'], data['END_DATE']))
    conn.commit()
    conn.close()
    return jsonify({'mensaje': 'Poliza creada'}), 201

@app.route('/contract', methods=['GET'])
def listar_contratos():
    conn = get_db_connection()
    CONTRACT = conn.execute('SELECT * FROM CONTRACT').fetchall()
    conn.close()
    return jsonify([dict(row) for row in CONTRACT])

@app.route('/bank', methods=['GET'])
def listar_bancos():
    conn = get_db_connection()
    bancos = conn.execute('SELECT * FROM BANK').fetchall()
    conn.close()
    return jsonify([dict(row) for row in bancos])

#@app.route('/bank', methods=['POST'])
#def crear_banco():
#    data = request.get_json()
#    conn = get_db_connection()
#    cursor = conn.cursor()
#    cursor.execute('INSERT INTO BANK (BANK_ID, NAME) VALUES (?, ?)', 
#                   (data['BANK_ID'], data['NAME']))
#    conn.commit()
#    conn.close()
#    return jsonify({'mensaje': 'Banco creado'}), 201
#

@app.route('/bank', methods=['POST'])
def crear_banco():
    data = request.get_json()  # Esperamos una lista de diccionarios

    if not isinstance(data, list):
        return jsonify({'error': 'Se esperaba una lista de bancos'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    for banco in data:
        try:
            cursor.execute(
                'INSERT INTO BANK (BANK_ID, NAME) VALUES (?, ?)',
                (banco['BANK_ID'], banco['NAME'])
            )
        except Exception as e:
            conn.rollback()
            conn.close()
            return jsonify({'error': f'Error al insertar banco: {str(e)}'}), 500

    conn.commit()
    conn.close()
    return jsonify({'mensaje': 'Bancos creados correctamente'}), 201


if __name__ == '__main__':
    app.run(debug=True)