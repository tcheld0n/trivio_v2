from app import app
from flask import render_template, request, redirect, url_for, session, g, flash
from urllib.parse import urlparse
from app.forms import LoginForm, RegistrationForm, QuestionForm
from app.models import User, Questions
from app import db
import requests
import random

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        g.user = user

@app.route('/')
def home():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        session['user_id'] = user.id
        session['marks'] = 0
        from urllib.parse import urlparse
        next_page = request.args.get('next')
        if next_page and urlparse(next_page).netloc == '':
            next_page = url_for('home')
        return redirect(next_page)
        return redirect(url_for('home'))
    if g.user:
        return redirect(url_for('home'))
    return render_template('login.html', form=form, title='Login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.password.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        session['marks'] = 0
        return redirect(url_for('home'))
    if g.user:
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/question/<int:id>', methods=['GET', 'POST'])
def question(id):
    form = QuestionForm()

    # Inicializa perguntas e pontuação na sessão
    if 'questions' not in session:
        # Chamada à Open Trivia DB para obter 10 perguntas
        response = requests.get('https://opentdb.com/api.php?amount=10', verify=False)
        if response.status_code == 200:
            data = response.json()
            if data['response_code'] == 0:
                session['questions'] = data['results']  # Armazena as perguntas na sessão
                session['marks'] = 0  # Inicializa a pontuação
                session['current_question'] = 0  # Índice da pergunta atual
            else:
                return redirect(url_for('score'))
        else:
            return redirect(url_for('score'))

    # Verifica se todas as perguntas foram respondidas
    if session['current_question'] >= len(session['questions']):
        return redirect(url_for('score'))

    # Obtém a pergunta atual da sessão
    current_question_index = session['current_question']
    question_data = session['questions'][current_question_index]
    question = question_data['question']
    correct_answer = question_data['correct_answer']
    incorrect_answers = question_data['incorrect_answers']
    all_answers = incorrect_answers + [correct_answer]
    random.shuffle(all_answers)  # Embaralha as opções

    # Lida com envio do formulário
    if request.method == 'POST':
        option = request.form['options']
        if option == correct_answer:  # Verifica se a resposta está correta
            session['marks'] += 10  # Incrementa a pontuação
        session['current_question'] += 1  # Incrementa o índice para a próxima pergunta
        return redirect(url_for('question', id=(id + 1)))

    # Configura as opções no formulário
    form.options.choices = [(answer, answer) for answer in all_answers]

    # Renderiza o template com a pergunta atual
    return render_template(
        'question.html',
        form=form,
        question=question,
        id=id,
        title=f'Question {id}'
    )

@app.route('/score')
def score():
    if not g.user:
        return redirect(url_for('login'))
    g.user.marks = session['marks']
    # db.session.commit()
    return render_template('score.html', title='Final Score')

@app.route('/logout')
def logout():
    if not g.user:
        return redirect(url_for('login'))
    session.pop('user_id', None)
    session.pop('marks', None)
    return redirect(url_for('home'))