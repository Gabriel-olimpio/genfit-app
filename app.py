from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import requests, markdown

OLLAMA_API_URL = 'http://localhost:11434/api/generate'

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


@app.route('/generate', methods=['POST'])
def generate():
    objetivo = request.form['objetivo']
    dias = request.form['dias']
    peso = request.form['peso']
    altura = request.form['altura']
    tempo = request.form['duracao']


    prompt = f"""
    Crie uma rotina de exercícios para uma pessoa com as seguintes características:
    - Peso: {peso} kg
    - Altura: {altura} cm
    - Objetivo: {objetivo}
    - Tempo de treino: {tempo} minutos por dia
    - Dias de treino por semana: {dias}

    A rotina deve ser detalhada e incluir aquecimento, exercícios principais e alongamento. Gere o texto em markdown, mas não liste os exercícios por numeração.
    """
    data = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_API_URL, json=data)

    if response.status_code == 200:
        result = response.json()
        generated_text = result.get('response', '')

        # Formata o texto de markdown para HTML
        formated_text = markdown.markdown(generated_text)

        # Salvar plano gerado no banco de dados
        new_plan = WorkoutPlan(plan_data=generated_text, user_id=current_user.id) # Armazena o plano em MARKDOWN 
        db.session.add(new_plan)
        db.session.commit()

        return render_template('result.html', routine=formated_text)
    else:
        return render_template('result.html', error='Erro ao gerar rotina de exercícios.')

# Rota de quando o plano é gerado
@app.route('/result')
@login_required
def result():
    return render_template('result.html')

# Rota do plano gerado com base no usuário
@app.route('/plan')
@login_required
def plan():
    latest_plan = WorkoutPlan.query.filter_by(user_id=current_user.id).order_by(WorkoutPlan.created_at.desc()).first()

    # Checa se há um plano
    if latest_plan:
        formated_text = markdown.markdown(latest_plan.plan_data)
        return render_template('result.html', routine=formated_text)
    else:
        return render_template('result.html', error='Nenhum plano de treino encontrado.')


# Classe do Usuario
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    

class WorkoutPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plan_data = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    user = db.relationship('Usuario', backref=db.backref('plans', lazy=True))


# Rotas da Aplicação Web

@app.route('/')
def home():
    return render_template('index.html')

@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html')




@app.route('/form', methods=['GET', 'POST'])
@login_required
def form():
    return render_template('form.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.senha == senha:
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

        if Usuario.query.filter_by(email=email).first():
            flash('Email já registrado', 'danger')
            return redirect(url_for('register'))

        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
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


