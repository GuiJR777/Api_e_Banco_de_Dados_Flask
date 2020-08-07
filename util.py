from models import Pessoas

# Insere dados na tabela Pessoa(INSERT)
def insere_pessoas():
    pessoa= Pessoas (nome= 'Felipe', idade=25)
    print(pessoa)
    pessoa.save()

# Consulta dados na tabela Pessoas(SELECT)
def consulta_pessoa():
    pessoa= Pessoas.query.all()
    # pessoa= Pessoas.query.filter_by(nome='Guilherme')
    for p in pessoa:
        print(p.nome, p.idade)

# Altera dados na tabela Pessoas(UPDATE)
def altera_pessoa():
    pessoa= Pessoas.query.filter_by(nome='Rafael').first()
    pessoa.idade= 21
    pessoa.save()

# Deleta dados da tabela Pessoas(DELETE)
def exclui_pessoa():
    pessoa= Pessoas.query.filter_by(nome='Felipe').first()
    pessoa.delete()


# Executor
if __name__== '__main__':
    # insere_pessoas()
    # consulta_pessoa()
    # altera_pessoa()
    # exclui_pessoa()