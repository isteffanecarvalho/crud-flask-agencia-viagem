# Importação dos pacotes
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

# Herdando a classe Flask
app = Flask(__name__)

# Configurando uma chave
# secreta para a sessão
app.secret_key = '36eertu76kw4tshuy045w25bfgj6'

# Função para desativar o cache nas páginas
@app.after_request
def add_header(response):
    """
    Desativa o cache nas páginas para evitar que o botão de "voltar" acesse páginas protegidas
    após o logout.
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

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
    # da aplicação (login.html)
    return render_template('login.html')

# 2) Rota para carregar a página
# de início do usuário
@app.route(' /inicio')
def inicio():

    return render_template('index.html')
  # Protegendo a rota
    # se o usuário não estiver logado
    if 'id_usuario' not in session:
        return redirect('/')


# 3) Rota para criar um novo passageiro
@app.route('/criar', methods=['GET', 'POST'])
def criar():
    
    # Protegendo a rota
    # se o usuário não estiver logado
    if 'id_usuario' not in session:
        return redirect('/')

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

# 4) Rota para listar todos os passageiros
@app.route('/listar')
def listar():

    # Comando em SQl para selecionar
    # os passageiros
    comando = "select * from passageiros"

    # Executar o comando em SQL
    cursor.execute(comando)

    # Variável que irá receber
    # o resultado do comando
    passageiros = cursor.fetchall() # acessar todos
    
    # res.render('listar', passageiros: results)
    
    # retornar o resultado
    # carregando em outra página
    return render_template('listar.html', passageiros=passageiros)

    # OBS: a primeira variável 'passageiros' será usada como
    # recebimento do resultado do script em SQL. A segunda
    # vairável 'passageiros' será usada no arquivo listar.html
    # para a leitura dos dados selecionados na página


# 5) Rota para selecionar somente um passageiro
@app.route('/editar/<int:id>', methods=['GET'])

# OBS: como o id será usado como atributo identificador
# para a seleção do passageiro, esse será parâmetro
# da função que ira executar o script em SQL
def selecionar_passageiro(id):

     # Protegendo a rota
    # se o usuário não estiver logado
    if 'id_usuario' not in session:
        return redirect('/')

    
    # Comando SQL para selecionar
    # somente um passageiro pelo id
    comando = "select * from passageiros where id = %s"

    # Variável que irá receber 
    # o valor do id do passageiro
    valor = (id,)

    # Executar o comando em SQL
    cursor.execute(comando, valor)

    # Atribuir um variável para o
    # receber o resultado da
    # execução do comando em SQL
    passageiro = cursor.fetchone() # acessar um
    
    # Retornar o resultado
    # carregando em outra página
    return render_template('editar.html', passageiro=passageiro)

    # OBS: a primeira variável 'passageiro' será usada como
    # recebimento do resultado do script em SQL. A segunda
    # vairável 'passageiro' será usada no arquivo listar.html
    # para a leitura dos dados selecionados na página

# 6) Rota para editar um passageiro
@app.route('/editar-passageiro/<int:id>', methods=['POST'])
def editar(id):

     # Protegendo a rota
    # se o usuário não estiver logado
    if 'id_usuario' not in session:
        return redirect('/')
    
    nome = request.form['nome']
    data_nascimento = request.form['dataNascimento']
    endereco = request.form['endereco']
    telefone = request.form['telefone']
    cpf = request.form['cpf']
    
    # Comando para editar os
    # dados do passageiro
    comando = "update passageiros set nome = %s, dataNascimento = %s, endereco = %s, telefone = %s, cpf = %s where id = %s"

    # Variável que irá receber todos
    # os valores das variáveis anteriores

    # OBS: a ordem dos valores é o mesmo usado para
    # editar os dados do passageiros no script SQL
    valores = (nome, data_nascimento, endereco, telefone, cpf, id)

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
    
    # Retorno alternativo
    # return redirect('/listar')


# 7) Rota para excluir um passageiro
@app.route('/excluir/<int:id>')
def excluir(id):

    # Comando em SQL para excluir
    # um passageiro
    comando = 'delete from passageiros where id = %s'
    
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
    return redirect('/listar')




# 8 Rota de login do usuário

@app.route('/login', methods = ['GET', 'POST'])
def login():
        
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        # Criar o comando para selecionar
        # o usuário pelo e-mail e senha
        # OBS: modelar a tabela chamada
        # 'usuario' com as colunas:
        #  - id
        #  - nome
        #  - email
        #  - senha
        comando = 'select id. e-mail,senha from usuario where email = %s and senha = %s '
        valores = (email, senha)
        cursor.execute(comando, valores)
        usuario = cursor.fetchone()
        
        # Verificando se o usuário
        # existe na tabela 'usuario'
        if usuario:
            # Criando a sessão do usuário
            # atribuindo um apelido
            # chamado 'id_usuario' no
            # primeiro colchete
            session['id_usuario'] = usuario['id']
            
            # Acessando o e-mail do usuário
            # atribuindo um apelido
            # chamado 'email_usuario' no
            # primeiro colchete
            session['email_usuario'] = usuario['email']
            
            # Acessando o nome do usuário
            session[nome_usuaria] = [nome] usuario
            
            
            # Redirecionar para a página
            # de início do usuário
            return redirect('/inicio')
        
        # Mas se ele não existir ou
        # se o e-mail e/ou a senha
        # estiverem incorretos
        else:
            # Variável que irá exibir
            # a mensagem de erro
            mensagem = "login falhou"          
            
            return render_template('login.html', mensagem=mensagem)

    return render_template('login.html')

# 10) Rota de sair do sistema
# e destruindo a sessão
@app.route('/sair')
def sair():



     # Protegendo a rota
    # se o usuário não estiver logado
    if 'id_usuario' not in session:
        return redirect('/')
    
    
    # Destruindo a sessão
    session.clear()
    
    # Retornando para a página
    # de login
    # return redirect(url_for('index'))

    # Retorno alternativo
    return redirect('/')


# Execução do servidor
# Nesse modo, o servidor irá
# reiniciar automaticamente após
# mudanças na aplicação principal
if __name__ == '__main__':
    app.run(debug=True)