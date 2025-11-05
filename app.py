from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

# Criação da aplicação Flask
app = Flask(__name__)

# Configuração da conexão com o banco de dados MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="senac123456789",
    database="biblioteca"
)

# Criar cursor para executar queries
# Usar dictionary=True para receber linhas como dicionários
# Isso permite acessar campos no template via `livro.id` ou `livro['id']`
cursor = db.cursor(dictionary=True)

# 1) ROTA INICIAL
@app.route('/')
def index():
    return render_template('index.html')

# 2) ROTA PARA O FORMULÁRIO
# DE CRIAÇÃO DO LIVRO
@app.route('/criar')
def pagina_criar():
    return render_template('criar.html')

# 3) ROTA PARA CRIAÇÃO DO
# LIVRO NO BANCO DE DADOS
@app.route('/criar/novo', methods=['POST'])
def criar_livro():
    titulo = request.form['titulo']
    ano_publicacao = request.form['ano_publicacao']
    editora = request.form['editora']
    isbn = request.form['isbn']
    
    query = "INSERT INTO livro (titulo, ano_publicacao, editora, isbn) VALUES (%s, %s, %s, %s)"
    values = (titulo, ano_publicacao, editora, isbn)
    
    cursor.execute(query, values)
    db.commit()
    
    return redirect('/')

# 4) ROTA PARA LISTAR
# TODOS OS LIVROS
@app.route('/listar')
def listar():
    cursor.execute("SELECT * FROM livro")
    livros = cursor.fetchall() # fetch all
    return render_template('listar.html', livros=livros)
    # A primeira constante 'livros' refere-se
    # ao retorno do pedido pelo banco de dados.

    # A segunda constante 'livros' será usada
    # na página de listagem de todos os livros

# 5) ROTA PARA EXIBIR O FORMULÁRIO
# DE EDIÇÃO DOS DADOS DO LIVRO
@app.route('/editar/<int:id>')
def pagina_editar(id):
    cursor.execute("SELECT * FROM livro WHERE id = %s", (id,))
    livro = cursor.fetchone() # fetch one
    return render_template('editar.html', livro=livro)

@app.route('/editar/salvar/<int:id>', methods=['POST'])
def editar_livro(id):
    titulo = request.form['titulo']
    ano_publicacao = request.form['ano_publicacao']
    editora = request.form['editora']
    isbn = request.form['isbn']
    
    query = "UPDATE livro SET titulo = %s, ano_publicacao = %s, editora = %s, isbn = %s WHERE id = %s"
    values = (titulo, ano_publicacao, editora, isbn, id)
    
    cursor.execute(query, values)
    db.commit()
    
    return redirect('/listar')

@app.route('/deletar/<int:id>')
def deletar(id):
    cursor.execute("DELETE FROM livro WHERE id = %s", (id,))
    db.commit()
    return redirect('/listar')

# INICIALIZAÇÃO DO SERVIDOR
if __name__ == '__main__':
    app.run(debug=True)