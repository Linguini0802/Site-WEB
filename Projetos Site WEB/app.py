from flask import Flask, render_template, request, redirect, url_for
import functions

app = Flask(__name__)

cadastros = functions.carregar_dados()

@app.route('/', methods=['GET', 'POST'])
def login():

    mensagem_erro = False

    if request.method == 'POST':
        # Captura os dados enviados pelo formulário HTML
        usuario = request.form.get('username')
        senha = request.form.get('password')
        
        # Validação simples
        if usuario in cadastros and senha == cadastros[usuario]:
            # Redireciona para a rota do dashboard se as credenciais estiverem corretas
            return redirect(url_for('dashboard', nome_usuario=usuario))
        else:
            mensagem_erro = "Usuário ou senha incorretos!"
            
    return render_template('login.html', erro=mensagem_erro)


@app.route('/cadaster', methods=['GET', 'POST'])
def cadaster():
   
   
    if request.method == 'POST':
        cadastro_usuario = request.form.get('cadastro_usuario')
        cadastro_senha = request.form.get('cadastro_senha')

        if cadastro_usuario in cadastros:
            mensagem_erro = "Usuário já cadastrado!"
            return render_template('cadaster.html', erro=mensagem_erro)
        elif len(cadastro_senha) <= 8 or not any(char.isdigit() for char in cadastro_senha):
            mensagem_erro = "A senha deve conter ao mínimo 8 caracteres e ao menos um número!"
            return render_template('cadaster.html', erro=mensagem_erro)
        else:
            cadastros[cadastro_usuario] = cadastro_senha
            functions.salvar_dados(cadastros)
            return render_template('cadaster.html', cadaster=cadastro_usuario)

    return render_template('cadaster.html')
        
        
@app.route('/dashboard')
def dashboard():
    nome = request.args.get('nome_usuario', 'Visitante')
    return render_template('dashboard.html', nome=nome)

if __name__ == '__main__':
    app.run(debug=True)