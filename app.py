# Importações necessárias para o Flask (framework web) e MySQL (banco de dados)
from flask import Flask, render_template, request, session, flash, redirect, url_for, jsonify
import mysql.connector as mc

# Cria uma instância do Flask (aplicação web) e define uma chave secreta para sessões
app = Flask(__name__)
app.secret_key = "my_secret_key"

# Função para conectar ao banco de dados MySQL
def connect_database():
    return mc.connect(
        user='root',       # Usuário do banco de dados
        password='',       # Senha do banco de dados (vazia no exemplo)
        host='127.0.0.1',  # Host do banco (localhost)
        database='school'  # Nome do banco de dados
    )

# Função para verificar se senha e confirmação de senha são iguais
def validConfirmPassword(password, confirmPassword):
    return password == confirmPassword

# Função para criar um novo usuário no banco de dados
def createUser(user, password):
    conn = connect_database()  # Conecta ao banco
    cursor = conn.cursor()     # Cria um cursor para executar comandos SQL
    try:
        # Insere um novo usuário na tabela 'user'
        cursor.execute("INSERT INTO user(email, senha) VALUES (%s, %s)", (user, password))
        conn.commit()  # Confirma a transação
        return True    # Retorna True se inserção for bem-sucedida
    except mc.IntegrityError:  # Se e-mail já existir (violação de integridade)
        return False
    finally:
        conn.close()  # Fecha a conexão com o banco

# Função para cadastrar um novo aluno no banco de dados
def create_aluno(nome, senha, dataNascimento, whatsapp):
    conn = connect_database()
    cursor = conn.cursor()
    try:
        # Insere um novo aluno na tabela 'student'
        cursor.execute("INSERT INTO student VALUES(null, %s, %s, %s, %s)", (nome, senha, dataNascimento, whatsapp))
        conn.commit()
        return True
    except:
        flash("Erro ao cadastrar aluno", "danger")  # Mensagem de erro (usando Flask flash)
        return False
    finally:
        conn.close()

# Função para cadastrar um novo curso no banco de dados
def create_curso(sigla, nome, cargaHoraria):
    conn = connect_database()
    cursor = conn.cursor()
    try:
        # Insere um novo curso na tabela 'course'
        cursor.execute("INSERT INTO course VALUES(null, %s, %s, %s)", (sigla, nome, cargaHoraria))
        conn.commit()
        return True
    except:
        flash("Erro ao cadastrar curso", "danger")
        return False
    finally:
        conn.close()

# Função para buscar todos os alunos cadastrados
def findAllAlunos():
    conn = connect_database()
    cursor = conn.cursor()
    try:
        # Seleciona ID e nome de todos os alunos
        cursor.execute("SELECT id, nome FROM student")
        return cursor.fetchall()  # Retorna uma lista de tuplas (id, nome)
    except:
        flash("Erro ao listar alunos", "danger")
        return []
    finally:
        conn.close()

# Função para buscar todos os cursos cadastrados
def findAllCursos():
    conn = connect_database()
    cursor = conn.cursor()
    try:
        # Seleciona ID e nome de todos os cursos
        cursor.execute("SELECT id, nome FROM course")
        return cursor.fetchall()
    except:
        flash("Erro ao listar cursos", "danger")
        return []
    finally:
        conn.close()

# Função para matricular um aluno em um curso
def registration(fk_aluno, fk_curso):
    conn = connect_database()
    cursor = conn.cursor()
    try:
        # Insere uma matrícula na tabela 'registration'
        cursor.execute("INSERT INTO registration VALUES (null, %s, %s)", (fk_aluno, fk_curso))
        conn.commit()
        flash('Matrícula realizada com sucesso', 'success')
        return True
    except:
        flash('Erro ao matricular o aluno', 'danger')
        return False
    finally:
        conn.close()

# Função para buscar todas as matrículas (com JOIN entre tabelas)
def findAllMatriculas():
    conn = connect_database()
    cursor = conn.cursor(dictionary=True)  # Retorna resultados como dicionários (melhor legibilidade)
    try:
        # Consulta SQL com JOIN para obter aluno, curso e WhatsApp
        cursor.execute("""
            SELECT s.nome as aluno, 
                   c.nome as curso, 
                   s.whatsapp
            FROM registration r
            JOIN student s ON r.fk_student = s.id
            JOIN course c ON r.fk_course = c.id
            ORDER BY s.nome
        """)
        return cursor.fetchall()  # Retorna lista de dicionários
    except Exception as e:
        print(f"ERRO NO SQL: {str(e)}")  # Log de erro no console
        return []
    finally:
        conn.close()

# Rota para login (GET: exibe formulário; POST: processa dados)
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")    
        
        conn = connect_database()
        cursor = conn.cursor()
        # Verifica se usuário e senha existem no banco
        cursor.execute("SELECT * FROM user WHERE email = %s AND senha = %s", (username, password))
        valid = cursor.fetchall()        
        
        if valid:
            session['admin'] = username  # Armazena usuário na sessão
            flash('Login efetuado com sucesso', "success")
            return redirect(url_for('createAluno'))  # Redireciona para página de alunos
        else:
            flash('Usuário ou senha incorretos', "danger")
        conn.close()
            
    return render_template('index.html')  # Renderiza template de login

# Rota para página de cadastro de aluno (requer autenticação)
@app.route("/createAluno")
def createAluno():
    if 'admin' not in session:  # Verifica se usuário está logado
        return redirect(url_for('login'))
    return render_template('createAluno.html')

# Rota para página de cadastro de curso (requer autenticação)
@app.route("/createCurso")
def createCurso():
    if 'admin' not in session:
        return redirect(url_for('login'))
    return render_template('createCurso.html')

# Rota para logout (remove usuário da sessão)
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('admin', None)  # Remove 'admin' da sessão
    flash("Logout efetuado com sucesso", "success")
    return redirect(url_for('login'))

# Rota para redirecionar para página de registro de usuário
@app.route('/moveRegister', methods=['GET'])
def moveRegister():
    return render_template('registerUser.html')

# Rota para registrar novo usuário (valida senhas e insere no banco)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')
        
        if not validConfirmPassword(password, confirmPassword):
            flash("As senhas devem ser iguais", "warning")
            return redirect(url_for('moveRegister'))

        if createUser(username, password):
            flash("Usuário cadastrado com sucesso", "success")
            return redirect(url_for('login'))
        else:
            flash("Este e-mail já está cadastrado", "danger")
            return redirect(url_for('moveRegister'))

    return render_template('registerUser.html')

# Rota inicial (redireciona para login ou página de alunos)
@app.route('/')
def home():
    if 'admin' in session:  # Se logado, vai para alunos
        return redirect(url_for('createAluno'))
    return redirect(url_for('login'))  # Senão, vai para login

# Rota para inserir aluno via formulário POST
@app.route('/insertAluno', methods=['GET', 'POST'])
def insertAluno():
    if request.method == 'POST':
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        dataNascimento = request.form.get('dataNascimento')
        whatsapp = request.form.get('whatsapp')
         
        if create_aluno(nome, senha, dataNascimento, whatsapp):
            flash('Aluno cadastrado com sucesso', 'success')
        return redirect(url_for('createAluno'))
    return redirect(url_for('createAluno'))

# Rota para inserir curso via formulário POST
@app.route('/insertCurso', methods=['GET', 'POST'])
def insertCurso():
    if request.method == 'POST':
        sigla = request.form.get('sigla')
        nome = request.form.get('nome')
        cargaHoraria = request.form.get('cargaHoraria')
        
        if create_curso(sigla, nome, cargaHoraria):
            flash('Curso cadastrado com sucesso', 'success')
        return redirect(url_for('createCurso'))
    return redirect(url_for('createCurso'))

# Rota para listar alunos em formato JSON (usada possivelmente por AJAX)
@app.route('/alunos', methods=['GET'])
def aluno():
    alunos = findAllAlunos()
    list_alunos = [{'id': a[0], 'nome': a[1]} for a in alunos]  # Converte para lista de dicionários
    return jsonify(list_alunos)  # Retorna JSON

# Rota para listar cursos em formato JSON
@app.route('/cursos', methods=['GET'])
def curso():
    cursos = findAllCursos()
    list_cursos = [{'id': c[0], 'nome': c[1]} for c in cursos]
    return jsonify(list_cursos)

# Rota para matrículas (exibe lista e processa novas matrículas)
@app.route('/matriculas', methods=['GET', 'POST'])
def matriculas():
    if 'admin' not in session:
        return redirect(url_for('login'))
    
    matriculas_data = findAllMatriculas()
    print("DADOS QUE SERÃO ENVIADOS PARA O HTML:", matriculas_data)  # Debug
    
    if request.method == 'POST':
        aluno_id = request.form.get('aluno')
        curso_id = request.form.get('curso')
        if aluno_id and curso_id:
            registration(aluno_id, curso_id)
            matriculas_data = findAllMatriculas()  # Atualiza dados após cadastro
    
    return render_template('matriculas.html', 
                         alunos=matriculas_data,
                         options_alunos=findAllAlunos(),
                         options_cursos=findAllCursos())

# Rota para listar matrículas em JSON
@app.route('/listaMatriculas', methods=['GET'])
def listaMatriculas():
    dados = findAllMatriculas()
    list_matriculas = [{
        "aluno": m[0],
        "curso": m[1],
        "whatsapp": m[2]
    } for m in dados]
    return jsonify(list_matriculas)

# Inicia o servidor Flask em modo debug (se executado diretamente)
if __name__ == "__main__":    
    app.run(debug=True)