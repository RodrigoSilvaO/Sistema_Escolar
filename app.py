import time
from functools import wraps

from flask import Flask, request, render_template, session, redirect, url_for

from db.db import executar_insert_delete_update, executar_select

app = Flask(__name__)
app.secret_key = "sistema_escolar"

USUARIOS = {
    "Rodrigo": {
        "senha": "Rodrigo",
        "nome": "Rodrigo da Silva",
        "perfil": "DEV",
        "foto": "Rodrigo.png"
    },
    "Andre": {
        "senha": "Andre",
        "nome": "Andre Madureira",
        "perfil": "Professor",
        "foto": "Andre.png"
    },
    "Aryan": {
        "senha": "Aryan",
        "nome": "Aryan Assis",
        "perfil": "DEV",
        "foto": "Aryan.png"
    },
    "Helena": {
        "senha": "Helena",
        "nome": "Helena Freitas",
        "perfil": "DEV",
        "foto": "Helena.png"
    },
    "Saulo": {
        "senha": "Saulo",
        "nome": "Saulo Henrique",
        "perfil": "DEV",
        "foto": "Saulo.png"
    }
}
NOME_BANCO = "sistema_escolar"

STATUS_PRESENCA_OPCOES = [
    ("Presente", "Presente"),
    ("Ausente", "Ausente"),
    ("Justificada", "Justificada"),
]
SITUACAO_OPCOES = [
    ("Aprovado", "Aprovado"),
    ("Reprovado", "Reprovado"),
    ("Recuperacao", "Recuperacao"),
]
FREQUENCIA_OPCOES = [
    ("Presente", "Presente"),
    ("Ausente", "Ausente"),
    ("Justificado", "Justificado"),
]

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def perfil_requerido(perfil_necessario):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'usuario' not in session:
                return redirect(url_for('login'))
            if session['usuario']['perfil'] != perfil_necessario:
                return "ACESSO NEGADO: Você não tem permissão para acessar esta área.", 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def buscar_especialidades():
    return executar_select(db=NOME_BANCO, consulta_sql="SELECT id_especialidade, especialidade FROM especialidade_professor")

def buscar_professores():
    return executar_select(db=NOME_BANCO, consulta_sql="SELECT id_professor, nome FROM professor")

def buscar_disciplinas():
    return executar_select(db=NOME_BANCO, consulta_sql="SELECT id_disciplina, nome FROM disciplina")

def buscar_periodos():
    return executar_select(db=NOME_BANCO, consulta_sql="SELECT id_periodo, descricao FROM periodo_letivo")

def buscar_turmas():
    return executar_select(db=NOME_BANCO, consulta_sql="SELECT id_turma, nome FROM turma")

def buscar_alunos():
    return executar_select(db=NOME_BANCO, consulta_sql="SELECT id_aluno, nome FROM aluno")


@app.route('/', methods=['GET'])
@login_required
def home():
    return render_template(
        'index.jinja2',
        usuario=session['usuario']
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        if usuario in USUARIOS and USUARIOS[usuario]["senha"] == senha:
            dados_usuario = USUARIOS[usuario].copy()
            dados_usuario["usuario"] = usuario
            session["usuario"] = dados_usuario
            return redirect(url_for('home'))

        return render_template(
            'login.jinja2',
            erro='Usuário ou senha incorretos.'
        )
    return render_template('login.jinja2')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/cadastrar/aluno', methods=['GET'])
@perfil_requerido('DEV')
def tela_cadastrar_aluno():
    return render_template(
        'cadastrar/aluno.jinja2',
        api='/api/cadastrar/aluno',
    )

@app.route('/atualizar/aluno', methods=['GET'])
@perfil_requerido('DEV')
def tela_atualizar_aluno():
    registros = executar_select(
        db=NOME_BANCO,
        consulta_sql="""
            SELECT id_aluno, nome, data_nascimento, endereco, data_matricula
            FROM aluno
            WHERE id_aluno = %s
        """,
        parametros=(request.args.get('id_aluno') or "",)
    )
    if len(registros) <= 0:
        return "ERRO: Consulta de aluno falhou. Veja logs do Python para detalhes."
    id_aluno, nome, data_nascimento, endereco, data_matricula = registros[0]
    return render_template(
        'atualizar/aluno.jinja2',
        api='/api/atualizar/aluno',
        id_aluno=id_aluno,
        nome=nome,
        data_nascimento=data_nascimento,
        endereco=endereco,
        data_matricula=data_matricula,
    )

@app.route('/consultar/aluno', methods=['GET'])
@perfil_requerido('DEV')
def tela_consultar_aluno():
    registros = executar_select(
        db=NOME_BANCO,
        consulta_sql="""
            SELECT id_aluno, nome, data_nascimento, endereco, data_matricula
            FROM aluno
        """
    )
    cabecalho = ["ID", "Nome", "Data de Nascimento", "Endereco", "Data de Matricula"]
    return render_template(
        'consultar.jinja2',
        titulo='Alunos',
        api_atualizar='/atualizar/aluno',
        api_apagar='/api/apagar/aluno',
        campos_chave=[("ID do Aluno:", "id_aluno")],
        cabecalho=cabecalho,
        dados=registros,
    )


@app.route('/cadastrar/especialidade_professor', methods=['GET'])
@perfil_requerido('DEV')
def tela_cadastrar_especialidade_professor():
    return render_template(
        'cadastrar/especialidade_professor.jinja2',
        api='/api/cadastrar/especialidade_professor',
    )

@app.route('/atualizar/especialidade_professor', methods=['GET'])
@perfil_requerido('DEV')
def tela_atualizar_especialidade_professor():
    registros = executar_select(
        db=NOME_BANCO,
        consulta_sql="""
            SELECT id_especialidade, especialidade
            FROM especialidade_professor
            WHERE id_especialidade = %s
        """,
        parametros=(request.args.get('id_especialidade') or "",)
    )
    if len(registros) <= 0:
        return "ERRO: Consulta de especialidade falhou. Veja logs do Python para detalhes."
    id_especialidade, especialidade = registros[0]
    return render_template(
        'atualizar/especialidade_professor.jinja2',
        api='/api/atualizar/especialidade_professor',
        id_especialidade=id_especialidade,
        especialidade=especialidade,
    )

@app.route('/consultar/especialidade_professor', methods=['GET'])
@perfil_requerido('DEV')
def tela_consultar_especialidade_professor():
    registros = executar_select(
        db=NOME_BANCO,
        consulta_sql="SELECT id_especialidade, especialidade FROM especialidade_professor"
    )
    cabecalho = ["ID", "Especialidade"]
    return render_template(
        'consultar.jinja2',
        titulo='Especialidades de Professor',
        api_atualizar='/atualizar/especialidade_professor',
        api_apagar='/api/apagar/especialidade_professor',
        campos_chave=[("ID da Especialidade:", "id_especialidade")],
        cabecalho=cabecalho,
        dados=registros,
    )


@app.route('/cadastrar/professor', methods=['GET'])
@perfil_requerido('DEV')
def tela_cadastrar_professor():
    return render_template(
        'cadastrar/professor.jinja2',
        api='/api/cadastrar/professor',
        especialidades=buscar_especialidades(),
    )

@app.route('/atualizar/professor', methods=['GET'])
@perfil_requerido('DEV')
def tela_atualizar_professor():
    registros = executar_select(
        db=NOME_BANCO,
        consulta_sql="""
            SELECT id_professor, nome, id_especialidade
            FROM professor
            WHERE id_professor = %s
        """,
        parametros=(request.args.get('id_professor') or "",)
    )
    if len(registros) <= 0:
        return "ERRO: Consulta de professor falhou. Veja logs do Python para detalhes."
    id_professor, nome, id_especialidade = registros[0]
    return render_template(
        'atualizar/professor.jinja2',
        api='/api/atualizar/professor',
        especialidades=buscar_especialidades(),
        id_professor=id_professor,
        nome=nome,
        id_especialidade=id_especialidade,
    )

@app.route('/consultar/professor', methods=['GET'])
@perfil_requerido('DEV')
def tela_consultar_professor():
    registros = executar_select(
        db=NOME_BANCO,
        consulta_sql="""
            SELECT p.id_professor, p.nome, e.especialidade
            FROM professor p, especialidade_professor e
            WHERE p.id_especialidade = e.id_especialidade
        """
    )
    cabecalho = ["ID", "Nome", "Especialidade"]
    return render_template(
        'consultar.jinja2',
        titulo='Professores',
        api_atualizar='/atualizar/professor',
        api_apagar='/api/apagar/professor',
        campos_chave=[("ID do Professor:", "id_professor")],
        cabecalho=cabecalho,
        dados=registros,
    )


@app.route('/cadastrar/disciplina', methods=['GET'])
@perfil_requerido('DEV')
def tela_cadastrar_disciplina():
    return render_template(
        'cadastrar/disciplina.jinja2',
        api='/api/cadastrar/disciplina',
    )

@app.route('/atualizar/disciplina', methods=['GET'])
@perfil_requerido('DEV')
def tela_atualizar_disciplina():
    registros = executar_select(
        db=NOME_BANCO,
        consulta_sql="""
            SELECT id_disciplina, nome, carga_horaria, tipo
            FROM disciplina
            WHERE id_disciplina = %s
        """,
        parametros=(request.args.get('id_disciplina') or "",)
    )
    if len(registros) <= 0:
        return "ERRO: Consulta de disciplina falhou. Veja logs do Python para detalhes."
    id_disciplina, nome, carga_horaria, tipo = registros[0]
    return render_template(
        'atualizar/disciplina.jinja2',
        api='/api/atualizar/disciplina',
        id_disciplina=id_disciplina,
        nome=nome,
        carga_horaria=carga_horaria,
        tipo=tipo,
    )

@app.route('/consultar/disciplina', methods=['GET'])
@perfil_requerido('DEV')
def tela_consultar_disciplina():
    registros = executar_select(
        db=NOME_BANCO,
        consulta_sql="SELECT id_disciplina, nome, carga_horaria, tipo FROM disciplina"
    )
    cabecalho = ["ID", "Nome", "Carga Horaria", "Tipo"]
    return render_template(
        'consultar.jinja2',
        titulo='Disciplinas',
        api_atualizar='/atualizar/disciplina',
        api_apagar='/api/apagar/disciplina',
        campos_chave=[("ID da Disciplina:", "id_disciplina")],
        cabecalho=cabecalho,
        dados=registros,
    )


@app.route('/cadastrar/disciplina_professor', methods=['GET'])
@perfil_requerido('DEV')
def tela_cadastrar_disciplina_professor():
    return render_template(
        'cadastrar/disciplina_professor.jinja2',
        api='/api/cadastrar/disciplina_professor',
        professores=buscar_professores(),
        disciplinas=buscar_disciplinas(),
    )

@app.route('/consultar/disciplina_professor', methods=['GET'])
@perfil_requerido('DEV')
def tela_consultar_disciplina_professor():
    registros = executar_select(
        db=NOME_BANCO,
        consulta_sql="""
            SELECT p.id_professor, p.nome, d.id_disciplina, d.nome
            FROM disciplina_professor dp, professor p, disciplina d
            WHERE dp.id_professor = p.id_professor AND dp.id_disciplina = d.id_disciplina
        """
    )
    cabecalho = ["ID Professor", "Professor", "ID Disciplina", "Disciplina"]
    return render_template(
        'consultar.jinja2',
        titulo='Disciplinas x Professores',
        api_atualizar=None,
        api_apagar='/api/apagar/disciplina_professor',
        campos_chave=[("ID do Professor:", "id_professor"), ("ID da Disciplina:", "id_disciplina")],
        cabecalho=cabecalho,
        dados=registros,
    )


@app.route('/cadastrar/periodo_letivo', methods=['GET'])
@perfil_requerido('DEV')
def tela_cadastrar_periodo_letivo():
    return render_template(
        'cadastrar/periodo_letivo.jinja2',
        api='/api/cadastrar/periodo_letivo',
    )

@app.route('/atualizar/periodo_letivo', methods=['GET'])
@perfil_requerido('DEV')
def tela_atualizar_periodo_letivo():
    registros = executar_select(
        db=NOME_BANCO,
        consulta_sql="""
            SELECT id_periodo, descricao, data_inicio, data_fim
            FROM periodo_letivo
            WHERE id_periodo = %s
        """,
        parametros=(request.args.get('id_periodo') or "",)
    )
    if len(registros) <= 0:
        return "ERRO: Consulta de periodo letivo falhou. Veja logs do Python para detalhes."
    id_periodo, descricao, data_inicio, data_fim = registros[0]
    return render_template(
        'atualizar/periodo_letivo.jinja2',
        api='/api/atualizar/periodo_letivo',
        id_periodo=id_periodo,
        descricao=descricao,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )

@app.route('/consultar/periodo_letivo', methods=['GET'])
@perfil_requerido('DEV')
def tela_consultar_periodo_letivo():
    registros = executar_select(
        db=NOME_BANCO,
        consulta_sql="SELECT id_periodo, descricao, data_inicio, data_fim FROM periodo_letivo"
    )
    cabecalho = ["ID", "Descricao", "Data de Inicio", "Data de Fim"]
    return render_template(
        'consultar.jinja2',
        titulo='Periodos Letivos',
        api_atualizar='/atualizar/periodo_letivo',
        api_apagar='/api/apagar/periodo_letivo',
        campos_chave=[("ID do Periodo:", "id_periodo")],
        cabecalho=cabecalho,
        dados=registros,
    )


@app.route('/cadastrar/periodo_ferias', methods=['GET'])
@perfil_requerido('DEV')
def tela_cadastrar_periodo_ferias():
    return render_template(
        'cadastrar/periodo_ferias.jinja2',
        api='/api/cadastrar/periodo_ferias',
        periodos=buscar_periodos(),
    )

@app.route('/atualizar/periodo_ferias', methods=['GET'])
@perfil_requerido('DEV')
def tela_atualizar_periodo_ferias():
    registros = executar_select(
        db=NOME_BANCO,
        consulta_sql="""
            SELECT id_ferias, id_periodo, data_inicio, data_fim
            FROM periodo_ferias
            WHERE id_ferias = %s
        """,
        parametros=(request.args.get('id_ferias') or "",)
    )
    if len(registros) <= 0:
        return "ERRO: Consulta de periodo de ferias falhou. Veja logs do Python para detalhes."
    id_ferias, id_periodo, data_inicio, data_fim = registros[0]
    return render_template(
        'atualizar/periodo_ferias.jinja2',
        api='/api/atualizar/periodo_ferias',
        periodos=buscar_periodos(),
        id_ferias=id_ferias,
        id_periodo=id_periodo,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )

@app.route('/consultar/periodo_ferias', methods=['GET'])
@perfil_requerido('DEV')
def tela_consultar_periodo_ferias():
    registros = executar_select(
        db=NOME_BANCO,
        consulta_sql="""
            SELECT f.id_ferias, p.descricao, f.data_inicio, f.data_fim
            FROM periodo_ferias f, periodo_letivo p
            WHERE f.id_periodo = p.id_periodo
        """
    )
    cabecalho = ["ID", "Periodo Letivo", "Data de Inicio", "Data de Fim"]
    return render_template(
        'consultar.jinja2',
        titulo='Periodos de Ferias',
        api_atualizar='/atualizar/periodo_ferias',
        api_apagar='/api/apagar/periodo_ferias',
        campos_chave=[("ID das Ferias:", "id_ferias")],
        cabecalho=cabecalho,
        dados=registros,
    )


@app.route('/cadastrar/turma', methods=['GET'])
@perfil_requerido('DEV')
def tela_cadastrar_turma():
    return render_template(
        'cadastrar/turma.jinja2',
        api='/api/cadastrar/turma',
        periodos=buscar_periodos(),
    )

@app.route('/atualizar/turma', methods=['GET'])
@perfil_requerido('DEV')
def tela_atualizar_turma():
    registros = executar_select(
        db=NOME_BANCO,
        consulta_sql="""
            SELECT id_turma, nome, id_periodo
            FROM turma
            WHERE id_turma = %s
        """,
        parametros=(request.args.get('id_turma') or "",)
    )
    if len(registros) <= 0:
        return "ERRO: Consulta de turma falhou. Veja logs do Python para detalhes."
    id_turma, nome, id_periodo = registros[0]
    return render_template(
        'atualizar/turma.jinja2',
        api='/api/atualizar/turma',
        periodos=buscar_periodos(),
        id_turma=id_turma,
        nome=nome,
        id_periodo=id_periodo,
    )

@app.route('/consultar/turma', methods=['GET'])
@perfil_requerido('DEV')
def tela_consultar_turma():
    registros = executar_select(
        db=NOME_BANCO,
        consulta_sql="""
            SELECT t.id_turma, t.nome, p.descricao
            FROM turma t, periodo_letivo p
            WHERE t.id_periodo = p.id_periodo
        """
    )
    cabecalho = ["ID", "Nome", "Periodo Letivo"]
    return render_template(
        'consultar.jinja2',
        titulo='Turmas',
        api_atualizar='/atualizar/turma',
        api_apagar='/api/apagar/turma',
        campos_chave=[("ID da Turma:", "id_turma")],
        cabecalho=cabecalho,
        dados=registros,
    )


@app.route('/cadastrar/turma_disciplina', methods=['GET'])
@perfil_requerido('DEV')
def tela_cadastrar_turma_disciplina():
    return render_template(
        'cadastrar/turma_disciplina.jinja2',
        api='/api/cadastrar/turma_disciplina',
        turmas=buscar_turmas(),
        disciplinas=buscar_disciplinas(),
        professores=buscar_professores(),
    )

@app.route('/consultar/turma_disciplina', methods=['GET'])
@perfil_requerido('DEV')
def tela_consultar_turma_disciplina():
    registros = executar_select(
        db=NOME_BANCO,
        consulta_sql="""
            SELECT t.id_turma, t.nome, d.nome, p.nome
            FROM turma_disciplina td, turma t, disciplina d, professor p
            WHERE td.id_turma = t.id_turma
              AND td.id_disciplina = d.id_disciplina
              AND td.id_professor = p.id_professor
        """
    )
    cabecalho = ["ID Turma", "Turma", "Disciplina", "Professor"]
    return render_template(
        'consultar.jinja2',
        titulo='Turmas x Disciplinas',
        api_atualizar=None,
        api_apagar='/api/apagar/turma_disciplina',
        campos_chave=[
            ("ID da Turma:", "id_turma"),
            ("ID da Disciplina:", "id_disciplina"),
            ("ID do Professor:", "id_professor"),
        ],
        cabecalho=cabecalho,
        dados=registros,
    )


@app.route('/cadastrar/matricula_disciplina', methods=['GET'])
@perfil_requerido('DEV')
def tela_cadastrar_matricula_disciplina():
    return render_template(
        'cadastrar/matricula_disciplina.jinja2',
        api='/api/cadastrar/matricula_disciplina',
        alunos=buscar_alunos(),
        disciplinas=buscar_disciplinas(),
        turmas=buscar_turmas(),
    )

@app.route('/consultar/matricula_disciplina', methods=['GET'])
@perfil_requerido('DEV')
def tela_consultar_matricula_disciplina():
    registros = executar_select(
        db=NOME_BANCO,
        consulta_sql="""
            SELECT a.id_aluno, a.nome, d.nome, t.nome
            FROM matricula_disciplina m, aluno a, disciplina d, turma t
            WHERE m.id_aluno = a.id_aluno
              AND m.id_disciplina = d.id_disciplina
              AND m.id_turma = t.id_turma
        """
    )
    cabecalho = ["ID Aluno", "Aluno", "Disciplina", "Turma"]
    return render_template(
        'consultar.jinja2',
        titulo='Matriculas em Disciplinas',
        api_atualizar=None,
        api_apagar='/api/apagar/matricula_disciplina',
        campos_chave=[
            ("ID do Aluno:", "id_aluno"),
            ("ID da Disciplina:", "id_disciplina"),
            ("ID da Turma:", "id_turma"),
        ],
        cabecalho=cabecalho,
        dados=registros,
    )


@app.route('/cadastrar/avaliacao', methods=['GET'])
@login_required
def tela_cadastrar_avaliacao():
    return render_template(
        'cadastrar/avaliacao.jinja2',
        api='/api/cadastrar/avaliacao',
        alunos=buscar_alunos(),
        disciplinas=buscar_disciplinas(),
    )

@app.route('/atualizar/avaliacao', methods=['GET'])
@login_required
def tela_atualizar_avaliacao():
    registros = executar_select(
        db=NOME_BANCO,
        consulta_sql="""
            SELECT id_boletim, observacao, numero_avaliacao, nota, data_avaliacao, id_aluno, id_disciplina
            FROM avaliacao
            WHERE id_boletim = %s
        """,
        parametros=(request.args.get('id_boletim') or "",)
    )
    if len(registros) <= 0:
        return "ERRO: Consulta de avaliacao falhou. Veja logs do Python para detalhes."
    id_boletim, observacao, numero_avaliacao, nota, data_avaliacao, id_aluno, id_disciplina = registros[0]
    return render_template(
        'atualizar/avaliacao.jinja2',
        api='/api/atualizar/avaliacao',
        alunos=buscar_alunos(),
        disciplinas=buscar_disciplinas(),
        id_boletim=id_boletim,
        observacao=observacao,
        numero_avaliacao=numero_avaliacao,
        nota=nota,
        data_avaliacao=data_avaliacao,
        id_aluno=id_aluno,
        id_disciplina=id_disciplina,
    )

@app.route('/consultar/avaliacao', methods=['GET'])
@login_required
def tela_consultar_avaliacao():
    registros = executar_select(
        db=NOME_BANCO,
        consulta_sql="""
            SELECT av.id_boletim, a.nome, d.nome, av.numero_avaliacao, av.nota, av.data_avaliacao
            FROM avaliacao av, aluno a, disciplina d
            WHERE av.id_aluno = a.id_aluno AND av.id_disciplina = d.id_disciplina
        """
    )
    cabecalho = ["ID Boletim", "Aluno", "Disciplina", "Numero Avaliacao", "Nota", "Data"]
    return render_template(
        'consultar.jinja2',
        titulo='Avaliacoes',
        api_atualizar='/atualizar/avaliacao',
        api_apagar='/api/apagar/avaliacao',
        campos_chave=[("ID do Boletim:", "id_boletim")],
        cabecalho=cabecalho,
        dados=registros,
    )


@app.route('/cadastrar/registro_frequencia', methods=['GET'])
@login_required
def tela_cadastrar_registro_frequencia():
    return render_template(
        'cadastrar/registro_frequencia.jinja2',
        api='/api/cadastrar/registro_frequencia',
        alunos=buscar_alunos(),
        disciplinas=buscar_disciplinas(),
        status_opcoes=STATUS_PRESENCA_OPCOES,
    )

@app.route('/atualizar/registro_frequencia', methods=['GET'])
@login_required
def tela_atualizar_registro_frequencia():
    registros = executar_select(
        db=NOME_BANCO,
        consulta_sql="""
            SELECT id_frequencia, id_aluno, id_disciplina, data_aula, status_presenca
            FROM registro_frequencia
            WHERE id_frequencia = %s
        """,
        parametros=(request.args.get('id_frequencia') or "",)
    )
    if len(registros) <= 0:
        return "ERRO: Consulta de registro de frequencia falhou. Veja logs do Python para detalhes."
    id_frequencia, id_aluno, id_disciplina, data_aula, status_presenca = registros[0]
    return render_template(
        'atualizar/registro_frequencia.jinja2',
        api='/api/atualizar/registro_frequencia',
        alunos=buscar_alunos(),
        disciplinas=buscar_disciplinas(),
        status_opcoes=STATUS_PRESENCA_OPCOES,
        id_frequencia=id_frequencia,
        id_aluno=id_aluno,
        id_disciplina=id_disciplina,
        data_aula=data_aula,
        status_presenca=status_presenca,
    )

@app.route('/consultar/registro_frequencia', methods=['GET'])
@login_required
def tela_consultar_registro_frequencia():
    registros = executar_select(
        db=NOME_BANCO,
        consulta_sql="""
            SELECT rf.id_frequencia, a.nome, d.nome, rf.data_aula, rf.status_presenca
            FROM registro_frequencia rf, aluno a, disciplina d
            WHERE rf.id_aluno = a.id_aluno AND rf.id_disciplina = d.id_disciplina
        """
    )
    cabecalho = ["ID", "Aluno", "Disciplina", "Data da Aula", "Status"]
    return render_template(
        'consultar.jinja2',
        titulo='Registros de Frequencia',
        api_atualizar='/atualizar/registro_frequencia',
        api_apagar='/api/apagar/registro_frequencia',
        campos_chave=[("ID da Frequencia:", "id_frequencia")],
        cabecalho=cabecalho,
        dados=registros,
    )


@app.route('/cadastrar/resultado_final', methods=['GET'])
@login_required
def tela_cadastrar_resultado_final():
    return render_template(
        'cadastrar/resultado_final.jinja2',
        api='/api/cadastrar/resultado_final',
        alunos=buscar_alunos(),
        disciplinas=buscar_disciplinas(),
        situacao_opcoes=SITUACAO_OPCOES,
        frequencia_opcoes=FREQUENCIA_OPCOES,
    )

@app.route('/atualizar/resultado_final', methods=['GET'])
@login_required
def tela_atualizar_resultado_final():
    registros = executar_select(
        db=NOME_BANCO,
        consulta_sql="""
            SELECT id_aluno, id_disciplina, situacao, frequencia
            FROM resultado_final
            WHERE id_aluno = %s AND id_disciplina = %s
        """,
        parametros=(
            request.args.get('id_aluno') or "",
            request.args.get('id_disciplina') or "",
        )
    )
    if len(registros) <= 0:
        return "ERRO: Consulta de resultado final falhou. Veja logs do Python para detalhes."
    id_aluno, id_disciplina, situacao, frequencia = registros[0]
    return render_template(
        'atualizar/resultado_final.jinja2',
        api='/api/atualizar/resultado_final',
        situacao_opcoes=SITUACAO_OPCOES,
        frequencia_opcoes=FREQUENCIA_OPCOES,
        id_aluno=id_aluno,
        id_disciplina=id_disciplina,
        situacao=situacao,
        frequencia=frequencia,
    )

@app.route('/consultar/resultado_final', methods=['GET'])
@login_required
def tela_consultar_resultado_final():
    registros = executar_select(
        db=NOME_BANCO,
        consulta_sql="""
            SELECT r.id_aluno, a.nome, d.nome, r.situacao, r.frequencia
            FROM resultado_final r, aluno a, disciplina d
            WHERE r.id_aluno = a.id_aluno AND r.id_disciplina = d.id_disciplina
        """
    )
    cabecalho = ["ID Aluno", "Aluno", "Disciplina", "Situacao", "Frequencia"]
    return render_template(
        'consultar.jinja2',
        titulo='Resultados Finais',
        api_atualizar='/atualizar/resultado_final',
        api_apagar='/api/apagar/resultado_final',
        campos_chave=[("ID do Aluno:", "id_aluno"), ("ID da Disciplina:", "id_disciplina")],
        cabecalho=cabecalho,
        dados=registros,
    )


@app.route('/api/cadastrar/aluno', methods=['POST'])
@perfil_requerido('DEV')
def api_cadastrar_aluno():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="""
            INSERT INTO aluno (nome, data_nascimento, endereco, data_matricula)
            VALUES (%s, %s, %s, %s)
        """,
        parametros=(
            request.form.get('nome') or "",
            request.form.get('data_nascimento') or "",
            request.form.get('endereco') or "",
            request.form.get('data_matricula') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Insercao de aluno mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} aluno(s) inserido(s). Volte para /consultar/aluno para ver o resultado."

@app.route('/api/atualizar/aluno', methods=['POST'])
@perfil_requerido('DEV')
def api_atualizar_aluno():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="""
            UPDATE aluno
            SET nome = %s, data_nascimento = %s, endereco = %s, data_matricula = %s
            WHERE id_aluno = %s
        """,
        parametros=(
            request.form.get('nome') or "",
            request.form.get('data_nascimento') or "",
            request.form.get('endereco') or "",
            request.form.get('data_matricula') or "",
            request.form.get('id_aluno') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Atualizacao de aluno mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} aluno(s) atualizado(s). Volte para /consultar/aluno para ver o resultado."

@app.route('/api/apagar/aluno', methods=['POST'])
@perfil_requerido('DEV')
def api_apagar_aluno():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="DELETE FROM aluno WHERE id_aluno = %s",
        parametros=(request.form.get('id_aluno') or "",)
    )
    if qtd < 0:
        return "ERRO: Delete de aluno mal feito. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} aluno(s) apagado(s). Volte para /consultar/aluno para ver o resultado."


@app.route('/api/cadastrar/especialidade_professor', methods=['POST'])
@perfil_requerido('DEV')
def api_cadastrar_especialidade_professor():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="INSERT INTO especialidade_professor (especialidade) VALUES (%s)",
        parametros=(request.form.get('especialidade') or "",)
    )
    if qtd < 0:
        return "ERRO: Insercao de especialidade mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} especialidade(s) inserida(s). Volte para /consultar/especialidade_professor."

@app.route('/api/atualizar/especialidade_professor', methods=['POST'])
@perfil_requerido('DEV')
def api_atualizar_especialidade_professor():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="UPDATE especialidade_professor SET especialidade = %s WHERE id_especialidade = %s",
        parametros=(
            request.form.get('especialidade') or "",
            request.form.get('id_especialidade') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Atualizacao de especialidade mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} especialidade(s) atualizada(s). Volte para /consultar/especialidade_professor."

@app.route('/api/apagar/especialidade_professor', methods=['POST'])
@perfil_requerido('DEV')
def api_apagar_especialidade_professor():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="DELETE FROM especialidade_professor WHERE id_especialidade = %s",
        parametros=(request.form.get('id_especialidade') or "",)
    )
    if qtd < 0:
        return "ERRO: Delete de especialidade mal feito. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} especialidade(s) apagada(s). Volte para /consultar/especialidade_professor."


@app.route('/api/cadastrar/professor', methods=['POST'])
@perfil_requerido('DEV')
def api_cadastrar_professor():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="INSERT INTO professor (nome, id_especialidade) VALUES (%s, %s)",
        parametros=(
            request.form.get('nome') or "",
            request.form.get('id_especialidade') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Insercao de professor mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} professor(es) inserido(s). Volte para /consultar/professor."

@app.route('/api/atualizar/professor', methods=['POST'])
@perfil_requerido('DEV')
def api_atualizar_professor():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="UPDATE professor SET nome = %s, id_especialidade = %s WHERE id_professor = %s",
        parametros=(
            request.form.get('nome') or "",
            request.form.get('id_especialidade') or "",
            request.form.get('id_professor') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Atualizacao de professor mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} professor(es) atualizado(s). Volte para /consultar/professor."

@app.route('/api/apagar/professor', methods=['POST'])
@perfil_requerido('DEV')
def api_apagar_professor():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="DELETE FROM professor WHERE id_professor = %s",
        parametros=(request.form.get('id_professor') or "",)
    )
    if qtd < 0:
        return "ERRO: Delete de professor mal feito. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} professor(es) apagado(s). Volte para /consultar/professor."


@app.route('/api/cadastrar/disciplina', methods=['POST'])
@perfil_requerido('DEV')
def api_cadastrar_disciplina():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="INSERT INTO disciplina (nome, carga_horaria, tipo) VALUES (%s, %s, %s)",
        parametros=(
            request.form.get('nome') or "",
            request.form.get('carga_horaria') or "",
            request.form.get('tipo') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Insercao de disciplina mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} disciplina(s) inserida(s). Volte para /consultar/disciplina."

@app.route('/api/atualizar/disciplina', methods=['POST'])
@perfil_requerido('DEV')
def api_atualizar_disciplina():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="UPDATE disciplina SET nome = %s, carga_horaria = %s, tipo = %s WHERE id_disciplina = %s",
        parametros=(
            request.form.get('nome') or "",
            request.form.get('carga_horaria') or "",
            request.form.get('tipo') or "",
            request.form.get('id_disciplina') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Atualizacao de disciplina mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} disciplina(s) atualizada(s). Volte para /consultar/disciplina."

@app.route('/api/apagar/disciplina', methods=['POST'])
@perfil_requerido('DEV')
def api_apagar_disciplina():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="DELETE FROM disciplina WHERE id_disciplina = %s",
        parametros=(request.form.get('id_disciplina') or "",)
    )
    if qtd < 0:
        return "ERRO: Delete de disciplina mal feito. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} disciplina(s) apagada(s). Volte para /consultar/disciplina."


@app.route('/api/cadastrar/disciplina_professor', methods=['POST'])
@perfil_requerido('DEV')
def api_cadastrar_disciplina_professor():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="INSERT INTO disciplina_professor (id_professor, id_disciplina) VALUES (%s, %s)",
        parametros=(
            request.form.get('id_professor') or "",
            request.form.get('id_disciplina') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Insercao mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} vinculo(s) inserido(s). Volte para /consultar/disciplina_professor."

@app.route('/api/apagar/disciplina_professor', methods=['POST'])
@perfil_requerido('DEV')
def api_apagar_disciplina_professor():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="DELETE FROM disciplina_professor WHERE id_professor = %s AND id_disciplina = %s",
        parametros=(
            request.form.get('id_professor') or "",
            request.form.get('id_disciplina') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Delete mal feito. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} vinculo(s) apagado(s). Volte para /consultar/disciplina_professor."


@app.route('/api/cadastrar/periodo_letivo', methods=['POST'])
@perfil_requerido('DEV')
def api_cadastrar_periodo_letivo():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="INSERT INTO periodo_letivo (descricao, data_inicio, data_fim) VALUES (%s, %s, %s)",
        parametros=(
            request.form.get('descricao') or "",
            request.form.get('data_inicio') or "",
            request.form.get('data_fim') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Insercao de periodo letivo mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} periodo(s) inserido(s). Volte para /consultar/periodo_letivo."

@app.route('/api/atualizar/periodo_letivo', methods=['POST'])
@perfil_requerido('DEV')
def api_atualizar_periodo_letivo():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="UPDATE periodo_letivo SET descricao = %s, data_inicio = %s, data_fim = %s WHERE id_periodo = %s",
        parametros=(
            request.form.get('descricao') or "",
            request.form.get('data_inicio') or "",
            request.form.get('data_fim') or "",
            request.form.get('id_periodo') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Atualizacao de periodo letivo mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} periodo(s) atualizado(s). Volte para /consultar/periodo_letivo."

@app.route('/api/apagar/periodo_letivo', methods=['POST'])
@perfil_requerido('DEV')
def api_apagar_periodo_letivo():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="DELETE FROM periodo_letivo WHERE id_periodo = %s",
        parametros=(request.form.get('id_periodo') or "",)
    )
    if qtd < 0:
        return "ERRO: Delete de periodo letivo mal feito. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} periodo(s) apagado(s). Volte para /consultar/periodo_letivo."


@app.route('/api/cadastrar/periodo_ferias', methods=['POST'])
@perfil_requerido('DEV')
def api_cadastrar_periodo_ferias():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="INSERT INTO periodo_ferias (id_periodo, data_inicio, data_fim) VALUES (%s, %s, %s)",
        parametros=(
            request.form.get('id_periodo') or "",
            request.form.get('data_inicio') or "",
            request.form.get('data_fim') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Insercao de periodo de ferias mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} periodo(s) de ferias inserido(s). Volte para /consultar/periodo_ferias."

@app.route('/api/atualizar/periodo_ferias', methods=['POST'])
@perfil_requerido('DEV')
def api_atualizar_periodo_ferias():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="UPDATE periodo_ferias SET id_periodo = %s, data_inicio = %s, data_fim = %s WHERE id_ferias = %s",
        parametros=(
            request.form.get('id_periodo') or "",
            request.form.get('data_inicio') or "",
            request.form.get('data_fim') or "",
            request.form.get('id_ferias') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Atualizacao de periodo de ferias mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} periodo(s) de ferias atualizado(s). Volte para /consultar/periodo_ferias."

@app.route('/api/apagar/periodo_ferias', methods=['POST'])
@perfil_requerido('DEV')
def api_apagar_periodo_ferias():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="DELETE FROM periodo_ferias WHERE id_ferias = %s",
        parametros=(request.form.get('id_ferias') or "",)
    )
    if qtd < 0:
        return "ERRO: Delete de periodo de ferias mal feito. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} periodo(s) de ferias apagado(s). Volte para /consultar/periodo_ferias."


@app.route('/api/cadastrar/turma', methods=['POST'])
@perfil_requerido('DEV')
def api_cadastrar_turma():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="INSERT INTO turma (nome, id_periodo) VALUES (%s, %s)",
        parametros=(
            request.form.get('nome') or "",
            request.form.get('id_periodo') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Insercao de turma mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} turma(s) inserida(s). Volte para /consultar/turma."

@app.route('/api/atualizar/turma', methods=['POST'])
@perfil_requerido('DEV')
def api_atualizar_turma():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="UPDATE turma SET nome = %s, id_periodo = %s WHERE id_turma = %s",
        parametros=(
            request.form.get('nome') or "",
            request.form.get('id_periodo') or "",
            request.form.get('id_turma') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Atualizacao de turma mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} turma(s) atualizada(s). Volte para /consultar/turma."

@app.route('/api/apagar/turma', methods=['POST'])
@perfil_requerido('DEV')
def api_apagar_turma():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="DELETE FROM turma WHERE id_turma = %s",
        parametros=(request.form.get('id_turma') or "",)
    )
    if qtd < 0:
        return "ERRO: Delete de turma mal feito. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} turma(s) apagada(s). Volte para /consultar/turma."


@app.route('/api/cadastrar/turma_disciplina', methods=['POST'])
@perfil_requerido('DEV')
def api_cadastrar_turma_disciplina():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="""
            INSERT INTO turma_disciplina (id_turma, id_disciplina, id_professor)
            VALUES (%s, %s, %s)
        """,
        parametros=(
            request.form.get('id_turma') or "",
            request.form.get('id_disciplina') or "",
            request.form.get('id_professor') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Insercao mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} vinculo(s) inserido(s). Volte para /consultar/turma_disciplina."

@app.route('/api/apagar/turma_disciplina', methods=['POST'])
@perfil_requerido('DEV')
def api_apagar_turma_disciplina():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="""
            DELETE FROM turma_disciplina
            WHERE id_turma = %s AND id_disciplina = %s AND id_professor = %s
        """,
        parametros=(
            request.form.get('id_turma') or "",
            request.form.get('id_disciplina') or "",
            request.form.get('id_professor') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Delete mal feito. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} vinculo(s) apagado(s). Volte para /consultar/turma_disciplina."


@app.route('/api/cadastrar/matricula_disciplina', methods=['POST'])
@perfil_requerido('DEV')
def api_cadastrar_matricula_disciplina():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="""
            INSERT INTO matricula_disciplina (id_aluno, id_disciplina, id_turma)
            VALUES (%s, %s, %s)
        """,
        parametros=(
            request.form.get('id_aluno') or "",
            request.form.get('id_disciplina') or "",
            request.form.get('id_turma') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Insercao mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} matricula(s) inserida(s). Volte para /consultar/matricula_disciplina."

@app.route('/api/apagar/matricula_disciplina', methods=['POST'])
@perfil_requerido('DEV')
def api_apagar_matricula_disciplina():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="""
            DELETE FROM matricula_disciplina
            WHERE id_aluno = %s AND id_disciplina = %s AND id_turma = %s
        """,
        parametros=(
            request.form.get('id_aluno') or "",
            request.form.get('id_disciplina') or "",
            request.form.get('id_turma') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Delete mal feito. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} matricula(s) apagada(s). Volte para /consultar/matricula_disciplina."


@app.route('/api/cadastrar/avaliacao', methods=['POST'])
@login_required
def api_cadastrar_avaliacao():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="""
            INSERT INTO avaliacao (observacao, numero_avaliacao, nota, data_avaliacao, id_aluno, id_disciplina)
            VALUES (%s, %s, %s, %s, %s, %s)
        """,
        parametros=(
            request.form.get('observacao') or "",
            request.form.get('numero_avaliacao') or "",
            request.form.get('nota') or "",
            request.form.get('data_avaliacao') or "",
            request.form.get('id_aluno') or "",
            request.form.get('id_disciplina') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Insercao de avaliacao mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} avaliacao(oes) inserida(s). Volte para /consultar/avaliacao."

@app.route('/api/atualizar/avaliacao', methods=['POST'])
@login_required
def api_atualizar_avaliacao():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="""
            UPDATE avaliacao
            SET observacao = %s, numero_avaliacao = %s, nota = %s, data_avaliacao = %s,
                id_aluno = %s, id_disciplina = %s
            WHERE id_boletim = %s
        """,
        parametros=(
            request.form.get('observacao') or "",
            request.form.get('numero_avaliacao') or "",
            request.form.get('nota') or "",
            request.form.get('data_avaliacao') or "",
            request.form.get('id_aluno') or "",
            request.form.get('id_disciplina') or "",
            request.form.get('id_boletim') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Atualizacao de avaliacao mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} avaliacao(oes) atualizada(s). Volte para /consultar/avaliacao."

@app.route('/api/apagar/avaliacao', methods=['POST'])
@login_required
def api_apagar_avaliacao():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="DELETE FROM avaliacao WHERE id_boletim = %s",
        parametros=(request.form.get('id_boletim') or "",)
    )
    if qtd < 0:
        return "ERRO: Delete de avaliacao mal feito. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} avaliacao(oes) apagada(s). Volte para /consultar/avaliacao."


@app.route('/api/cadastrar/registro_frequencia', methods=['POST'])
@login_required
def api_cadastrar_registro_frequencia():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="""
            INSERT INTO registro_frequencia (id_aluno, id_disciplina, data_aula, status_presenca)
            VALUES (%s, %s, %s, %s)
        """,
        parametros=(
            request.form.get('id_aluno') or "",
            request.form.get('id_disciplina') or "",
            request.form.get('data_aula') or "",
            request.form.get('status_presenca') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Insercao de frequencia mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} registro(s) inserido(s). Volte para /consultar/registro_frequencia."

@app.route('/api/atualizar/registro_frequencia', methods=['POST'])
@login_required
def api_atualizar_registro_frequencia():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="""
            UPDATE registro_frequencia
            SET id_aluno = %s, id_disciplina = %s, data_aula = %s, status_presenca = %s
            WHERE id_frequencia = %s
        """,
        parametros=(
            request.form.get('id_aluno') or "",
            request.form.get('id_disciplina') or "",
            request.form.get('data_aula') or "",
            request.form.get('status_presenca') or "",
            request.form.get('id_frequencia') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Atualizacao de frequencia mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} registro(s) atualizado(s). Volte para /consultar/registro_frequencia."

@app.route('/api/apagar/registro_frequencia', methods=['POST'])
@login_required
def api_apagar_registro_frequencia():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="DELETE FROM registro_frequencia WHERE id_frequencia = %s",
        parametros=(request.form.get('id_frequencia') or "",)
    )
    if qtd < 0:
        return "ERRO: Delete de frequencia mal feito. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} registro(s) apagado(s). Volte para /consultar/registro_frequencia."


@app.route('/api/cadastrar/resultado_final', methods=['POST'])
@login_required
def api_cadastrar_resultado_final():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="""
            INSERT INTO resultado_final (id_aluno, id_disciplina, situacao, frequencia)
            VALUES (%s, %s, %s, %s)
        """,
        parametros=(
            request.form.get('id_aluno') or "",
            request.form.get('id_disciplina') or "",
            request.form.get('situacao') or "",
            request.form.get('frequencia') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Insercao de resultado final mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} resultado(s) inserido(s). Volte para /consultar/resultado_final."

@app.route('/api/atualizar/resultado_final', methods=['POST'])
@login_required
def api_atualizar_resultado_final():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="""
            UPDATE resultado_final
            SET situacao = %s, frequencia = %s
            WHERE id_aluno = %s AND id_disciplina = %s
        """,
        parametros=(
            request.form.get('situacao') or "",
            request.form.get('frequencia') or "",
            request.form.get('id_aluno') or "",
            request.form.get('id_disciplina') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Atualizacao de resultado final mal feita. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} resultado(s) atualizado(s). Volte para /consultar/resultado_final."

@app.route('/api/apagar/resultado_final', methods=['POST'])
@login_required
def api_apagar_resultado_final():
    qtd = executar_insert_delete_update(
        db=NOME_BANCO,
        consulta_sql="DELETE FROM resultado_final WHERE id_aluno = %s AND id_disciplina = %s",
        parametros=(
            request.form.get('id_aluno') or "",
            request.form.get('id_disciplina') or "",
        )
    )
    if qtd < 0:
        return "ERRO: Delete de resultado final mal feito. Veja os logs do Python para detalhes."
    return f"SUCESSO: {qtd} resultado(s) apagado(s). Volte para /consultar/resultado_final."


if __name__ == '__main__':
    while True:
        try:
            print("Iniciando servidor Flask...")
            print("Pressione Ctrl+C para encerrar o servidor.")
            app.run(debug=True)
            raise KeyboardInterrupt()
        except KeyboardInterrupt:
            print("Servidor Flask encerrado pelo usuário.")
            break
        except Exception as e:
            print(f"Erro no servidor Flask: {e}")
            time.sleep(0.500)
