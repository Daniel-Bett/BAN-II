from conector import Conector

class ProjetoRelacionado:
    def __init__(self, idprojeto=None, idprojetorelacionado=None):
        self.idprojeto = idprojeto
        self.idprojetorelacionado = idprojetorelacionado

    def inserir(self):
        if not self.idprojeto or not self.idprojetorelacionado:
            print("IDs de projeto e projeto relacionado são obrigatórios para inserção.")
            return

        con = Conector()
        con.conectar()
        sql = """
            INSERT INTO projetosrelacionamentos (idprojeto, idprojetorelacionado)
            VALUES (%s, %s)
        """
        params = (self.idprojeto, self.idprojetorelacionado)
        con.executar(sql, params)
        con.fechar()

    @staticmethod
    def listar():
        con = Conector()
        con.conectar()
        sql = """
            SELECT idrelacionamento, idprojeto, idprojetorelacionado
            FROM projetosrelacionamentos
            ORDER BY idprojeto, idprojetorelacionado
        """
        resultados = con.consultar(sql)
        con.fechar()
        return resultados

    def deletar(self, idrelacionamento):
        if not idrelacionamento:
            print("ID do relacionamento é obrigatório para exclusão.")
            return

        con = Conector()
        con.conectar()
        sql = """
            DELETE FROM projetosrelacionamentos
            WHERE idrelacionamento = %s
        """
        con.executar(sql, (idrelacionamento,))
        con.fechar()
