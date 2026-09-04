from flask import render_template, request, redirect, url_for, session
from main import app
import db.functions as fc

# HOME-PAGE - LOGIN
@app.route("/", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        usuario_login = request.form.get("usuario_login")
        senha_login = request.form.get("senha_login")
        cadastros = fc.carregar_dados_cadastros()

        for user in cadastros.get("usuarios", []):
            if user.get("usuario") == usuario_login:
                if user.get("senha") == senha_login:
                    session['user_id'] = user.get("id")
                    session['usuario'] = user.get("usuario")

                    if usuario_login == "admin":
                        return redirect(url_for('admin')) # Ou 'auth.admin' se estiver usando Blueprints
                    
                    return redirect(url_for('dashboard', id_usuario=user.get("id")))
                else:
                    erro = "Usuário ou senha incorreta!"
                    return render_template("login.html", erro=erro), 401
                
        erro = "O usuário informado não existe!"
        return render_template("login.html", erro=erro), 404

    stats_cadastro = request.args.get("stats_cadastro")
    return render_template('login.html', stats_cadastro=stats_cadastro)# LOGOUT - Encerra a sessão e redireciona para a página de login

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

#PAINEL DO ADMINISTRADOR
@app.route("/admin", methods=['GET'])
def admin():

    if session.get("usuario") != "admin":
        return redirect(url_for('login'))

    cadastros = fc.carregar_dados_cadastros()
    stats_delete = request.args.get("stats_delete")
    stats_edit = request.args.get("stats_edit")
    return render_template('admin.html', cadastros=cadastros, stats_delete=stats_delete, stats_edit=stats_edit) #página normal quando o úsuario abre a página

#ADM/ DELETAR USUÁRIO
@app.route("/admin/delete_user/<int:id>", methods=['GET', 'POST'])
def delete_user(id):

    if session.get("usuario") != "admin":
        return redirect(url_for('login'))

    cadastros = fc.carregar_dados_cadastros()
    for user in cadastros.get("usuarios", []):
        if user.get("id") == id:
            cadastros["usuarios"].remove(user)
            fc.salvar_dados_cadastros(cadastros)
            stats_delete = f'Usuário com o ID "{id}" foi removido com sucesso!'
            return redirect(url_for('admin', stats_delete=stats_delete)) #usuário deletado com sucesso
        
    stats_delete = f'ID "{id}" não encontrado!'
    return redirect(url_for('admin', stats_delete=stats_delete)), 404 #ID não encontrado

#ADM/ EDITAR USUÁRIO
@app.route("/admin/edit_user/<int:id>", methods=['GET', 'POST'])
def edit_user(id):

    if session.get("usuario") != "admin":
        return redirect(url_for('login'))

    cadastros = fc.carregar_dados_cadastros()

    if request.method == 'POST':
        usuario_editado = request.form.get("usuario_editado")
        senha_editado = request.form.get("senha_editado")

        for user in cadastros.get("usuarios", []):
            if not usuario_editado or not usuario_editado.strip():
                if user.get("id") == id:
                    usuario_editado = user.get("usuario")
            if usuario_editado == user.get("usuario") and id != user.get("id"):
                erro = "Nome de usuário já cadastrado!"
                return redirect(url_for('edit_user', id=id, erro=erro)), 409 #Nome de usuario já cadastrado no banco de dados

        for user in cadastros.get("usuarios", []):
            if user.get("id") == id:
                if not senha_editado:
                    senha_editado = user.get("senha")

                elif len(senha_editado) <= 7 or not any(char.isdigit() for char in senha_editado):
                    erro = "A senha deve conter ao mínimo 8 caracteres e ao menos um número!"
                    return redirect(url_for('edit_user', id=id, erro=erro)), 422 #Formato da senha inválido
                else:
                    user["usuario"] = usuario_editado
                    user["senha"] = senha_editado
                    fc.salvar_dados_cadastros(cadastros)
                    stats_edit = "Usuário editado com sucesso"
                    return redirect(url_for("admin", stats_edit=stats_edit)) #as alterações deram certo

    for user in cadastros.get("usuarios", []):
        if user.get("id") == id:
            erro = request.args.get("erro")
            return render_template("edit_user.html", erro=erro, id=id, usuario=user.get("usuario"), senha=user.get("senha")) #página normal quando o úsuario abre a página
    erro = "Usuário não encontrado!"
    return render_template("edit_user.html", erro=erro), 404 #usuario não foi encontrado no banco de dados

#CADASTRO DE USUÁRIOS
@app.route("/cadaster", methods=['GET', 'POST'])
def cadaster():

    if request.method == 'POST':
        usuario_cadastro = request.form.get("usuario_cadastro")
        senha_cadastro = request.form.get("senha_cadastro")
        senha_cadastro_confirmar = request.form.get("senha_cadastro_confirmar")
        cadastros = fc.carregar_dados_cadastros()

        for user in cadastros.get("usuarios", []):
            if user.get("usuario") == usuario_cadastro:
                erro = "Nome de usuário já cadastrado!"
                return render_template("cadaster.html", erro=erro), 409 #Nome de usuario já cadastrado no banco de dados
        if len(senha_cadastro) <= 7 or not any(char.isdigit() for char in senha_cadastro):
            erro = "A senha deve conter ao mínimo 8 caracteres e ao menos um número!"
            return render_template("cadaster.html", erro=erro), 422 #Formato da senha inválido
        if senha_cadastro != senha_cadastro_confirmar:
            erro = "As senhas não coincidem"
            return render_template("cadaster.html", erro=erro), 400 #Senhas informadas não coincidem
        novo_usuario = {
            "id": cadastros.get("proximo_id"),
            "usuario": usuario_cadastro,
            "senha": senha_cadastro
        }
        cadastros["usuarios"].append(novo_usuario)
        cadastros["proximo_id"] += 1
        fc.salvar_dados_cadastros(cadastros)
        stats_cadastro = f"O usuário '{usuario_cadastro}' foi cadastrado com sucesso!"
        return redirect(url_for("login", stats_cadastro=stats_cadastro)) #se o cadastro der certo, ele redireciona para a página de login confirmando o cdastro
        
    return render_template("cadaster.html") #página normal quando o úsuario abre a página

# DASHBOARD APÓS O LOGIN
@app.route("/dashboard/<int:id_usuario>", methods=['GET', 'POST'])
def dashboard(id_usuario):
    #Trava de segurança: se não estiver logado, manda pro login
    if 'user_id' not in session:
        return redirect(url_for('login'))

    videos = fc.carregar_dados_videos()
    usuario = session.get("usuario")

    if request.method == 'POST':
        nome_video = request.form.get("nome_video")
        url_video = request.form.get("url_video")
        usuario_video = request.form.get("usuario_video")
        if not usuario_video:
            cadastros = fc.carregar_dados_cadastros()
            for user in cadastros.get("usuarios", []):
                if user.get("id") == id_usuario:
                    usuario_video = user["usuario"]
                    break
    
        novo_video = {
            "id": videos["proximo_id"],
            "id_usuario": id_usuario,
            "nome_usuario": usuario_video,
            "nome_video": nome_video,
            "url_video": url_video
        }

        videos["videos"].append(novo_video)
        videos["proximo_id"] += 1
        fc.salvar_dados_videos(videos)
        stats_video = "Vídeo inserido com sucesso!"
        return redirect(url_for('dashboard', stats_video=stats_video, id_usuario=id_usuario)), 200

    stats_video = request.args.get("stats_video")
    stats_delete = request.args.get("stats_delete")
    return render_template('dashboard.html', usuario=usuario, videos=videos, stats_video=stats_video, stats_delete=stats_delete, id_usuario=id_usuario) #página normal quando o úsuario abre a página

# DELETAR VÍDEO
@app.route("/dashboard/delete_video/<int:id>", methods=['POST'])
def delete_video(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    videos = fc.carregar_dados_videos()

    for video in videos.get("videos", []):
        if video.get("id") == id:
            id_usuario_dono = video.get("id_usuario") # Recupera o dono do vídeo
            videos["videos"].remove(video)
            fc.salvar_dados_videos(videos)
            stats_delete = "Vídeo removido com sucesso!"
            return redirect(url_for('dashboard', stats_delete=stats_delete, id_usuario=id_usuario_dono))

    stats_delete = "Vídeo não encontrado"
    return redirect(url_for('dashboard', stats_delete=stats_delete, id_usuario=session.get('user_id'))), 404