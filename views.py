from flask import render_template, request, redirect, url_for
import functions
from app import app

cadastros = functions.carregar_dados()

#LOGIN
@app.route('/', methods=['GET', 'POST'])
def login():

    cadastros = functions.carregar_dados()
    mensagem_erro = False

    if request.method == 'POST':
        # Captura os dados enviados pelo formulário HTML
        usuario = request.form.get('username')
        senha = request.form.get('password')
        
        # Validação simples
        if usuario in cadastros and senha == cadastros[usuario]:
            if usuario == 'admin':
                return redirect(url_for('admin'))
            return redirect(url_for('dashboard', nome_usuario=usuario))
        
    mensagem_erro = "Usuário ou senha incorretos!"            
    return render_template('login.html', erro=mensagem_erro)

#ÁREA ADM
@app.route('/admin', methods=['POST', 'GET'])
def admin():
    dados_cadastros = functions.carregar_dados()
    stats_delete = request.args.get('stats_delete')

    # Envia os dados com a chave 'usuarios' para o HTML
    return render_template('admin.html', usuarios=dados_cadastros, stats_delete=stats_delete)

#ÁREA ADM/ EDITAR USUARIO
@app.route('/admin/edit_user/<usuario>', methods=['POST', 'GET'])
def edit_user(usuario):

    stats_edit = False
    cadastros = functions.carregar_dados()

    if request.method == 'GET':
        for u in cadastros:
            if u == usuario:
                senha = cadastros[u]
                return render_template('edit_user.html', usuario=usuario, senha=senha)

    if request.method == 'POST':
        usuario_editado = request.form.get('edit_name')
        senha_editada = request.form.get('edit_password')
        senha = cadastros[usuario]
        if not senha_editada:
            for u in cadastros:
                if u == usuario:
                    senha_editada = cadastros[u]

        print(f'a {senha_editada}')
        if usuario_editado in cadastros:
            mensagem_erro = "Usuário já cadastrado!"
            return render_template('edit_user.html', usuario=usuario, senha=senha, erro=mensagem_erro)
        
        elif len(senha_editada) <= 7 or not any(char.isdigit() for char in senha_editada):
            mensagem_erro = "A senha deve conter ao mínimo 8 caracteres e ao menos um número!"
            return render_template('edit_user.html', usuario=usuario, senha=senha, erro=mensagem_erro)
        
        else:
            for u in cadastros:
                if u == usuario:
                    del cadastros[usuario]
                    cadastros[usuario_editado] = senha_editada
                    functions.salvar_dados(cadastros)
                    stats_edit = True
                    return redirect(url_for('admin', stats_edit=stats_edit))

    return render_template('edit_user.html')

#ÁREA ADM/ DELETAR USUÁRIO
@app.route('/admin/delete_user', methods=['POST', 'GET'])
def delete_user():

    stats_delete = False
    usuario_deletado = request.form.get('usuario_deletado')

    if request.method == 'POST':
        cadastros = functions.carregar_dados()
        for u in cadastros:
            if u == usuario_deletado:
                del cadastros[usuario_deletado]
                functions.salvar_dados(cadastros)
                stats_delete = f"O usuário {usuario_deletado} foi deletado com sucesso!"
                return redirect(url_for('admin', stats_delete=stats_delete))
    return render_template('admin.html')

#CADASTRAR
@app.route('/cadaster', methods=['GET', 'POST'])
def cadaster():
   
    if request.method == 'POST':
        cadastro_usuario = request.form.get('cadastro_usuario')
        cadastro_senha = request.form.get('cadastro_senha')

        if cadastro_usuario in cadastros:
            mensagem_erro = "Usuário já cadastrado!"
            return render_template('cadaster.html', erro=mensagem_erro)
        elif len(cadastro_senha) <= 7 or not any(char.isdigit() for char in cadastro_senha):
            mensagem_erro = "A senha deve conter ao mínimo 8 caracteres e ao menos um número!"
            return render_template('cadaster.html', erro=mensagem_erro)
        else:
            cadastros[cadastro_usuario] = cadastro_senha
            functions.salvar_dados(cadastros)
            return render_template('cadaster.html', cadaster=cadastro_usuario)

    return render_template('cadaster.html')
        
#DASHBOARD
@app.route('/dashboard')
def dashboard():
    nome = request.args.get('nome_usuario', 'Visitante')
    return render_template('dashboard.html', nome=nome)
