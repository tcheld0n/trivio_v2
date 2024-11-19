
# Projeto Trivia Game

## Descrição do Projeto

Este projeto é um jogo simples de Trivia, implementado em Python utilizando o framework Flask. Ele inclui autenticação de usuários, um ranking (leaderboard) e jogabilidade baseada em perguntas, onde os jogadores podem testar seus conhecimentos. As perguntas são obtidas de uma API externa e o jogo suporta funcionalidade offline após as perguntas serem carregadas.

## Requisitos

- **Python**: Versão 3.10 ou superior.
- **Framework**: Flask, Flask-SQLAlchemy, Flask-WTF.
- **Banco de Dados**: SQLite (padrão) para persistência.
- **API**: As perguntas são obtidas da Open Trivia Database (https://opentdb.com).

## Instruções de Instalação

Siga os passos abaixo para configurar o ambiente e executar o projeto:

### Passo 1: Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd <diretorio-do-repositorio>
```

### Passo 2: Configurar o Ambiente Virtual

Crie e ative um ambiente virtual Python:

**No Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**No macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instalar as Dependências

Instale os pacotes Python necessários usando `pip`:

```bash
pip install -r requirements.txt
```

### Passo 4: Configurar o Banco de Dados

O projeto utiliza SQLite como banco de dados padrão. Certifique-se de que o arquivo `app.db` seja criado na primeira execução do projeto. Se necessário, inicialize o banco de dados manualmente:

```bash
flask db upgrade
```

### Passo 5: Executar a Aplicação

Inicie o servidor de desenvolvimento do Flask:

```bash
flask run
```

A aplicação estará acessível em `http://127.0.0.1:5000`.

## Como Jogar

1. Acesse a página de login e crie uma nova conta.
2. Após fazer login, inicie um novo jogo.
3. Responda às perguntas exibidas e acompanhe sua pontuação.
4. Visualize sua pontuação final e compare-a no ranking (leaderboard).

## Colaboradores

- **Guilherme Oliveira** - gosg@ic.ufal.br
- **Willian Tcheldon** - wtos@ic.ufal.br

---

Este README fornece instruções básicas de instalação e configuração. Caso encontre algum problema, entre em contato com os colaboradores.
