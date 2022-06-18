from flask import Flask, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projeto2.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'teste$%#'

db = SQLAlchemy(app)
login_manager = LoginManager(app)


class usuarios(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(50))
    tipo_usuario = db.Column(db.String(20))

    def __repr__(self):
        return '<Adm %r>'%self.nome

class projetos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    
    def __repr__(self):
        return '<Projeto %r>'%self.nome
    
class coordenadores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(50))
    tipo_usuario = db.Column(db.String(20))

    grupos = db.relationship('grupos', backref='coordenadores', lazy=True)

    def __repr__(self):
        return '<Coordenador %r>'%self.nome

class grupos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dia = db.Column(db.String(10))
    hora = db.Column(db.String(10))

    projeto_id = db.Column(db.Integer, ForeignKey('projetos.id'))
    coordenador = db.Column(db.Integer, ForeignKey('coordenadores.id'))
    alunos = db.relationship('alunos', backref='grupos', lazy=True)

    def __repr__(self):
        return '<Grupo %r>'%self.id

class alunos(db.Model):
    ra = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(50))
    curso = db.Column(db.String(50))
    polo = db.Column(db.String(50))
    interesse = db.Column(db.String(50))
    hobby = db.Column(db.String(50))
    telefone = db.Column(db.String(15))
    tipo_usuario = db.Column(db.String(20))

    projeto_id = db.Column(db.Integer, ForeignKey('projetos.id'))
    grupo_id = db.Column(db.Integer, ForeignKey('grupos.id'))

    def __repr__(self):
        return '<Aluno: %r>'%self.nome


@app.route('/')
@app.route('/index')
#@login_required
def index():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# CADASTRAR ALUNOS
@app.route('/cadastrar_aluno', methods=['GET','POST'])
@login_required

def cadastrar_aluno():    
    aluno = alunos()
    if request.method == 'POST':
        aluno.nome = request.form.get('nome')
        aluno.senha = request.form.get('senha')
        aluno.curso = request.form.get('curso')
        aluno.polo = request.form.get('polo')
        aluno.projeto_id = request.form.get('projeto')
        aluno.grupo_id = request.form.get('grupo')
        aluno.interesse = request.form.get('interesse')
        aluno.hobby = request.form.get('hobby')
        aluno.telefone = request.form.get('telefone')
        aluno.email = request.form.get('email')

        db.session.add(aluno)
        db.session.commit()

        return redirect(url_for('lista_alunos'))

    return render_template('cadastrar_aluno.html')

# ATUALIZAR ALUNOS
@app.route('/<int:ra>/atualiza_aluno', methods=['GET','POST'])
@login_required

def atualiza_aluno(ra):
    aluno = alunos.query.filter_by(ra=ra).first()
    if request.method == 'POST':
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        curso = request.form.get('curso')
        polo = request.form.get('polo')
        projeto_id = request.form.get('projeto')
        grupo_id = request.form.get('grupo')
        interesse = request.form.get('interesse')
        hobby = request.form.get('hobby')
        telefone = request.form.get('telefone')
        email = request.form.get('email')

        aluno = alunos.query.filter_by(ra=ra).update({
            'nome':nome, 'senha':senha, 'curso':curso,
            'polo':polo, 'projeto_id':projeto_id, 
            'grupo_id':grupo_id, 'interesse':interesse,
            'hobby':hobby, 'telefone':telefone, 'email':email
        })
        db.session.commit()
        return redirect(url_for('lista_alunos'))

    return render_template('atualiza_aluno.html', aluno=aluno)

#EXCLUIR ALUNO
@app.route('/<int:ra>/excluir_aluno')
@login_required

def excluir_aluno(ra):
    aluno = alunos.query.filter_by(ra=ra).first()
    db.session.delete(aluno)
    db.session.commit()

    return redirect(url_for('lista_alunos'))

#LISTAR ALUNOS
@app.route('/lista_alunos')
@login_required

def lista_alunos():
    return render_template('lista_alunos.html', alunos=alunos.query.all())


#GRUPOS
@app.route('/cadastrar_grupo', methods=['GET','POST'])
@login_required

def cadastrar_grupo():
    grupo = grupos()
    if request.method == 'POST':
        grupo.dia = request.form.get('dia')
        grupo.hora = request.form.get('hora')
        grupo.projeto_id = request.form.get('projeto')
        grupo.coordenador = request.form.get('coordenador')

        db.session.add(grupo)
        db.session.commit()

        return redirect(url_for('lista_grupos'))

    return render_template('cadastrar_grupo.html')

@app.route('/<int:id>/atualiza_grupo', methods=['GET','POST'])
@login_required

def atualiza_grupo(id):
    grupo = grupos.query.filter_by(id=id).first()

    if request.method == 'POST':
        dia = request.form.get('dia')
        hora = request.form.get('hora')
        projeto_id = request.form.get('projeto')
        coordenador = request.form.get('coordenador')

        grupo = grupos.query.filter_by(id=id).update({'dia':dia,'hora':hora,
            'projeto_id':projeto_id, 'coordenador':coordenador})
        db.session.commit()

        return redirect(url_for('lista_grupos'))

    return render_template('atualiza_grupo.html', grupo=grupo)

@app.route('/<int:id>/excluir_grupo')
@login_required

def excluir_grupo(id):
    grupo = grupos.query.filter_by(id=id).first()
    db.session.delete(grupo)
    db.session.commit()
    return redirect(url_for('lista_grupos'))


#LISTAR GRUPOS
@app.route('/lista_grupos')
@login_required

def lista_grupos():
    lista_grupos = grupos.query.all()
    return render_template('lista_grupos.html', grupos=lista_grupos)

#COORDENADORES
@app.route('/cadastrar_coordenador', methods=['GET','POST'])
@login_required

def cadastrar_coordenador():
    coordenador = coordenadores()
    if request.method == 'POST':
        coordenador.nome = request.form.get('nome')
        coordenador.email = request.form.get('email')
        coordenador.senha = request.form.get('senha')
        coordenador.tipo_usuario = 'coordenador'

        db.session.add(coordenador)
        db.session.commit()

        return redirect(url_for('lista_coordenadores'))

    return render_template('cadastrar_coordenador.html')

@app.route('/<int:id>/atualiza_coordenador', methods=['GET', 'POST'])
@login_required

def atualiza_coordenador(id):
    coordenador = coordenadores.query.filter_by(id=id).first()

    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        email = request.form['email']

        coordenador = coordenadores.query.filter_by(id=id).update({'nome':nome, 'senha':senha, 'email':email})
        db.session.commit()

        return redirect(url_for('lista_coordenadores'))

    return render_template('atualiza_coordenador.html', coordenador=coordenador)

#EXCLUIR COORDENADOR
@app.route('/<int:id>/excluir_coordenador')
@login_required

def excluir_coordenador(id):
    coordenador = coordenadores.query.filter_by(id=id).first()
    db.session.delete(coordenador)
    db.session.commit()
    
    return redirect(url_for('lista_coordenadores'))

@app.route('/lista_coordenadores')
@login_required

def lista_coordenadores():
    lista_coordenadores = coordenadores.query.all()
    return render_template('lista_coordenadores.html', coordenadores=lista_coordenadores)

#USUÁRIOS
@app.route('/cadastrar_usuario', methods=['GET','POST'])
@login_required

def cadastrar_usuario():
    user = usuarios()
    if request.method == 'POST':
        user.nome = request.form.get('nome')
        user.email = request.form.get('email')
        user.senha = request.form.get('senha')
        user.tipo_usuario = 'administrador'

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('lista_usuarios'))

    return render_template('cadastrar_usuario.html')

@app.route('/<int:id>/atualiza_usuario', methods=['GET','POST'])
@login_required

def atualiza_usuario(id):
    usuario = usuarios.query.filter_by(id=id).first()

    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        email = request.form['email']

        usuario = usuarios.query.filter_by(id=id).update({'nome':nome, 'senha':senha, 'email':email})
        db.session.commit()

        return redirect(url_for('lista_usuarios'))
    return render_template('atualiza_usuario.html', usuario=usuario)

@app.route('/<int:id>/excluir_usuario')
@login_required

def excluir_usuario(id):
    usuario = usuarios.query.filter_by(id=id).first()
    db.session.delete(usuario)
    db.session.commit()
    
    return redirect(url_for('lista_usuarios')) 

@app.route('/lista_usuarios')
@login_required

def lista_usuarios():
    return render_template('lista_usuarios.html', usuarios=usuarios.query.all())

# PROJETOS CRUD
@app.route('/cadastrar_projeto', methods=['GET','POST'])
@login_required

def cadastrar_projeto():
    projeto = projetos()
    if request.method == 'POST':
        projeto.nome = request.form.get('nome')

        db.session.add(projeto)
        db.session.commit()

        return redirect(url_for('lista_projetos'))

    return render_template('cadastrar_projeto.html')

@app.route('/<int:id>/atualiza_projeto', methods=['GET','POST'])
@login_required

def atualiza_projeto(id):
    projeto = projetos.query.filter_by(id=id).first()

    if request.method == 'POST':
        nome = request.form['nome']
        projeto = projetos.query.filter_by(id=id).update({'nome':nome})
        db.session.commit()
        
        return redirect(url_for('lista_projetos'))

    return render_template('atualiza_projeto.html', projeto=projeto)

@app.route('/<int:id>/excluir_projeto')
@login_required

def excluir_projeto(id):
    projeto = projetos.query.filter_by(id=id).first()
    db.session.delete(projeto)
    db.session.commit()
    
    return redirect(url_for('lista_projetos')) 

@app.route('/lista_projetos')
@login_required

def lista_projetos():
    return render_template('lista_projetos.html', projetos=projetos.query.all())

# LOGIN E LOGOUT
@login_manager.user_loader
def load_user(user_id):
    return usuarios.query.get(user_id)

@app.route('/login', methods=['GET','POST'])
def login():
    user = usuarios.query.filter_by(email=request.form.get('email')).first()
    if user and user.senha == request.form.get('senha'):        
        login_user(user)
        flash('Usuário conectado com sucesso!')
        return redirect(url_for('index')) 
    # else:
    #     flash('Usuário ou senha errados!')

    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    flash('Usuário desconectado com sucesso!')
    return redirect(url_for('login'))

#BUSCAR ALUNOS FUNÇÃO PRINCIPAL
@app.route('/buscar_alunos')
def buscar_alunos():
    aluno_teste = {
        "nome":"Aluno Teste",
        "curso":"Engenharia da Computação",
        "polo":"Santa Isabel",
        "interesse":"Banco de Dados",
        "hobby":"Futebol"
    }
    integrantes = alunos.query.all()
    return render_template('buscar_alunos.html', integrantes=integrantes, aluno_teste=aluno_teste)

@app.route('/busca_por_curso', methods=['GET','POST'])
def busca_por_curso():
    aluno_teste = {
        "nome":"Aluno Teste",
        "curso":"Engenharia da Computação",
        "polo":"Santa Isabel",
        "interesse":"Banco de Dados",
        "hobby":"Futebol"
    }
    integrantes = alunos.query.filter_by(curso=aluno_teste['curso'])
    return render_template('busca_por_curso.html', integrantes=integrantes)

@app.route('/busca_por_polo', methods=['GET','POST'])
def busca_por_polo():
    aluno_teste = {
        "nome":"Aluno Teste",
        "curso":"Engenharia da Computação",
        "polo":"Santa Isabel",
        "interesse":"Banco de Dados",
        "hobby":"Futebol"
    }
    integrantes = alunos.query.filter_by(polo=aluno_teste['polo'])
    return render_template('busca_por_polo.html', integrantes=integrantes)

@app.route('/busca_por_interesse', methods=['GET','POST'])
def busca_por_interesse():
    aluno_teste = {
        "nome":"Aluno Teste",
        "curso":"Engenharia da Computação",
        "polo":"Santa Isabel",
        "interesse":"Banco de Dados",
        "hobby":"Futebol"
    }
    integrantes = alunos.query.filter_by(interesse=aluno_teste['interesse'])
    return render_template('busca_por_interesse.html', integrantes=integrantes)

@app.route('/busca_por_hobby', methods=['GET','POST'])
def busca_por_hobby():
    aluno_teste = {
        "nome":"Aluno Teste",
        "curso":"Engenharia da Computação",
        "polo":"Santa Isabel",
        "interesse":"Banco de Dados",
        "hobby":"Futebol"
    }
    integrantes = alunos.query.filter_by(hobby=aluno_teste['hobby'])
    return render_template('busca_por_hobby.html', integrantes=integrantes)

if __name__=='__main__':
    db.create_all()
    app.run(debug=False)


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projeto2.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'teste$%#'

    db = SQLAlchemy(app)
    login_manager = LoginManager(app)