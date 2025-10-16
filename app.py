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

#con este metodo puedo crear varios clientes a la vez
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
    CUSTOMER = conn.execute('SELECT NAME, LAST_NAME, BIRTHDATE, DOCUMENT_TYPE, DOCUMENT_NUMBER, TAX_STATUS FROM CUSTOMER').fetchall()
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

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#METODOS PARA LA GESTION DE RIESGOS
#CREAR RIESGO
@app.route('/risk', methods=['POST'])
def crear_riesgo():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO RISK (RISK_ID, NAME) VALUES (?, ?)',
                   (data['RISK_ID'], data['NAME']))
    conn.commit()
    conn.close()
    return jsonify({'mensaje': 'Riesgo creado'}), 201

#LISTAR RIESGOS
@app.route('/risk', methods=['GET'])
def listar_riesgos():   
    conn = get_db_connection()
    risks = conn.execute('SELECT * FROM RISK').fetchall()
    conn.close()
    return jsonify([dict(row) for row in risks])    

#ELIMINAR RIESGO    
@app.route('/risk/<int:risk_id>', methods=['DELETE'])
def eliminar_riesgo(risk_id):  
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verificamos si el riesgo existe
    cursor.execute('SELECT * FROM RISK WHERE RISK_ID = ?', (risk_id,))
    riesgo = cursor.fetchone()

    if riesgo is None:
        conn.close()
        return jsonify({'error': 'Riesgo no encontrado'}), 404

    # Eliminamos el riesgo
    cursor.execute('DELETE FROM RISK WHERE RISK_ID = ?', (risk_id,))
    conn.commit()
    conn.close()

    return jsonify({'mensaje': f'Riesgo con ID {risk_id} eliminado correctamente'}), 200

#-------------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#METODOS PARA LA GESTION DE MARCAS DE AUTOS
#CREAR MARCA
@app.route('/brands', methods=['POST'])
def crear_marca():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO BRANDS (NAME) VALUES (?)',
                   (data['NAME'],))
    conn.commit()
    conn.close()
    return jsonify({'mensaje': 'Marca creada'}), 201

#LISTAR MARCAS
@app.route('/brands', methods=['GET'])
def listar_marcas():   
    conn = get_db_connection()
    brands = conn.execute('SELECT * FROM BRANDS').fetchall()
    conn.close()
    return jsonify([dict(row) for row in brands])    

#ELIMINAR MARCA    
@app.route('/brands/<int:brand_id>', methods=['DELETE'])
def eliminar_marca(brand_id):  
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verificamos si la marca existe
    cursor.execute('SELECT * FROM BRANDS WHERE BRAND_ID = ?', (brand_id,))
    marca = cursor.fetchone()

    if marca is None:
        conn.close()
        return jsonify({'error': 'Marca no encontrada'}), 404

    # Eliminamos la marca
    cursor.execute('DELETE FROM BRANDS WHERE BRAND_ID = ?', (brand_id,))
    conn.commit()
    conn.close()

    return jsonify({'mensaje': f'Marca con ID {brand_id} eliminada correctamente'}), 200

@app.route('/dataloadbrand', methods=['POST'])
def crear_marcas():
    data = request.get_json()  # Esperamos una lista de diccionarios

    if not isinstance(data, list):
        return jsonify({'error': 'Se esperaba una lista de marcas'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    for marca in data:
        try:
            cursor.execute(
                'INSERT INTO BRANDS (BRAND_ID, NAME) VALUES (?, ?)',
                (marca['BRAND_ID'], marca['NAME'])
            )
        except Exception as e:
            conn.rollback()
            conn.close()
            return jsonify({'error': f'Error al insertar marca: {str(e)}'}), 500

    conn.commit()
    conn.close()
    return jsonify({'mensaje': 'Marcas creadas correctamente'}), 201

#-------------------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True)