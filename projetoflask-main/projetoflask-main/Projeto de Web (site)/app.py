from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('bdLivros.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS conta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Livroscurtidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            livro TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS autorescurtidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            autor TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comentarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            mensagem TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()





@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        nome = request.form.get("nome")
        mensagem = request.form.get("mensagem")

        if not nome or not mensagem:
            return "Erro: Todos os campos são obrigatórios."
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO comentarios (nome, mensagem) 
                VALUES (?, ?)
            ''', (nome, mensagem))
            conn.commit()
        except sqlite3.Error as e:
            return f"Erro no banco de dados: {str(e)}"
        finally:
            conn.close()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT nome, mensagem FROM comentarios')
        comentarios = cursor.fetchall()
    except sqlite3.Error as e:
        return f"Erro no banco de dados: {str(e)}"
    finally:
        conn.close()

    return render_template("index.html", comentarios=comentarios)



@app.route('/comentarios')
def mostrar_comentarios():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT nome, mensagem FROM comentarios')
        comentarios = cursor.fetchall()
    except sqlite3.Error as e:
        return f"Erro no banco de dados: {str(e)}"
    finally:
        conn.close()
    return render_template('comentarios.html', comentarios=comentarios)




@app.route('/amendoas')
def amendoas():
    return render_template("amendoas.html")





@app.route('/amor-a-primeira-vista')
def amor():
    return render_template("amor.html")





@app.route('/deixa-nevar')
def deixa():
    return render_template("deixa nevar.html")





@app.route('/o-horizonte-mora-em-um-dia-cinza')
def horizonte():
    return render_template("horizonte.html")





@app.route('/livraria-hyunam-dong')
def livraria():
    return render_template("livraria Hyunam-dong.html")





@app.route('/minha-vida-com-boris')
def boris():
    return render_template("boris.html")





@app.route('/no-final-daquele-dia')
def final():
    return render_template("no final dql dia.html")





@app.route('/paralela')
def paralela():
    return render_template("paralela.html")





@app.route('/vantagens-de-ser-incrivel')
def vantagens():
    return render_template("vantagens.html")




@app.route('/a-saga-wingfeather')
def wingfeather():
    return render_template("wingfeather.html")



@app.route('/livros')
def livros():
    return render_template("livros.html")




@app.route('/autores')
def autores():
    return render_template("autores.html")



@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        if not nome or not  email or not senha:
            return "Erro: Todos os campos são obrigatórios."

        print(f"Dados recebidos: {nome}, {email}, {senha}")

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO conta (nome, email, senha) 
                VALUES (?, ?, ?)''', (nome, email, senha))
            conn.commit()
            return redirect("/")
        except sqlite3.IntegrityError:
            return "Erro: Este usuário ou email já está cadastrado."
        finally:
            conn.close()
    return render_template('cadastrar.html')

@app.route('/alterar', methods=['GET', 'POST'])
def alterar():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        novo_nome = request.form['novo_nome']
        nova_senha = request.form['nova_senha']

        if not email or not senha:
            return "Erro: Email e senha são obrigatórios."

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''SELECT * FROM conta WHERE email = ? AND senha = ?''', (email, senha))
            usuario = cursor.fetchone()

            if usuario:
                cursor.execute('''
                    UPDATE conta 
                    SET nome = ?, senha = ?
                    WHERE email = ? AND senha = ?
                ''', (novo_nome, nova_senha, email, senha))
                conn.commit()
                return redirect("/")
            else:
                return "Erro: Usuário ou senha inválidos."
        except sqlite3.Error as e:
            return f"Erro no banco de dados: {str(e)}"
        finally:
            conn.close()

    return render_template("alterar.html")


@app.route('/deletar', methods=['GET', 'POST'])
def deletar():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
    
        if not email or not senha:
            return "Erro: Todos os campos são obrigatórios."
        
        print(f"Dados recebidos: {email}, {senha}")

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT * FROM conta WHERE email = ? AND senha = ?
            ''', (email, senha))
            usuario = cursor.fetchone()
            
            if usuario:
                cursor.execute('''
                    DELETE FROM conta WHERE email = ? AND senha = ?
                ''', (email, senha))
                conn.commit()
                return redirect("/")
            else:
                return "Erro: Usuário ou senha inválidos."
        except sqlite3.Error as e:
            return f"Erro no banco de dados: {str(e)}"
        finally:
            conn.close()
    return render_template("deletar.html")




@app.route('/Livrocurtir', methods=['POST'])
def curtir_livro():
    livro = request.json.get('livro')
    if not livro:
        return {"status": "error", "message": "Nenhum livro especificado"}, 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT id FROM Livroscurtidas WHERE livro = ?', (livro,))
        registro = cursor.fetchone()

        if registro:
            cursor.execute('DELETE FROM Livroscurtidas WHERE livro = ?', (livro,))
            conn.commit()
            return {"status": "success", "message": "Livro removido dos curtidos", "curtido": False}
        else:
            cursor.execute('INSERT INTO Livroscurtidas (livro) VALUES (?)', (livro,))
            conn.commit()
            return {"status": "success", "message": "Livro adicionado aos curtidos", "curtido": True}
    except sqlite3.Error as e:
        return {"status": "error", "message": f"Erro no banco de dados: {str(e)}"}, 500
    finally:
        conn.close()


@app.route('/livros-curtidos')
def mostrar_Lcurtidos():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT livro FROM Livroscurtidas')
        livros_curtidos = [row['livro'] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        return f"Erro no banco de dados: {str(e)}"
    finally:
        conn.close()

    return render_template('Livroscurtidos.html', livros=livros_curtidos)





@app.route('/Autorcurtir', methods=['POST'])
def curtir_autor():
    autor = request.json.get('autor')
    if not autor:
        return {"status": "error", "message": "Nenhum autor especificado"}, 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT id FROM autorescurtidas WHERE autor = ?', (autor,))
        registro = cursor.fetchone()

        if registro:
            cursor.execute('DELETE FROM autorescurtidas WHERE autor = ?', (autor,))
            conn.commit()
            return {"status": "success", "message": "Autor removido dos curtidos", "curtido": False}
        else:
            cursor.execute('INSERT INTO autorescurtidas (autor) VALUES (?)', (autor,))
            conn.commit()
            return {"status": "success", "message": "Autor adicionado aos curtidos", "curtido": True}
    except sqlite3.Error as e:
        return {"status": "error", "message": f"Erro no banco de dados: {str(e)}"}, 500
    finally:
        conn.close()

@app.route('/autores-curtidos')
def mostrar_Acurtidos():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT autor FROM autorescurtidas')
        autores_curtidos = [row['autor'] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        return f"Erro no banco de dados: {str(e)}"
    finally:
        conn.close()

    return render_template('Autorescurtidos.html', autores=autores_curtidos)



if __name__ == "__main__":
    create_table()
    app.run(debug=True)
