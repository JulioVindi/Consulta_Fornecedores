import pyodbc

# Caminho do seu banco de dados Access
DATABASE_PATH = r'C:\Users\julio.heredia_vindi\Projetos\Consulta de fornecedor\conta_contabil.accdb'

# String de conexão ODBC
connection_string = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=' + DATABASE_PATH + ';'
)

# Tentativa de conexão
try:
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Exemplo de consulta para verificar a conexão
    cursor.execute("SELECT * FROM Conta_contabil")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()

except pyodbc.Error as e:
    print(f"Erro de conexão: {e}")
