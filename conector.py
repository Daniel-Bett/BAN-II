import psycopg2
from config import DB_CONFIG

class Conector:
    def __init__(self):
        self.conn = None
        self.cur = None

    def conectar(self):
        try:
            # Conecta ao banco usando as credenciais do config.py
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cur = self.conn.cursor()
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def executar(self, sql, params=None):
        try:
            # Executa comandos SQL que não retornam dados (INSERT, UPDATE, DELETE)
            self.cur.execute(sql, params or ())
            self.conn.commit()
        except Exception as e:
            print(f"Erro ao executar comando SQL: {e}")

    def consultar(self, sql, params=None):
        try:
            # Executa SELECT e retorna os resultados
            self.cur.execute(sql, params or ())
            return self.cur.fetchall()
        except Exception as e:
            print(f"Erro ao consultar dados: {e}")
            return []

    def fechar(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
