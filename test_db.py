import psycopg2

try:
    conn = psycopg2.connect(
        dbname="pidomas",
        user="postgres",
        password="malacca87",
        host="127.0.0.1",
        port="5432"
    )
    print("¡Conexión exitosa!")
    conn.close()
except Exception as e:
    print(f"Error de conexión: {e}") 