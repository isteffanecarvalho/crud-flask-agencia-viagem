# Importação dos pacotes
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

# Herdando a classe Flask
app = Flask(__name__)

# Configuração do banco de dados
# Verificando a conexão

try:
    conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='senac123456789',
    database='agenciaviagem'   
    )
    if conexao.is_connected():
        print('Conexão realizada com sucesso')
except OSError as error:
    print('Erro ao conectar: ', error)

# Herdando o método de execução
# dos scripts em SQL

# OBS: nas operações de seleção, os dados
# são recebidos no tipo dicionário
# e a configuração do cursor deve tá
# definida para a leitura do tipo
cursor = conexao.cursor(dictionary=True)

# 1) Rota para acesso
# da página principal da aplicação
@app.route('/')

# Função de definição
# da rota
def index():
    # return "Servidor funcionando"

    # Carregando a página principal
    # da aplicação (index.html)
    return render_template('index.html')

# 2) Rota para criar um novo passageiro
@app.route('/criar', methods=['GET', 'POST'])
def criar():

    # Verificar qual método será
    # usado na operação e atribuir
    # variáveis para receber os valores
    # dos campos de texto (inputs) em criar.html
    if request.method == 'POST':
        nome = request.form['nome']
        dataNascimento = request.form['dataNascimento']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        cpf = request.form['cpf']
        
        # Comando em SQL para criar
        # o passageiro

        # OBS: como no Node.js, os dados a serem recebidos
        # são substituídos por ponto de interrogação, em
        # Python os dados serão recebidos no lugar do %s
        comando = "INSERT INTO passageiros (nome, dataNascimento, endereco, telefone, cpf) VALUES (%s, %s, %s, %s, %s)"
        
        # Variável que irá receber todos
        # os valores das variáveis anteriores
        valores = (nome, dataNascimento, endereco, telefone, cpf)

        # Executar o comando em SQL
        cursor.execute(comando, valores)

        # Confirmar a execução do
        # comando no banco de dados
        conexao.commit()

        # Atribuir um retorno podendo
        # ser o redirecionamento para
        # outra página
        # return redirect(url_for('listar'))
        return redirect('/listar')
    
    # Atribuir um retorno para o
    # carregamento da página de
    # de criação do passageiro
    return render_template('criar.html')

# 3) Rota para listar todos os passageiros
@app.route('/listar')
def listar():

    # Comando em SQl para selecionar
    # os passageiros
    comando = "select * from passageiros"

    # Executar o comando em SQL
    cursor.execute(comando)

    # Variável que irá receber
    # o resultado do comando
    passageiros = cursor.fetchall()
    
    # retornar o resultado
    # carregando em outra página
    return render_template('listar.html', passageiros=passageiros)

    # OBS: a primeira variável 'passageiros' será usada como
    # recebimento do resultado do script em SQL. A segunda
    # vairável 'passageiros' será usada no arquivo listar.html
    # para a leitura dos dados selecionados na página



# 4) Rota para selecionar somente um passageiro
@app.route('/editar/<int:id>', methods=['GET'])

# OBS: como o id será usado como atributo identificador
# para a seleção do passageiro, esse será parâmetro
# da função que ira executar o script em SQL
def selecionar_passageiro(id):
    
    # Comando SQL para selecionar
    # somente um passageiro pelo id
    comando = ""

    # Variável que irá receber 
    # o valor do id do passageiro
    valor = (id,)

    # Executar o comando em SQL
    cursor.execute(comando, valor)

    # Atribuir um variável para o
    # receber o resultado da
    # execução do comando em SQL
    passageiro = cursor.fetchone()
    
    # Retornar o resultado
    # carregando em outra página
    return render_template('editar.html', passageiro=passageiro)

    # OBS: a primeira variável 'passageiro' será usada como
    # recebimento do resultado do script em SQL. A segunda
    # vairável 'passageiro' será usada no arquivo listar.html
    # para a leitura dos dados selecionados na página

# 5) Rota para editar um passageiro
@app.route('/editar-passageiro/<int:id>', methods=['POST'])
def editar(id):
    nome = request.form['nome']
    data_nascimento = request.form['dataNascimento']
    endereco = request.form['endereco']
    telefone = request.form['telefone']
    cpf = request.form['cpf']
    
    # Comando para editar os
    # dados do passageiro
    comando = ""

    # Variável que irá receber todos
    # os valores das variáveis anteriores

    # OBS: a ordem dos valores é o mesmo usado para
    # editar os dados do passageiros no script SQL
    valores = ()

    # Executar o comando
    cursor.execute(comando, valores)
    
    # Confirmar a execução
    # no banco de dados
    conexao.commit()
    
    # Retornar para a
    # página de listagem dos passageiros

    # OBS: o método 'url_for' pede o nome
    # da função ue irá executar a rota
    # que será redirecionada para uma outra página
    return redirect(url_for('listar'))


# 6) Rota para excluir um passageiro
@app.route('/excluir/<int:id>')
def excluir(id):

    # Comando em SQL para excluir
    # a passageiro
    comando = ''
    
    # Variável que irá receber 
    # o valor do id da passageiro
    valor = (id,)
    
    # Executar o comando em SQL
    cursor.execute(comando, valor)
    
    # Confirmar a execução do
    # comando no banco de dados
    conexao.commit()
    
    # Atribuir um retorno podendo
    # ser o redirecionamento para
    # a página de listar os passageiros
    return redirect(url_for(''))

# Execução do servidor
# Nesse modo, o servidor irá
# reiniciar automaticamente após
# mudanças na aplicação principal
if __name__ == '__main__':
    app.run(debug=True)