import pyodbc
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Caminho do banco de dados de fornecedores
DB_PATH_FORNECEDORES = r'G:\Meu Drive\Projetos\BD\fornecedores.accdb'
# Caminho do banco de dados de contas contábeis
DB_PATH_CONTA_CONTABIL = r'G:\Meu Drive\Projetos\BD\conta_contabil.accdb'

# Função para conectar ao banco de dados
def connect_to_database(db_path):
    connection_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + db_path + ';'
    return pyodbc.connect(connection_string)

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para buscar fornecedores
@app.route('/api/supplier', methods=['GET'])
def get_supplier():
    nome = request.args.get('nome', '').strip()
    centro_custo = request.args.get('centro_custo', '').strip()
    uo = request.args.get('uo', '').strip()
    tipo = request.args.get('tipo', '').strip()
    frequencia = request.args.get('frequencia', '').strip()

    try:
        connection = connect_to_database(DB_PATH_FORNECEDORES)
        cursor = connection.cursor()
        
        query = "SELECT [ID Fornecedor], [nome do Fornecedor], [Centro de Custo], [UO], [Tipo], [Frequência], [Conta Contábil] FROM fornecedores WHERE 1=1"
        params = []

        if nome:
            query += " AND [nome do Fornecedor] LIKE ?"
            params.append(f'%{nome}%')

        if centro_custo:
            query += " AND [Centro de Custo] LIKE ?"
            params.append(f'%{centro_custo}%')

        if uo:
            query += " AND [UO] LIKE ?"
            params.append(f'%{uo}%')

        if tipo:
            query += " AND [Tipo] LIKE ?"
            params.append(f'%{tipo}%')

        if frequencia:
            query += " AND [Frequência] LIKE ?"
            params.append(f'%{frequencia}%')

        cursor.execute(query, params)

        suppliers = cursor.fetchall()
        
        results = []
        for supplier in suppliers:
            conta_contabil_desc = get_conta_contabil_desc(supplier[6])  # Chamada para a função de busca da conta contábil
            results.append({
                "id_fornecedor": supplier[0],
                "nome": supplier[1],
                "centro_custo": supplier[2],
                "uo": supplier[3],
                "tipo": supplier[4],
                "frequencia": supplier[5],
                "conta_contabil_desc": conta_contabil_desc  # Adiciona descrição da conta contábil
            })

        cursor.close()
        connection.close()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Função para buscar descrição da conta contábil
def get_conta_contabil_desc(conta_razao):
    try:
        connection = connect_to_database(DB_PATH_CONTA_CONTABIL)
        cursor = connection.cursor()
        
        query_conta = "SELECT DESC_CONTA_RAZAO, DESC_CONTA_RAZAO_ORIGINAL FROM conta_contabil WHERE CONTA_RAZAO = ?"
        cursor.execute(query_conta, (conta_razao,))
        
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if result:
            return {
                "desc_conta_razao": result[0],
                "desc_conta_razao_original": result[1]
            }
        else:
            return None
    except Exception as e:
        return {"error": str(e)}

# Rota para adicionar um novo fornecedor
@app.route('/api/supplier', methods=['POST'])
def add_supplier():
    data = request.get_json()
    try:
        connection = connect_to_database(DB_PATH_FORNECEDORES)
        cursor = connection.cursor()
        query = """
            INSERT INTO fornecedores ([nome do Fornecedor], [Centro de Custo], [UO], [Tipo], [Frequência], [Conta Contábil])
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (data['nome'], data['centro_custo'], data['uo'], data['tipo'], data['frequencia'], data['conta_contabil']))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Fornecedor adicionado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rota para atualizar um fornecedor
@app.route('/api/supplier/<int:supplier_id>', methods=['PUT'])
def update_supplier(supplier_id):
    data = request.get_json()
    try:
        connection = connect_to_database(DB_PATH_FORNECEDORES)
        cursor = connection.cursor()
        query = """
            UPDATE fornecedores SET [nome do Fornecedor] = ?, [Centro de Custo] = ?, [UO] = ?, [Tipo] = ?, [Frequência] = ?, [Conta Contábil] = ?
            WHERE [ID Fornecedor] = ?
        """
        cursor.execute(query, (data['nome'], data['centro_custo'], data['uo'], data['tipo'], data['frequencia'], data['conta_contabil'], supplier_id))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Fornecedor atualizado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rota para exibir a tela de criação de fornecedor
@app.route('/add_supplier')
def add_supplier_page():
    return render_template('add_supplier.html')

# Rota para exibir a tela de edição de fornecedor
@app.route('/edit_supplier/<int:supplier_id>', methods=['GET'])
def edit_supplier(supplier_id):
    try:
        connection = connect_to_database(DB_PATH_FORNECEDORES)
        cursor = connection.cursor()
        
        query = "SELECT [ID Fornecedor], [nome do Fornecedor], [Centro de Custo], [UO], [Tipo], [Frequência], [Conta Contábil] FROM fornecedores WHERE [ID Fornecedor] = ?"
        cursor.execute(query, (supplier_id,))
        
        supplier = cursor.fetchone()
        cursor.close()
        connection.close()

        if supplier:
            return render_template('edit_supplier.html', supplier=supplier)
        else:
            return jsonify({"error": "Fornecedor não encontrado."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)


















