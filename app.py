from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session

from werkzeug.security import generate_password_hash, check_password_hash

from models.tatuagens.avaliacao import Avaliacao

from models.tatuagens.tatuagem import Tatuagem

from models.usuario import Usuario

from repositories import (usuario_repository,tatuagem_repository,avaliacao_repository,catalago_repository)


app = Flask(__name__)

app.secret_key = 'sua_chave_secreta'


def login_required(funcao):

    @wraps(funcao)

    def verificar(*args, **kwargs):

        if 'id_usuario' not in session:

            return redirect(url_for('login'))

        return funcao(*args, **kwargs)

    return verificar


# =========================

# CADASTRO

# =========================

@app.route('/cadastro', methods=['GET', 'POST'])

def cadastro():

    if request.method == 'POST':

        nome = request.form['nome']

        email = request.form['email']

        senha = request.form['senha']

        senha_hash = generate_password_hash(senha)

        usuario = usuario_repository.buscar_por_email(email)

        if usuario is not None:

            return render_template(

                'cadastro.html',

                erro='Este e-mail já está cadastrado.'

            )

        usuario = Usuario(nome, email, senha_hash)

        usuario_repository.criar_usuario(usuario)

        return redirect(url_for('login'))
    return render_template('cadastro.html')


# =========================

# LOGIN

# =========================

@app.route('/login', methods=['GET', 'POST'])

def login():

    if request.method == 'POST':

        email = request.form['email']

        senha = request.form['senha']

        usuario = usuario_repository.buscar_por_email(email)

        if usuario is not None and check_password_hash(

            usuario.senha_hash,

            senha

        ):

            session['id_usuario'] = usuario.id_usuario

            return redirect(url_for('painel'))

        return render_template(

            'login.html',

            erro='E-mail ou senha inválidos.'

        )

    return render_template('login.html')


# =========================

# LOGOUT

# =========================

@app.route('/logout')

def logout():

    session.pop('id_usuario', None)

    return redirect(url_for('login'))


# =========================

# PAINEL

# =========================

@app.route('/painel')

@login_required

def painel():

    usuario = usuario_repository.buscar_por_id(

        session['id_usuario']

    )

    return render_template(

        'painel.html',

        usuario=usuario

    )


# =========================

# TATUAGENS

# =========================

@app.route('/tatuagens')

@login_required

def tatuagens():

    lista_tatuagens = tatuagem_repository.listar_tatuagens()

    return render_template(

        'tatuagem.html',

        tatuagens=lista_tatuagens

    )


# =========================

# AVALIAR TATUAGEM

# =========================

@app.route('/tatuagem/<int:id_tatuagem>/avaliar',

           methods=['GET', 'POST'])

@login_required

def avaliar_tatuagem(id_tatuagem):

    tatuagem = tatuagem_repository.buscar_por_id(

        id_tatuagem

    )

    if tatuagem is None:

        return redirect(url_for('tatuagens'))

    if request.method == 'POST':

        cliente = request.form['cliente']

        nota = float(request.form['nota'])

        avaliacao = Avaliacao(

            cliente,

            nota

        )

        avaliacao_repository.criar_avaliacao(

            id_tatuagem,

            avaliacao

        )

        return redirect(

            url_for(

                'listar_avaliacoes',

                id_tatuagem=id_tatuagem

            )

        )

    return render_template(

        'avaliar.html',

        tatuagem=tatuagem

    )


# =========================

# LISTAR AVALIAÇÕES

# =========================

@app.route('/tatuagem/<int:id_tatuagem>/avaliacoes')

@login_required

def listar_avaliacoes(id_tatuagem):

    tatuagem = tatuagem_repository.buscar_por_id(

        id_tatuagem

    )

    avaliacoes = avaliacao_repository.listar_completo(

        id_tatuagem

    )

    if tatuagem is None:

        return redirect(url_for('tatuagens'))

    return render_template(

        'avaliacoes.html',

        tatuagem=tatuagem,

        avaliacoes=avaliacoes

    )


# =========================

# CATÁLOGO

# =========================

@app.route('/tatuagens/<int:id_tatuagem>/catalogo')

@login_required

def listar_catalogo(id_tatuagem):

    tatuagem = tatuagem_repository.buscar_por_id(

        id_tatuagem

    )

    if tatuagem is None:

        return redirect(url_for('tatuagens'))

    itens = catalago_repository.listar_por_tatuagem(

        id_tatuagem

    )

    return render_template(

        'catalogo.html',

        tatuagem=tatuagem,

        itens=itens

    )


# =========================

# EXECUÇÃO

# =========================

if __name__ == '__main__':

    usuario_repository.criar_tabela_usuarios()

    tatuagem_repository.criar_tabela_tatuagens()

    avaliacao_repository.criar_tabela_avaliacoes()
    avaliacao_repository.listar_avaliacoes_por_tatuagem(1)
    catalago_repository.criar_tabela_catalogos()

    app.run(debug=True)

 