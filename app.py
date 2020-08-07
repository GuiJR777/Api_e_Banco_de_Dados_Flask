from flask import Flask, request
from flask_restful import Api, Resource
from models import Pessoas, Atividades, Usuarios
from flask_httpauth import HTTPBasicAuth
import json

auth= HTTPBasicAuth()
app= Flask(__name__)
api= Api(app)

""" USUARIOS= {
    'guilherme':'123',
    'rafael':'321'
}

@auth.verify_password
def verificacao(login, senha):
    if not (login, senha):
        return False
    return USUARIOS.get(login) == senha """

@auth.verify_password
def verificacao(login, senha):
    if not (login, senha):
        return False
    return Usuarios.query.filter_by(login=login, senha=senha).first() 

class Pessoa(Resource):
    # Procura pessoas no Banco de Dados pelo Nome
    @auth.login_required
    def get(self, nome):
        try:
            pessoa= Pessoas.query.filter_by(nome=nome).first()
            response= {
                'id':pessoa.id,
                'nome':pessoa.nome,
                'idade':pessoa.idade
            }
        except AttributeError:
            mensagem= 'A pessoa com o nome {} não foi encontrada'.format(nome)
            response= {'status':'Erro','mensagem':mensagem}
        return response

    # Altera pessoas no banco de dados pelo nome
    def put(self, nome):
        pessoa= Pessoas.query.filter_by(nome=nome).first()
        dados= json.loads(request.data)
        if 'nome' in dados:
            pessoa.nome = dados['nome']

        if 'idade' in dados:
            pessoa.idade = dados['idade']
        pessoa.save()
        response= {
                'id':pessoa.id,
                'nome':pessoa.nome,
                'idade':pessoa.idade
            }
        return response

    # Deleta pessoa pelo nome
    def delete(self, nome):
        pessoa= Pessoas.query.filter_by(nome=nome).first()
        pessoa.delete()
        mensagem= 'A pessoa com o nome {} foi deletada do Banco de Dados'.format(nome)
        response= {'status':'Sucesso','mensagem':mensagem}
        return response

class ListaPessoas(Resource):
    # Retorna todas as pessoas
    def get(self):
        pessoas= Pessoas.query.all()
        response= [{'id':p.id, 'nome':p.nome, 'idade':p.idade} for p in pessoas]
        return response

    # Cria novas pessoas
    def post(self):
        dados= json.loads(request.data)
        pessoa= Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        mensagem= 'A pessoa com o nome {} foi adicionada ao Banco de Dados'.format(pessoa.nome)
        response= {'status':'Sucesso','mensagem':mensagem}
        return response



class ListaAtividades(Resource):
    # Lista todas as atividades
    def get(self):
        atividades= Atividades.query.all()
        response= [{'id':i.id, 'nome':i.nome, 'pessoa':i.pessoa.nome} for i in atividades]
        return response

    # Cria novas atividades
    def post(self):
        dados= json.loads(request.data)
        pessoa= Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade= Atividades(nome=dados['nome'], pessoa=pessoa)
        atividade.save()
        mensagem= 'A atividade {} foi atribuida a pessoa {}'.format(atividade.nome, atividade.pessoa.nome)
        response= {'status':'Sucesso','mensagem':mensagem}
        return response



api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(ListaAtividades, '/atividades/')

if __name__==('__main__'):
    app.run(debug=True)