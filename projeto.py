from conector import Conector
from datetime import date


class Projeto:
    def __init__(self, idprojeto=None, nome=None, descricao=None, datainicio=None, datafim=None, situacao=None, idresponsavel=None):
        self.idprojeto = idprojeto
        self.nome = nome
        self.descricao = descricao
        self.datainicio = datainicio
        self.datafim = datafim
        self.situacao = situacao
        self.idresponsavel = idresponsavel

    def inserir(self):
        con = Conector()
        con.conectar()
        sql = """
        INSERT INTO projetos (nmprojeto, descricao, datainicio, datafim, situacao, idresponsavel)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (self.nome, self.descricao, self.datainicio, self.datafim, self.situacao, self.idresponsavel)
        con.executar(sql, params)
        con.fechar()

    @staticmethod
    def listar():
        con = Conector()
        con.conectar()
        sql = "SELECT idprojeto, nmprojeto, situacao, idresponsavel FROM projetos"
        resultados = con.consultar(sql)
        con.fechar()
        return resultados

    def atualizar(self):
        con = Conector()
        con.conectar()
        sql = """
        UPDATE projetos
        SET nmprojeto = %s, descricao = %s, datainicio = %s, datafim = %s, situacao = %s, idresponsavel = %s
        WHERE idprojeto = %s
        """
        params = (self.nome, self.descricao, self.datainicio, self.datafim, self.situacao, self.idresponsavel, self.idprojeto)
        con.executar(sql, params)
        con.fechar()

    def deletar(self):
        con = Conector()
        con.conectar()
        sql = "DELETE FROM projetos WHERE idprojeto = %s"
        con.executar(sql, (self.idprojeto,))
        con.fechar()

    @staticmethod
    def existe_projeto(nome, datainicio):
        con = Conector()
        con.conectar()
        sql = """
            SELECT COUNT(*) FROM projetos
            WHERE LOWER(nmprojeto) = LOWER(%s) AND datainicio = %s
        """
        resultado = con.consultar(sql, (nome, datainicio))
        con.fechar()
        return resultado[0][0] >= 1 
    
    @staticmethod
    def existe_nome(nome):
        con = Conector()
        con.conectar()
        sql = "SELECT COUNT(*) FROM projetos WHERE LOWER(nmprojeto) = LOWER(%s)"
        resultado = con.consultar(sql, (nome,))
        con.fechar()
        return resultado[0][0] >= 1
    
    def listarCompleto():
        con = Conector()
        con.conectar()
        sql = "SELECT idprojeto, nmprojeto, situacao, idresponsavel FROM projetos"
        resultados = con.consultar(sql)
        con.fechar()
        return resultados

    def atualizar_situacao(self):
        if self.situacao != "Ativo":
            print("Erro: Apenas projetos com situação 'Ativo' podem ser encerrados.")
            return
        self.situacao = "Encerrado"
        self.datafim = date.today().strftime("%Y-%m-%d")  # Pega a data de hoje no formato YYYY-MM-DD
        con = Conector()
        con.conectar()
        sql = "UPDATE projetos SET situacao = %s, datafim = %s WHERE idprojeto = %s"
        params = (self.situacao, self.datafim, self.idprojeto)
        con.executar(sql, params)
        con.fechar()
        print("Situação do projeto atualizada para 'Encerrado'.")

    def atualizar_situacao_suspensa(self):
        print(self.situacao)
        # Verifica se o projeto está "Ativo"
        if self.situacao != 'Ativo':
            print("Erro: O projeto precisa estar 'Ativo' para ser colocado em 'Suspenso'.")
            return

        # Caso a situação seja "Ativo", muda para "Suspenso"
        con = Conector()
        con.conectar()
        sql = "UPDATE projetos SET situacao = %s WHERE idprojeto = %s"
        params = ('Suspenso', self.idprojeto)
        con.executar(sql, params)
        con.fechar()
        print(f"Projeto {self.idprojeto} agora está 'Suspenso'.")
    
    def atualizar_situacao_reativar(self):
        # Verifica se o projeto está "Suspenso"
        if self.situacao != 'Suspenso':
            print("Erro: O projeto precisa estar 'Suspenso' para ser reativado.")
            return

        # Caso a situação seja "Suspenso", muda para "Ativo"
        con = Conector()
        con.conectar()
        sql = "UPDATE projetos SET situacao = %s WHERE idprojeto = %s"
        params = ('Ativo', self.idprojeto)
        con.executar(sql, params)
        con.fechar()
        print(f"Projeto {self.idprojeto} agora está 'Ativo'.")

    def criar_por_id(idprojeto):
        # Conectar ao banco de dados
        con = Conector()
        con.conectar()

        # Buscar os dados do projeto pelo ID
        sql = "SELECT idprojeto, nmprojeto, descricao, datainicio, datafim, situacao, idresponsavel FROM projetos WHERE idprojeto = %s"
        resultado = con.consultar(sql, (idprojeto,))
        con.fechar()

        # Verificar se o projeto foi encontrado
        if not resultado:
            print(f"Projeto com ID {idprojeto} não encontrado.")
            return None

        # Extrair os dados do projeto
        idprojeto, nome, descricao, datainicio, datafim, situacao, idresponsavel = resultado[0]

        # Criar e retornar o objeto Projeto
        return Projeto(idprojeto=idprojeto, nome=nome, descricao=descricao, datainicio=datainicio, datafim=datafim, situacao=situacao, idresponsavel=idresponsavel)