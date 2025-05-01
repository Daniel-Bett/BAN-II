from conector import Conector
from datetime import date

class Atividade:
    def __init__(self, idatividade=None, nmatividade=None, descricao=None, datainicio=None, datafim=None, situacao=None, idprojeto=None, idresponsavel=None):
        self.idatividade = idatividade
        self.nmatividade = nmatividade
        self.descricao = descricao
        self.datainicio = datainicio
        self.datafim = datafim
        self.situacao = situacao
        self.idprojeto = idprojeto
        self.idresponsavel = idresponsavel

    def inserir(self):
        con = Conector()
        con.conectar()
        sql = """
        INSERT INTO atividades (nmatividade, descricao, datainicio, datafim, situacao, idprojeto, idresponsavel)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (self.nmatividade, self.descricao, self.datainicio, self.datafim, self.situacao, self.idprojeto, self.idresponsavel)
        con.executar(sql, params)
        con.fechar()

    @staticmethod
    def listar():
        con = Conector()
        con.conectar()
        sql = "SELECT idatividade, nmatividade, descricao, datainicio, datafim, situacao, idprojeto, idresponsavel FROM atividades"
        resultados = con.consultar(sql)
        con.fechar()
        return resultados

    def atualizar(self):
        con = Conector()
        con.conectar()
        sql = """
        UPDATE atividades
        SET nmatividade = %s, descricao = %s, datainicio = %s, datafim = %s, situacao = %s, idprojeto = %s, idresponsavel = %s
        WHERE idatividade = %s
        """
        params = (self.nmatividade, self.descricao, self.datainicio, self.datafim, self.situacao, self.idprojeto, self.idresponsavel, self.idatividade)
        con.executar(sql, params)
        con.fechar()

    def deletar(self):
        con = Conector()
        con.conectar()
        sql = "DELETE FROM atividades WHERE idatividade = %s"
        con.executar(sql, (self.idatividade,))
        con.fechar()

    def atualizar_situacao(self):
        con = Conector()
        con.conectar()
        sql_select = "SELECT situacao FROM atividades WHERE idatividade = %s"
        resultado = con.consultar(sql_select, (self.idatividade,))

        if not resultado:
            print("Atividade não encontrada.")
            con.fechar()
            return
        situacao_atual = resultado[0][0]
        if situacao_atual == "Encerrado":
            print("Erro: A atividade já está encerrada e não pode ser executada novamente.")
        elif situacao_atual == "Pendente":
            nova_situacao = "Em Andamento"
            sql_update = "UPDATE atividades SET situacao = %s WHERE idatividade = %s"
            con.executar(sql_update, (nova_situacao, self.idatividade))
            print("Situação atualizada para Em Andamento.")
        elif situacao_atual == "Em Andamento":
            nova_situacao = "Encerrado"
            datafim = date.today().strftime("%Y-%m-%d")
            sql_update = "UPDATE atividades SET situacao = %s, datafim = %s WHERE idatividade = %s"
            con.executar(sql_update, (nova_situacao,datafim, self.idatividade))
            print("Situação atualizada para Encerrado.")
        else:
            print(f"Erro: Situação desconhecida '{situacao_atual}'.")
        con.fechar()