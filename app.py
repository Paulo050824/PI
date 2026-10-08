from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, abort
from werkzeug.security import generate_password_hash, check_password_hash

from models.tatuagens.avaliacao import Avaliacao
from models.tatuagens.tatuagem import Tatuagem
from models.usuario import Usuario

from repositories import (
    usuario_repository,
    tatuagem_repository,
    avaliacao_repository
)

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # troque por uma chave longa e aleatória antes de publicar


def login_required(funcao):
    @wraps(funcao)
    def verificar(*args, **kwargs):
        if 'id_usuario' not in session:
            return redirect(url_for('login'))
        return funcao(*args, **kwargs)
    return verificar


def admin_required(funcao):
    @wraps(funcao)
    def verificar(*args, **kwargs):
        if 'id_usuario' not in session:
            return redirect(url_for('login'))
        # Confere no banco a cada requisição: se o admin for removido, perde o acesso na hora
        usuario = usuario_repository.buscar_por_id(session['id_usuario'])
        if usuario is None or not usuario.is_admin:
            abort(403)
        return funcao(*args, **kwargs)
    return verificar


# =========================
# PÁGINA INICIAL (PÚBLICA)
# =========================
@app.route('/')
def index():
    return render_template('index.html')


# =========================
# CADASTRO (PÚBLICO)
# =========================
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        # Verifica o e-mail antes de gastar processamento gerando o hash
        if usuario_repository.buscar_por_email(email) is not None:
            return render_template(
                'cadastro.html',
                erro='Este e-mail já está cadastrado.'
            )

        usuario = Usuario(nome, email, generate_password_hash(senha))
        usuario_repository.criar_usuario(usuario)
        return redirect(url_for('login'))

    return render_template('cadastro.html')


# =========================
# LOGIN (PÚBLICO)
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = usuario_repository.buscar_por_email(email)
        if usuario and check_password_hash(usuario.senha_hash, senha):
            session['id_usuario'] = usuario.id
            session['is_admin'] = usuario.is_admin  # só para mostrar/esconder links
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
    session.pop('is_admin', None)
    return redirect(url_for('login'))


# =========================
# PAINEL (PRIVADO)
# =========================
@app.route('/painel')
@login_required
def painel():
    usuario = usuario_repository.buscar_por_id(session['id_usuario'])
    if usuario is None:
        # Conta removida com a sessão ainda aberta
        session.clear()
        return redirect(url_for('login'))
    return render_template('painel.html', usuario=usuario)


# =========================
# TATUAGENS (PÚBLICO)
# =========================
@app.route('/tatuagens')
def tatuagens():
    lista_tatuagens = tatuagem_repository.listar_tatuagens()
    return render_template('tatuagens.html', tatuagens=lista_tatuagens)


# =========================
# CADASTRAR TATUAGEM (SÓ ADMIN)
# =========================
@app.route('/tatuagens/cadastrar', methods=['GET', 'POST'])
@admin_required
def cadastrar_tattoo():
    if request.method == 'POST':
        try:
            nova_tatuagem = Tatuagem(
                nome=request.form['nome'].strip(),
                preco=float(request.form['preco'].replace(',', '.')),
                tamanho=float(request.form['tamanho'].replace(',', '.')),
                imagem=request.form.get('imagem', ''),
                descricao=request.form.get('descricao', '')
            )
        except ValueError:
            return render_template(
                'cadastrar_tattoo.html',
                erro='Preço e tamanho precisam ser números.'
            )

        tatuagem_repository.criar_tatuagem(nova_tatuagem)
        return redirect(url_for('tatuagens'))

    return render_template('cadastrar_tattoo.html')


# =========================
# DETALHE DA TATUAGEM (PÚBLICO)
# =========================
@app.route('/tatuagens/<int:id_tatuagem>')
def detalhe_tatuagem(id_tatuagem):
    tatuagem = tatuagem_repository.buscar_por_id(id_tatuagem)
    if tatuagem is None:
        abort(404)

    return render_template('tatuagem.html', tatuagem=tatuagem)


# =========================
# EXCLUIR TATUAGEM (SÓ ADMIN)
# =========================
@app.route('/tatuagem/<int:id_tatuagem>/excluir', methods=['POST'])
@admin_required
def excluir_tatuagem(id_tatuagem):
    if tatuagem_repository.buscar_por_id(id_tatuagem) is None:
        abort(404)

    tatuagem_repository.excluir_tatuagem(id_tatuagem)
    return redirect(url_for('tatuagens'))


# =========================
# AVALIAR TATUAGEM (PRIVADO)
# =========================
@app.route('/tatuagem/<int:id_tatuagem>/avaliar', methods=['GET', 'POST'])
@login_required
def avaliar_tatuagem(id_tatuagem):
    tatuagem = tatuagem_repository.buscar_por_id(id_tatuagem)
    if tatuagem is None:
        return redirect(url_for('tatuagens'))

    # Já devolve objetos Avaliacao, com .cliente e .nota
    avaliacoes = avaliacao_repository.listar_avaliacoes_por_tatuagem(id_tatuagem)

    if request.method == 'POST':
        # O nome do cliente vem da conta logada, não de um campo editável
        usuario = usuario_repository.buscar_por_id(session['id_usuario'])
        if usuario is None:
            session.clear()
            return redirect(url_for('login'))

        try:
            nota = float(request.form['nota'].replace(',', '.'))
        except ValueError:
            nota = None

        if nota is None or not 0 <= nota <= 5:
            return render_template(
                'avaliar.html',
                tatuagem=tatuagem,
                avaliacoes=avaliacoes,
                erro='A nota precisa ser um número de 0 a 5.'
            )

        avaliacao = Avaliacao(usuario.nome, nota)
        avaliacao_repository.criar_avaliacao(id_tatuagem, avaliacao)

        return redirect(url_for('listar_avaliacoes', id_tatuagem=id_tatuagem))

    return render_template(
        'avaliar.html',
        tatuagem=tatuagem,
        avaliacoes=avaliacoes
    )


# =========================
# LISTAR AVALIAÇÕES (PÚBLICO)
# =========================
@app.route('/tatuagem/<int:id_tatuagem>/avaliacoes')
def listar_avaliacoes(id_tatuagem):
    tatuagem = tatuagem_repository.buscar_por_id(id_tatuagem)
    if tatuagem is None:
        return redirect(url_for('tatuagens'))

    avaliacoes = avaliacao_repository.listar_avaliacoes_por_tatuagem(id_tatuagem)

    return render_template(
        'avaliar.html',
        tatuagem=tatuagem,
        avaliacoes=avaliacoes
    )


# =========================
# EXECUÇÃO
# =========================
if __name__ == '__main__':
    usuario_repository.criar_tabela_usuarios()
    tatuagem_repository.criar_tabela_tatuagens()
    avaliacao_repository.criar_tabela_avaliacoes()

    app.run(debug=True)