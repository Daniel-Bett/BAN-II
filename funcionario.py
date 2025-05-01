from conector import Conector

class Funcionario:
    def __init__(self, idfuncionario=None, nmfuncionario=None, iddepartamento=None):
        self.idfuncionario = idfuncionario
        self.nmfuncionario = nmfuncionario
        self.iddepartamento = iddepartamento

    def inserir(self):
        con = Conector()
        con.conectar()
        sql = """
        INSERT INTO funcionarios (nmfuncionario, iddepartamento) 
        VALUES (%s, %s)
        """
        params = (self.nmfuncionario, self.iddepartamento)
        con.executar(sql, params)
        con.fechar()

    @staticmethod
    def listar():
        con = Conector()
        con.conectar()
        sql = "SELECT idfuncionario, nmfuncionario, iddepartamento FROM funcionarios"
        resultados = con.consultar(sql)
        con.fechar()
        return resultados

    def atualizar(self):
        con = Conector()
        con.conectar()
        sql = """
        UPDATE funcionarios
        SET nmfuncionario = %s, iddepartamento = %s
        WHERE idfuncionario = %s
        """
        params = (self.nmfuncionario, self.iddepartamento, self.idfuncionario)
        con.executar(sql, params)
        con.fechar()

    def deletar(self):
        con = Conector()
        con.conectar()
        sql = "DELETE FROM funcionarios WHERE idfuncionario = %s"
        con.executar(sql, (self.idfuncionario,))
        con.fechar()

    def transferir(self, novo_iddepartamento):
        # Criar uma conexão com o banco de dados
        con = Conector()
        con.conectar()
        
        # Definir o SQL de atualização
        sql = """
        UPDATE funcionarios
        SET iddepartamento = %s
        WHERE idfuncionario = %s
        """
    
        # Passar os parâmetros necessários para a consulta
        params = (novo_iddepartamento, self.idfuncionario)
        
        # Executar o comando SQL
        con.executar(sql, params)
        
        # Fechar a conexão com o banco de dados
        con.fechar()
        
        print("Funcionário transferido com sucesso!")


