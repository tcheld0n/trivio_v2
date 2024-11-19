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
            flash('Usuário ou senha inválidos', 'danger')
            return redirect(url_for('login'))
        session.clear()  # Reinicia a sessão
        session['user_id'] = user.id
        session['marks'] = 0
        return redirect(url_for('home'))
    if g.user:
        return redirect(url_for('home'))
    return render_template('login.html', form=form, title='Login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        session.clear()  # Reinicia a sessão
        session['user_id'] = user.id
        session['marks'] = 0
        return redirect(url_for('home'))
    if g.user:
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/question/<int:id>', methods=['GET', 'POST'])
def question(id):
    form = QuestionForm()

    # Verifica se a sessão foi inicializada corretamente
    if 'questions' not in session or 'current_question' not in session:
        # Faz a chamada para buscar as perguntas
        response = requests.get('https://opentdb.com/api.php?amount=10', verify=False)
        if response.status_code == 200:
            data = response.json()
            if data['response_code'] == 0:
                session['questions'] = data['results']  # Armazena perguntas na sessão
                session['current_question'] = 0        # Inicializa o índice
                session['marks'] = 0                  # Reseta a pontuação
            else:
                return redirect(url_for('score'))
        else:
            return redirect(url_for('score'))

    # Verifica se todas as perguntas foram respondidas
    if session['current_question'] >= len(session['questions']):
        return redirect(url_for('score'))

    # Obtem a pergunta atual
    question_data = session['questions'][session['current_question']]
    question = question_data['question']
    correct_answer = question_data['correct_answer']
    incorrect_answers = question_data['incorrect_answers']
    all_answers = incorrect_answers + [correct_answer]
    random.shuffle(all_answers)  # Embaralha as opções

    # Lida com envio do formulário
    if request.method == 'POST':
        option = request.form['options']
        if option == correct_answer:  # Valida a resposta
            session['marks'] += 10
        session['current_question'] += 1  # Passa para a próxima pergunta
        return redirect(url_for('question', id=(id + 1)))

    # Configura as opções no formulário
    form.options.choices = [(answer, answer) for answer in all_answers]

    # Renderiza o template
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

@app.route('/retake-test')
def retake_test():
    # Limpa a sessão para reiniciar o teste
    session.pop('questions', None)
    session.pop('current_question', None)
    session['marks'] = 0  # Reseta a pontuação
    return redirect(url_for('question', id=1))  # Redireciona para o início do teste
