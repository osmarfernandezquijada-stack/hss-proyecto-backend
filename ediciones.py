
import sqlite3
# Conexión a la base de datos (o crea una si no existe)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()


#cursor.execute("DELETE FROM brands WHERE brand_id = 5")
#conn.commit()


#id_a_eliminar = 6
#cursor.execute("DELETE FROM brands WHERE brand_id = ?", (id_a_eliminar,))
#conn.commit()


cursor.execute("DELETE FROM brands")
conn.commit()
cursor.execute("VACUUM")  # Limpia la base y reinicia IDs


print("Registros eliminados correctamente.")
conn.close()

