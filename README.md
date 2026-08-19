
## Instalar dependencias

No terminal execute o seguinte comando:

```batch
python -m pip install -r requirements.txt
```

## Executar app Flask

No terminal execute o seguinte comando:

```batch
python.exe app.py
```

## O que fazer

1) Importar o arquivo **db/sistema_escolar_modelo_fisico.sql** no PhpMyAdmin ( http://localhost/phpmyadmin )
2) Instalar dependências do Flask (veja comando acima)
3) Executar o App Flask (veja o comando acima)
4) Acessar o App no endereço http://localhost:5000

## Estrutura do projeto

- **app.py**: Aplicativo Python que usa a biblioteca Flask para criar o site. Contem as telas (rotas GET)
  e as APIs (rotas POST) de cadastro, atualizacao e remocao para as 13 tabelas do sistema escolar.
- **db/**: contem o arquivo .SQL do banco de dados (sistema_escolar_modelo_fisico.sql) e a biblioteca
  db.py para acesso ao MySQL/MariaDB a partir do Python.
- **static/**: contem os arquivos .CSS, .JS e icones do site (Bootstrap).
- **templates/**: contem os templates HTML que o Python preenche (arquivos .JINJA2)
  - **_base.jinja2**: Template base do site, com o menu de navegacao (Consultar / Cadastrar)
  - **_macros.jinja2**: Funcoes reutilizaveis para montar inputs, selects e tabelas HTML
  - **index.jinja2**: Pagina inicial
  - **consultar.jinja2**: Template generico de consulta, reutilizado por todas as 13 tabelas
  - **cadastrar/**: paginas de cadastro (INSERT), uma por tabela
  - **atualizar/**: paginas de atualizacao (UPDATE), para as tabelas que tem campos alem da chave

## Tabelas cobertas (13 no total)

Aluno, Professor, Especialidade do Professor, Disciplina, Disciplina x Professor, Periodo Letivo,
Periodo de Ferias, Turma, Turma x Disciplina, Matricula em Disciplina, Avaliacao,
Registro de Frequencia, Resultado Final.

> As tabelas de vinculo N:N com chave composta e sem colunas proprias
> (Disciplina x Professor, Turma x Disciplina, Matricula em Disciplina) tem apenas
> Cadastrar/Consultar/Apagar — nao existe "atualizar" um vinculo, apenas apagar e recriar.
