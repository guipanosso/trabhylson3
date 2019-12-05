import os
from peewee import *
import json
from playhouse.shortcuts import model_to_dict

arq = "festival.db"
db = SqliteDatabase(arq)

class BaseModel(Model):
    class Meta:
        database = db

class Patrocinador(BaseModel):
    nome = CharField()
    cnpj = CharField()
    tipo_patrocinio = CharField()

class Local(BaseModel):
    cep = CharField()
    rua = CharField()
    numero = IntegerField()
    bairro = CharField()
    cidade = CharField()
    pais = CharField()

class Genero(BaseModel):
    nome = CharField()
    descricao = CharField()

class Premiacao(BaseModel):
    nome = CharField()
    descricao = CharField()
    ano = IntegerField()
    tipo= CharField()

class Cantor_banda(BaseModel):
    nome = CharField()
    genero = ManyToManyField(Genero)
    premiacao = ManyToManyField(Premiacao)

class Musica(BaseModel):
    nome = CharField()
    artistas = ManyToManyField(Cantor_banda)
    compositor = CharField()
    duracao = FloatField()
    ano = IntegerField()
    genero = ManyToManyField(Genero)

class Repertorio(BaseModel):
    musicas = ManyToManyField(Musica)
    duracao_show = FloatField()

class Organizador(BaseModel):
    nome = CharField()
    tipo = CharField()
    cpf_ou_cnpj= CharField()

class Promocao(BaseModel):
    valor = FloatField()
    descricao = CharField()

class Ingresso(BaseModel):
    preco = FloatField()
    desconto = ForeignKeyField(Promocao)

class Programacao(BaseModel):
   data = DateField()    
   horario = CharField()
   palco = CharField()

#if __name__ == "__main__":
arq = "festival.db"
if os.path.exists(arq):
    os.remove(arq)
db.connect()
db.create_tables([Patrocinador,Local, Genero, Premiacao, Cantor_banda, Cantor_banda.genero.get_through_model(), Cantor_banda.premiacao.get_through_model(), Musica, Musica.genero.get_through_model(), Musica.artistas.get_through_model(), Repertorio, Repertorio.musicas.get_through_model(), Organizador, Promocao, Ingresso, Programacao])

bradesco = Patrocinador.create(nome= "Bradesco", cnpj= "42.274.696/0025-61", tipo_patrocinio= "Com dinheiro e propaganda.")
patrocinadorlist = list(map(model_to_dict, Patrocinador.select()))
endereço = Local.create(cep= "04801-010", rua= "Av. Sen. Teotônio Vilela", numero= "261", bairro= "Interlagos", cidade= "São Paulo", pais= "Brasil")
locallist = list(map(model_to_dict, Local.select()))
mpb = Genero.create(nome= "MPB", descricao= "Gênero musical surgido no Brasil em meados da década de 1960.")
grammy_latino = Premiacao.create(nome= "Grammy Latino", descricao= "É uma premiação de música latina, criada em 2000.", ano= 2019, tipo= "Melhor Álbum")
guilherme = Organizador.create(nome= "Guilherme Panosso", tipo= "Pessoa física.", cpf_ou_cnpj= "123.456.789.01")
organizadorlist = list(map(model_to_dict, Organizador.select()))
programacao1 = Programacao.create(data= "2019-10-10", horario= "16:00", palco= "Palco Sunset.")
programacaolist = list(map(model_to_dict, Programacao.select()))
promocao1 = Promocao.create(valor= 40.0, descricao= "Promoção para quem tem cartão do Bando Bradesco.")
promocaolist = list(map(model_to_dict, Promocao.select()))
ingresso1 = Ingresso.create(preco= 400.0, desconto= promocao1)
ingressolist = list(map(model_to_dict, Ingresso.select()))
bem_melhor = Musica.create(nome= "Bem melhor", compositor= "Pedro Calais", duracao= 3.03, ano= 2018)
repertorio1 = Repertorio.create(duracao_show= 44.30)
lagum = Cantor_banda.create(nome= "Lagum", repertorio= repertorio1)


repertoriolist = list(map(model_to_dict, Repertorio.select()))
bem_melhor.genero.add(mpb)
lagum.genero.add(mpb)
lagum.premiacao.add(grammy_latino)
premiacaolist = list(map(model_to_dict, Premiacao.select()))
repertorio1.musicas.add(bem_melhor)
musicalist = list(map(model_to_dict, Musica.select()))
bem_melhor.artistas.add(lagum)
generolist= list(map(model_to_dict, Genero.select()))
cantor_bandalist = list(map(model_to_dict, Cantor_banda.select()))


def lista():
    festival = [patrocinadorlist, locallist, generolist, premiacaolist, organizadorlist, programacaolist, promocaolist, ingressolist, musicalist, repertoriolist, cantor_bandalist]
    return festival