from conector import Conector

class Departamento:
    def __init__(self, iddepartamento=None, nmdepartamento=None):
        self.iddepartamento = iddepartamento
        self.nmdepartamento = nmdepartamento

    def inserir(self):
        con = Conector()
        con.conectar()

        # Verificar se o nome já existe
        
        sql_verifica = "SELECT COUNT(*) FROM departamentos WHERE LOWER(nmdepartamento) = LOWER(%s)"
        existe = con.consultar(sql_verifica, (self.nmdepartamento,))
        if existe[0][0] > 0:
            print("Já existe um departamento com esse nome. Operação cancelada.")
        else:
            sql = "INSERT INTO departamentos (nmdepartamento) VALUES (%s)"
            params = (self.nmdepartamento,)
            con.executar(sql, params)
            print("Departamento inserido com sucesso!")

        con.fechar()

    @staticmethod
    def listar():
        con = Conector()
        con.conectar()
        sql = "SELECT iddepartamento, nmdepartamento FROM departamentos"
        resultados = con.consultar(sql)
        con.fechar()
        return resultados

    def atualizar(self):
        con = Conector()
        con.conectar()
        sql = "UPDATE departamentos SET nmdepartamento = %s WHERE iddepartamento = %s"
        params = (self.nmdepartamento, self.iddepartamento)
        con.executar(sql, params)
        con.fechar()

    def deletar(self):
        con = Conector()
        con.conectar()
        sql = "DELETE FROM departamentos WHERE iddepartamento = %s"
        con.executar(sql, (self.iddepartamento,))
        con.fechar()
