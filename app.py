from functools import wraps
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import bcrypt
from werkzeug.security import generate_password_hash


# Config do flask e banco de dados
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'chave_secreta'

db = SQLAlchemy(app)

# Log in manager
login_manager = LoginManager(app)

# Redireciona p/ login caso nao registrado
login_manager.login_view = 'login'
login_manager.login_message = 'Você precisa estar logado para acessar esta página'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


@app.route('/result')
def result():
    return render_template('result.html')

# Verificação de papel (adm, user)
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.papel != 'admin':
            abort(403)
        return func(*args, **kwargs)
    return wrapper


# Classe do Usuario
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    papel = db.Column(db.String(20), nullable=False, default='usuario')
    
    def set_senha(self, senha):
        self.senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verificar_senha(self, senha):
        return bcrypt.checkpw(senha.encode('utf-8'), self.senha.encode('utf-8'))


# Rotas da Aplicação Web

@app.route('/')
def home():
    return render_template('index.html')

@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html')

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    usuarios = Usuario.query.all()
    return render_template('admin_dashboard.html', usuarios=usuarios)

@app.route('/usuario')
@login_required
def usuario_dashboard():
    return render_template('usuario_dashboard.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']

        return f"Olá, {name.capitalize()}!"
    return render_template('form.html')

# @app.route('/usuarios')
# @login_required
# @admin_required
# def listar_usuarios():
#     usuarios = Usuario.query.all()
#     return render_template('usuarios.html', usuarios=usuarios) 

@app.route('/atualizar/<int:id>')
def atualizar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    usuario.nome = 'Nome Atualizado'
    db.session.commit()
    return f'Usuário {id} atualizado!'

@app.route('/deletar/<int:id>')
def deletar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return f'Usuário {id} deletado!'



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.verificar_senha(senha):
            login_user(usuario)
            flash('Login feito com sucesso!', 'success')
            return redirect(url_for('form'))
        else:
            flash('Email ou senha incorretos.', 'danger')
        
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    flash('Você saiu!', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('usuario_dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        papel = request.form.get('papel', 'usuario')

        if Usuario.query.filter_by(email=email).first():
            flash('Email já registrado', 'danger')
            return redirect(url_for('register'))

        hashed_senha = generate_password_hash(senha, method='pbkdf2:sha256')
        novo_usuario = Usuario(nome=nome, email=email, senha=hashed_senha, papel=papel)
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Conta criada com sucesso! Faça o login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')



# Criando tabelas no banco de dados
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)


