from datetime import datetime
from departamento import Departamento
from funcionario import Funcionario
from projetorelacionado import ProjetoRelacionado
from atividade import Atividade
from projeto import Projeto  
from conector import Conector

def menu():
    print("==== Menu de Opções ====")
    print("1 - CRUD")
    print("2 - Operações do Sistema")
    print("3 - Relatórios")
    print("0 - Sair")
    return input("Escolha uma opção: ")



def incluir():
    print("\nEscolha uma tabela para incluir:")
    print("1 - Departamento")
    print("2 - Funcionário")
    print("3 - Atividade")
    print("4 - Projeto Relacionado")
    print("5 - Projeto") 
    opcao = input("Escolha a opção: ")
    
    if opcao == '1':
        op=input("Deseja visualizar os registros existentes? 1-Sim 2-Nao").strip()
        if(op=='1'):
            departamentos = Departamento.listar()
            for dep in departamentos:
                print(dep)
        nome = input("Digite o nome do novo departamento: ")
        departamento = Departamento(nmdepartamento=nome)
        departamento.inserir()
    elif opcao == '2':
        nome = input("Digite o nome do novo funcionário: ").strip()
        if not nome:
            print("Erro: O nome do funcionário não pode estar vazio.")
        else:
            op = input("Deseja visualizar os departamentos existentes? 1-Sim 2-Nao: ").strip()
            if op == '1':
                departamentos = Departamento.listar()
                for dep in departamentos:
                    print(dep)
        iddepartamento = input("Digite o ID do departamento: ")
        departamentos_existentes = Departamento.listar()
        ids_validos = [str(dep[0]) for dep in departamentos_existentes]
        if iddepartamento not in ids_validos:
            print("Erro: ID de departamento inválido. Nenhum funcionário foi cadastrado.")
        else:
            funcionario = Funcionario(nmfuncionario=nome, iddepartamento=iddepartamento)
            funcionario.inserir()
            print("Funcionário incluído com sucesso!")
    elif opcao == '3':
        nome = input("Digite o nome da atividade: ").strip()
        descricao = input("Digite a descrição da atividade: ").strip()
        while True:
            datainicio = input("Digite a data de início (AAAA-MM-DD): ").strip()
            try:
                datetime.strptime(datainicio, "%Y-%m-%d")
                break
            except ValueError:
                print("Formato de data inválido. Use o formato AAAA-MM-DD.")
        datafim = None
        situacao = 'Pendente'
        op = input("Deseja visualizar os projetos existentes? 1-Sim 2-Nao: ").strip()
        if op == '1':
            project = Projeto.listar()
            for proj in project:
                print(proj)
        idprojeto = input("Digite o ID do projeto: ").strip()
        op = input("Deseja visualizar os funcionários existentes? 1-Sim 2-Nao: ").strip()
        if op == '1':
            funcionario = Funcionario.listar()
            for fun in funcionario:
                print(fun)
        idresponsavel = input("Digite o ID do responsável: ").strip()
        atividades_existentes = Atividade.listar()
        atividade_ja_existe = any(
            a[1].strip().lower() == nome.lower() and
            str(a[3]) == datainicio and
            str(a[6]) == idprojeto
            for a in atividades_existentes
        )
        if atividade_ja_existe:
            print("Já existe uma atividade com esse nome, data e projeto.")
        else:
            atividade = Atividade(
                nmatividade=nome,
                descricao=descricao,
                datainicio=datainicio,
                datafim=datafim,
                situacao=situacao,
                idprojeto=idprojeto,
                idresponsavel=idresponsavel
            )
            atividade.inserir()
            print("Atividade incluída com sucesso!")
    elif opcao == '4':
        op = input("Deseja visualizar os projetos existentes? 1-Sim 2-Nao: ").strip()
        if op == '1':
            projetos = Projeto.listar()
            for proj in projetos:
                print(proj)
        
        idprojeto = input("Digite o ID do projeto principal: ").strip()
        idprojetorelacionado = input("Digite o ID do projeto a ser relacionado: ").strip()
        
        projetos_dados = Projeto.listar()
        projetos_ids = [str(p[0]) for p in projetos_dados]  

        if idprojeto not in projetos_ids or idprojetorelacionado not in projetos_ids:
            print("Um ou ambos os projetos informados não existem no banco.")
        else:
            situacao_principal = None
            for p in projetos_dados:
                if str(p[0]) == idprojeto:  # Usando o ID do projeto corretamente (geralmente p[0] é o ID)
                    situacao_principal = p[2]  # Supondo que a situação esteja na posição 2 (ajuste conforme necessário)
            
            if situacao_principal is None:
                print("Não foi possível encontrar o projeto principal.")
            elif situacao_principal != 'Ativo':  # Garantindo que estamos comparando com a string 'Ativo'
                print("O projeto principal não está ativo.")
            else:
                projeto_relacionado = ProjetoRelacionado(
                    idprojeto=idprojeto,
                    idprojetorelacionado=idprojetorelacionado
                )
                projeto_relacionado.inserir()
                print("Projeto Relacionado incluído com sucesso!")

    elif opcao == '5':
        def validar_data(data):
            try:
                datetime.strptime(data, "%Y-%m-%d")
                return True
            except ValueError:
                return False
        def verificar_funcionario_existente(idfuncionario):
            funcionarios = Funcionario.listar()
            return any(str(f[0]) == idfuncionario for f in funcionarios)
        nome = input("Digite o nome do projeto: ").strip()
        descricao = input("Digite a descrição do projeto: ").strip()
        while True:
            datainicio = input("Digite a data de início (AAAA-MM-DD): ").strip()
            if validar_data(datainicio):
                break
            else:
                print("Data inválida! Use o formato AAAA-MM-DD.")
        datafim = None
        situacao = 'Ativo'
        while True:
            idresponsavel = input("Digite o ID do responsável: ").strip()
            if verificar_funcionario_existente(idresponsavel):
                break
            else:
                print("ID de responsável inválido!")
        if Projeto.existe_projeto(nome, datainicio):
            data_formatada = datetime.strptime(datainicio, "%Y-%m-%d").strftime("%m/%y")
            novo_nome = f"{nome} ({data_formatada})"
            if Projeto.existe_nome(novo_nome):
                print("Já existe um projeto com esse nome adaptado. Inclusão cancelada.")
                return 
            print(f"Projeto já existe com esse nome e data. Nome alterado para: {novo_nome}")
        else:
            novo_nome = nome
        projeto = Projeto(nome=novo_nome, descricao=descricao, datainicio=datainicio,
                        datafim=datafim, situacao=situacao, idresponsavel=idresponsavel)
        projeto.inserir()
        print("Projeto incluído com sucesso!")

def remover():
    print("\nEscolha uma tabela para remover:")
    print("1 - Departamento")
    print("2 - Funcionário")
    print("3 - Atividade")
    print("4 - Projeto Relacionado")
    print("5 - Projeto")  
    opcao = input("Escolha a opção: ")

    if opcao == '1':
        iddepartamento = input("Digite o ID do departamento a ser removido: ").strip()
        funcionarios = Funcionario.listar()
        existe_funcionario = any(str(f[2]) == iddepartamento for f in funcionarios)  # Supondo que f[2] seja iddepartamento
        if existe_funcionario:
            print("Não é possível remover o departamento: há funcionários associados.")
        else:
            departamento = Departamento(iddepartamento=iddepartamento)
            departamento.deletar()
            print("Departamento removido com sucesso!")

    elif opcao == '2':
        idfuncionario = input("Digite o ID do funcionário a ser removido: ").strip()
        atividades = Atividade.listar()
        projetos = Projeto.listarCompleto()
        tem_atividade = any(str(a[7]) == idfuncionario for a in atividades)  
        tem_projeto = any(str(p[3]) == idfuncionario for p in projetos)     
        if tem_atividade or tem_projeto:
            print("Não é possível remover o funcionário: há atividades ou projetos associados.")
        else:
            funcionario = Funcionario(idfuncionario=idfuncionario)
            funcionario.deletar()
            print("Funcionário removido com sucesso!")

    elif opcao == '3':
        idatividade = input("Digite o ID da atividade a ser removida: ").strip()
        atividade = Atividade(idatividade=idatividade)
        atividade.deletar()
        print("Atividade removida com sucesso!")

    elif opcao == '4':
        idrelacionamento = input("Digite o ID do relacionamento a ser removido: ").strip()
        projeto_relacionado = ProjetoRelacionado(idprojeto=None, idprojetorelacionado=None)
        projeto_relacionado.deletar(idrelacionamento)
        print("Projeto Relacionado removido com sucesso!")


    elif opcao == '5':
        idprojeto = input("Digite o ID do projeto a ser removido: ").strip()
        atividades = Atividade.listar()
        relacionados = ProjetoRelacionado.listar()  
        tem_atividade = any(str(a[6]) == idprojeto for a in atividades)  
        tem_relacionamento = any(str(r[0]) == idprojeto or str(r[1]) == idprojeto for r in relacionados)
        if tem_atividade or tem_relacionamento:
            print("Não é possível remover o projeto: há atividades ou relacionamentos associados.")
        else:
            projeto = Projeto(idprojeto=idprojeto)
            projeto.deletar()
            print("Projeto removido com sucesso!")

def consultar():
    print("\nEscolha uma tabela para consultar:")
    print("1 - Departamento")
    print("2 - Funcionário")
    print("3 - Atividade")
    print("4 - Projeto Relacionado")
    print("5 - Projeto")  
    opcao = input("Escolha a opção: ")

    if opcao == '1':
        departamentos = Departamento.listar()
        for dep in departamentos:
            print(dep)
    elif opcao == '2':
        funcionarios = Funcionario.listar()
        for func in funcionarios:
            print(func)
    elif opcao == '3':
        atividades = Atividade.listar()
        for atv in atividades:
            print(atv)
    elif opcao == '4':
        projetos_relacionados = ProjetoRelacionado.listar()
        for pr in projetos_relacionados:
            print(pr)
    elif opcao == '5':  
        projetos = Projeto.listar()
        for proj in projetos:
            print(proj)

def atualizar():
    print("\nEscolha uma tabela para atualizar:")
    print("1 - Departamento")
    print("2 - Funcionário")
    print("3 - Atividade")
    print("4 - Projeto Relacionado")
    print("5 - Projeto")  
    opcao = input("Escolha a opção: ")

    if opcao == '1':
        iddepartamento = input("Digite o ID do departamento a ser atualizado: ")
        nome = input("Digite o novo nome do departamento: ")
        departamento = Departamento(iddepartamento=iddepartamento, nmdepartamento=nome)
        departamento.atualizar()
        print("Departamento atualizado com sucesso!")
    elif opcao == '2':
        idfuncionario = input("Digite o ID do funcionário a ser atualizado: ")
        nome = input("Digite o novo nome do funcionário: ")
        iddepartamento = input("Digite o novo ID do departamento: ")
        funcionario = Funcionario(idfuncionario=idfuncionario, nmfuncionario=nome, iddepartamento=iddepartamento)
        funcionario.atualizar()
        print("Funcionário atualizado com sucesso!")
    elif opcao == '3':
        idatividade = input("Digite o ID da atividade a ser atualizada: ")
        nome = input("Digite o novo nome da atividade: ")
        descricao = input("Digite a nova descrição: ")
        datainicio = input("Digite a nova data de início (AAAA-MM-DD): ")
        datafim = input("Digite a nova data de fim (AAAA-MM-DD): ")
        situacao = input("Digite a nova situação da atividade: ")
        idprojeto = input("Digite o novo ID do projeto: ")
        idresponsavel = input("Digite o novo ID do responsável: ")
        atividade = Atividade(idatividade=idatividade, nmatividade=nome, descricao=descricao, 
                              datainicio=datainicio, datafim=datafim, situacao=situacao, 
                              idprojeto=idprojeto, idresponsavel=idresponsavel)
        atividade.atualizar()
        print("Atividade atualizada com sucesso!")
    elif opcao == '4':
        idprojeto = input("Digite o ID do projeto: ")
        idprojetorelacionado = input("Digite o novo ID do projeto relacionado: ")
        projeto_relacionado = ProjetoRelacionado(idprojeto=idprojeto, idprojetorelacionado=idprojetorelacionado)
        projeto_relacionado.atualizar()
        print("Projeto Relacionado atualizado com sucesso!")
    elif opcao == '5':  # Opção para atualizar projeto
        idprojeto = input("Digite o ID do projeto a ser atualizado: ")
        nome = input("Digite o novo nome do projeto: ")
        descricao = input("Digite a nova descrição do projeto: ")
        datainicio = input("Digite a nova data de início (AAAA-MM-DD): ")
        datafim = input("Digite a nova data de fim (AAAA-MM-DD): ")
        situacao = input("Digite a nova situação do projeto: ")
        idresponsavel = input("Digite o novo ID do responsável: ")
        projeto = Projeto(idprojeto=idprojeto, nmprojeto=nome, descricao=descricao, 
                          datainicio=datainicio, datafim=datafim, situacao=situacao, 
                          idresponsavel=idresponsavel)
        projeto.atualizar()
        print("Projeto atualizado com sucesso!")

def operacoes_especiais():
    while True:
        print("\n==== Operações Especiais ====")
        print("1 - Transferir Funcionário de Departamento")
        print("2 - Criar Atividade com Estado Inicial")
        print("3 - Executar Atividade")
        print("4 - Criar Projeto com Situação 'Ativo'")
        print("5 - Executar Projeto")
        print("6 - Suspender Projeto")
        print("7 - Reativar Projeto")
        print("8 - Relacionar Projetos")
        print("0 - Voltar ao Menu Principal")
        opcao = input("Escolha a opção: ")

        if opcao == '1':
            idfuncionario = input("ID do funcionário a ser transferido: ").strip()
            funcionarios = Funcionario.listar()
            if not any(str(f[0]) == idfuncionario for f in funcionarios):
                print("Funcionário não encontrado.")
                continue
            for dep in Departamento.listar():
                print(dep)
            idnovo_departamento = input("Novo ID de departamento: ").strip()
            funcionario = Funcionario(idfuncionario=idfuncionario)
            funcionario.transferir(idnovo_departamento)
            
        elif opcao == '2':
            nome = input("Digite o nome da atividade: ").strip()
            descricao = input("Digite a descrição da atividade: ").strip()
            while True:
                datainicio = input("Digite a data de início (AAAA-MM-DD): ").strip()
                try:
                    datetime.strptime(datainicio, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Formato de data inválido. Use o formato AAAA-MM-DD.")
            datafim = None
            situacao = input("Situação inicial (Pendente ou Em Andamento): ").strip()

            situacoes_validas = ["Pendente", "Em Andamento"]
            if situacao not in situacoes_validas:
                print("Situação inválida. As opções válidas são: Pendente ou Em Andamento.")
                continue
            op = input("Deseja visualizar os projetos existentes? 1-Sim 2-Nao: ").strip()
            if op == '1':
                project = Projeto.listar()
                for proj in project:
                    print(proj)
            idprojeto = input("Digite o ID do projeto: ").strip()
            op = input("Deseja visualizar os funcionários existentes? 1-Sim 2-Nao: ").strip()
            if op == '1':
                funcionario = Funcionario.listar()
                for fun in funcionario:
                    print(fun)
            idresponsavel = input("Digite o ID do responsável: ").strip()
            atividades_existentes = Atividade.listar()
            atividade_ja_existe = any(
                a[1].strip().lower() == nome.lower() and
                str(a[3]) == datainicio and
                str(a[6]) == idprojeto
                for a in atividades_existentes
            )
            if atividade_ja_existe:
                print("Já existe uma atividade com esse nome, data e projeto.")
            else:
                atividade = Atividade(
                    nmatividade=nome,
                    descricao=descricao,
                    datainicio=datainicio,
                    datafim=datafim,
                    situacao=situacao,
                    idprojeto=idprojeto,
                    idresponsavel=idresponsavel
                )
            atividade.inserir()
            print("Atividade incluída com sucesso!")


        elif opcao == '3':
            atividades = Atividade.listar()
            for a in atividades:
                print(a)

            idatividade = input("ID da atividade: ").strip()

            if not any(str(a[0]) == idatividade for a in atividades):
                print("Atividade não encontrada.")
                return

            atividade = Atividade(idatividade=idatividade)

            atividade.atualizar_situacao()

        elif opcao == '4':
            def validar_data(data):
                try:
                    datetime.strptime(data, "%Y-%m-%d")
                    return True
                except ValueError:
                    return False
            def verificar_funcionario_existente(idfuncionario):
                funcionarios = Funcionario.listar()
                return any(str(f[0]) == idfuncionario for f in funcionarios)
            nome = input("Digite o nome do projeto: ").strip()
            descricao = input("Digite a descrição do projeto: ").strip()
            while True:
                datainicio = input("Digite a data de início (AAAA-MM-DD): ").strip()
                if validar_data(datainicio):
                    break
                else:
                    print("Data inválida! Use o formato AAAA-MM-DD.")
            datafim = None
            situacao = 'Ativo'
            while True:
                idresponsavel = input("Digite o ID do responsável: ").strip()
                if verificar_funcionario_existente(idresponsavel):
                    break
                else:
                    print("ID de responsável inválido!")
            if Projeto.existe_projeto(nome, datainicio):
                data_formatada = datetime.strptime(datainicio, "%Y-%m-%d").strftime("%m/%y")
                novo_nome = f"{nome} ({data_formatada})"
                if Projeto.existe_nome(novo_nome):
                    print("Já existe um projeto com esse nome adaptado. Inclusão cancelada.")
                    return 
                print(f"Projeto já existe com esse nome e data. Nome alterado para: {novo_nome}")
            else:
                novo_nome = nome
            projeto = Projeto(nome=novo_nome, descricao=descricao, datainicio=datainicio,
                            datafim=datafim, situacao=situacao, idresponsavel=idresponsavel)
            projeto.inserir()
            print("Projeto incluído com sucesso!")

        elif opcao == '5':
            projetos = Projeto.listar()
            for p in projetos:
                print(p)
            
            idprojeto = input("ID do projeto: ").strip()

            projeto = Projeto.criar_por_id(idprojeto)
            
            if not projeto:
                print("Projeto não encontrado.")
                continue

            projeto.atualizar_situacao()

        elif opcao == '6':
            projetos = Projeto.listar()
            for p in projetos:
                print(p)
            
            idprojeto = input("ID do projeto: ").strip()

            projeto = Projeto.criar_por_id(idprojeto)
            
            if not projeto:
                print("Projeto não encontrado.")
                continue

            projeto.atualizar_situacao_suspensa()

        elif opcao == '7':
            projetos = Projeto.listar()
            for p in projetos:
                print(p)
            
            idprojeto = input("ID do projeto: ").strip()

            projeto = Projeto.criar_por_id(idprojeto)
            
            if not projeto:
                print("Projeto não encontrado.")
                continue

            projeto.atualizar_situacao_reativar()

        elif opcao == '8':
            projetos = Projeto.listar()
            for proj in projetos:
                    print(proj)
            idprojeto = input("Digite o ID do projeto principal: ").strip()
            idprojetorelacionado = input("Digite o ID do projeto a ser relacionado: ").strip()
            
            projetos_dados = Projeto.listar()
            projetos_ids = [str(p[0]) for p in projetos_dados]  # Ajustado para comparar com o ID do projeto

            if idprojeto not in projetos_ids or idprojetorelacionado not in projetos_ids:
                print("Um ou ambos os projetos informados não existem no banco.")
            else:
                situacao_principal = None
                for p in projetos_dados:
                    if str(p[0]) == idprojeto:  # Usando o ID do projeto corretamente (geralmente p[0] é o ID)
                        situacao_principal = p[2]  # Supondo que a situação esteja na posição 2 (ajuste conforme necessário)
                
                if situacao_principal is None:
                    print("Não foi possível encontrar o projeto principal.")
                elif situacao_principal != 'Ativo':  # Garantindo que estamos comparando com a string 'Ativo'
                    print("O projeto principal não está ativo.")
                else:
                    projeto_relacionado = ProjetoRelacionado(
                        idprojeto=idprojeto,
                        idprojetorelacionado=idprojetorelacionado
                    )
                    projeto_relacionado.inserir()
                    print("Projeto Relacionado incluído com sucesso!")

        elif opcao == '0':
            break
        else:
            print("Opção inválida.")

def menu_crud():
    while True:
        print("\n====== Submenu: Operações CRUD ======")
        print("1 - Incluir")
        print("2 - Remover")
        print("3 - Consultar")
        print("4 - Atualizar")
        print("0 - Voltar ao Menu Principal")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            incluir()
        elif opcao == '2':
            remover()
        elif opcao == '3':
            consultar()
        elif opcao == '4':
            atualizar()
        elif opcao == '0':
            print("Voltando ao menu principal...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_relatorios():
    while True:
        print("\n====== Submenu: Relatórios ======")
        print("1 - Percentual de conclusão do Projeto por responsável")
        print("2 - Projetos sem atividades associadas")
        print("3 - Departamento, Funcionários, projetos e atividades")
        print("4 - Responsáveis com atividades em período determinado")
        print("5 - Percentual de atividades concluídas por departamento")
        print("6 - Responsáveis por projetos com percentual de conclusão")
        print("7 - Percentual de conclusão de macroprojetos")
        print("8 - Percentual de atividades por responsável")
        print("9 - Percentual de conclusão de atividades por funcionário")
        print("0 - Voltar ao Menu Principal")
        opcao = input("Escolha uma opção: ")

        sql = None
        params = None

        if opcao == '1':
            sql = """
                SELECT 
                    p.idprojeto, 
                    p.nmprojeto AS projeto, 
                    f.nmfuncionario AS responsavel,  
                    COUNT(a.idatividade) AS atividades_totais, 
                    COALESCE(atf.qtfinalizado, 0) AS finalizadas,
                    (COALESCE(atf.qtfinalizado, 0)::decimal/COUNT(a.idatividade)::decimal*100)::char(4)  AS Percentual
                    FROM projetos p
                INNER JOIN atividades a ON a.idprojeto = p.idprojeto 
                INNER JOIN funcionarios f ON p.idresponsavel = f.idfuncionario 
                INNER JOIN departamentos d ON d.iddepartamento = f.iddepartamento 
                LEFT JOIN (
                    SELECT 
                        p.idprojeto, 
                        COUNT(a.idatividade) AS qtfinalizado 
                    FROM projetos p 
                    INNER JOIN atividades a ON a.idprojeto = p.idprojeto 
                    WHERE a.situacao = 'Encerrado' 
                    GROUP BY p.idprojeto 
                ) atf ON atf.idprojeto = p.idprojeto 
                GROUP BY p.idprojeto, p.nmprojeto, f.nmfuncionario, atf.qtfinalizado
            """
        elif opcao == '2':
            sql = """
                select p.idprojeto, p.nmprojeto, f.nmfuncionario as responsavel, a.nmatividade from projetos p

                inner join funcionarios f
                on p.idresponsavel = f.idfuncionario

                left join atividades a
                on p.idprojeto = a.idprojeto

                where a.idprojeto is null
            """
        elif opcao == '3':
            sql = """
                select distinct p.idprojeto, p.nmprojeto, f.nmfuncionario as responsavel,df.nmdepartamento as Departamento_responsavel, a.nmatividade,  ex.nmfuncionario as executor,dex.nmdepartamento as Departamento_executor, a.datainicio, a.datafim, a.situacao as situacao_atividade, p.situacao as situacao_projeto from projetos p
                inner join funcionarios f
                on p.idresponsavel = f.idfuncionario
                inner join departamentos df
                on df.iddepartamento = f.iddepartamento
                inner join atividades a
                on p.idprojeto = a.idprojeto
                inner join funcionarios ex
                on ex.idfuncionario = a.idresponsavel
                inner join departamentos dex
                on ex.iddepartamento = dex.iddepartamento
            """
        elif opcao == '4':
            def validar_data(data):
                try:
                    datetime.strptime(data, "%Y-%m-%d")
                    return True
                except ValueError:
                    return False
            
            while True:
                data_inicio = input("Informe a data inicial (AAAA-MM-DD): ")
                if validar_data(data_inicio):  # Valida a data inicial
                    break
                else:
                    print("Data inicial no formato inválido. Por favor, use o formato AAAA-MM-DD.")

            while True:
                data_fim = input("Informe a data final (AAAA-MM-DD): ")
                if validar_data(data_fim):  # Valida a data final
                    break
                else:
                    print("Data final no formato inválido. Por favor, use o formato AAAA-MM-DD.")

            sql = """
                SELECT DISTINCT 
                    p.idprojeto, 
                    p.nmprojeto, 
                    a.nmatividade,  
                    ex.nmfuncionario AS executor,
                    dex.nmdepartamento AS Departamento_executor, 
                    a.datainicio, 
                    a.datafim, 
                    a.situacao AS situacao_atividade, 
                    p.situacao AS situacao_projeto 
                FROM projetos p
                INNER JOIN atividades a ON p.idprojeto = a.idprojeto
                INNER JOIN funcionarios ex ON ex.idfuncionario = a.idresponsavel
                INNER JOIN departamentos dex ON ex.iddepartamento = dex.iddepartamento
                WHERE a.datainicio >= %s AND a.datafim <= %s
            """
            params = (data_inicio, data_fim)
        elif opcao == '5':
            sql = """
                SELECT 
                    d.nmdepartamento AS Departamento,  
                    COUNT(a.idatividade) AS atividades_totais, 
                    COALESCE(atf.qtfinalizado, 0) AS finalizadas,
                    (COALESCE(atf.qtfinalizado, 0)::decimal/COUNT(a.idatividade)::decimal*100)::char(4)  AS Percentual
                    FROM projetos p
                INNER JOIN atividades a ON a.idprojeto = p.idprojeto 
                INNER JOIN funcionarios f ON p.idresponsavel = f.idfuncionario 
                INNER JOIN departamentos d ON d.iddepartamento = f.iddepartamento 
                LEFT JOIN (
                    SELECT 
                        d.nmdepartamento, 
                        COUNT(a.idatividade) AS qtfinalizado 
                    FROM projetos p 
					inner join funcionarios f ON f.idfuncionario = p.idresponsavel
					inner join departamentos d ON d.iddepartamento = f.iddepartamento
                    INNER JOIN atividades a ON a.idprojeto = p.idprojeto 
                    WHERE a.situacao = 'Encerrado' 
                    GROUP BY d.nmdepartamento
                ) atf ON atf.nmdepartamento = d.nmdepartamento 
                GROUP BY  d.nmdepartamento, atf.qtfinalizado
            """
        elif opcao == '6':
            sql = """
                SELECT 
                    f.nmfuncionario AS Responsavel,  
                    COUNT(a.idatividade) AS atividades_totais, 
                    COALESCE(atf.qtfinalizado, 0) AS finalizadas,
                    (COALESCE(atf.qtfinalizado, 0)::decimal/COUNT(a.idatividade)::decimal)::char(4)  AS Percentual
                    FROM projetos p
                INNER JOIN atividades a ON a.idprojeto = p.idprojeto 
                INNER JOIN funcionarios f ON p.idresponsavel = f.idfuncionario 
                LEFT JOIN (
                    SELECT 
                        f.idfuncionario, 
                        COUNT(a.idatividade) AS qtfinalizado 
                    FROM projetos p 
					inner join funcionarios f ON f.idfuncionario = p.idresponsavel
                    INNER JOIN atividades a ON a.idprojeto = p.idprojeto 
                    WHERE a.situacao = 'Encerrado' 
                    GROUP BY f.idfuncionario
                ) atf ON atf.idfuncionario = f.idfuncionario 
                GROUP BY  f.idfuncionario, atf.qtfinalizado
            """
        elif opcao == '7':
            sql = """
                SELECT pp.idprojetomacro,pp.macroprojeto,pp.responsavel_geral,COUNT(PF.idsubprojeto) quantidade_subprojetos,
                ((SUM(pf.finalizados_sub) + pp.finalizados)::decimal/(SUM(pf.total_sub) + pp.total)::decimal *100)::char(4) perc_macro_projeto FROM 
                (select distinct 
                p.idprojeto as idprojetomacro,
                p.nmprojeto as MacroProjeto,
                f.nmfuncionario as Responsavel_Geral,
                count(a.idatividade) total,
                sum (case when a.situacao = 'Encerrado' then 1 else 0 end) finalizados
                from projetos p

                inner join atividades a
                on a.idprojeto = p.idprojeto

                inner join funcionarios f 
                on f.idfuncionario = p.idresponsavel

                group by p.idprojeto,p.nmprojeto, f.nmfuncionario
                ) PP

                inner join projetosrelacionamentos pr
                on pr.idprojeto = pp.idprojetomacro

                left join
                (select distinct p.idprojeto as idsubprojeto,
                count(a.idatividade) total_sub,
                sum (case when a.situacao = 'Encerrado' then 1 else 0 end) finalizados_sub
                from projetos p

                inner join atividades a
                on a.idprojeto = p.idprojeto

                group by p.idprojeto
                ) pf on pf.idsubprojeto = pr.idprojetorelacionado

                group by
                pp.idprojetomacro,pp.macroprojeto,pp.responsavel_geral, pp.total,pp.finalizados
            """
        elif opcao =='8':
            sql =  """
                    SELECT 
                    f.nmfuncionario AS Executor,  
                    COUNT(a.idatividade) AS atividades_totais, 
                    COALESCE(atf.qtfinalizado, 0) AS finalizadas,
					(COUNT(a.idatividade) - COALESCE(atf.qtfinalizado, 0) ) AS Atividades_Pendentes,
                    (COALESCE(atf.qtfinalizado, 0)::decimal/COUNT(a.idatividade)::decimal*100)::char(4)  AS Percentual
                    FROM projetos p
                INNER JOIN atividades a ON a.idprojeto = p.idprojeto 
                INNER JOIN funcionarios f ON a.idresponsavel = f.idfuncionario 
                LEFT JOIN (
                    SELECT 
                        f.idfuncionario, 
                        COUNT(a.idatividade) AS qtfinalizado 
                    FROM projetos p 
                    INNER JOIN atividades a ON a.idprojeto = p.idprojeto 
					inner join funcionarios f ON f.idfuncionario = a.idresponsavel

                    WHERE a.situacao = 'Encerrado' 
                    GROUP BY f.idfuncionario
                ) atf ON atf.idfuncionario = f.idfuncionario 
                GROUP BY  f.idfuncionario, atf.qtfinalizado
            """
        elif opcao == '9':
            sql = """
                select d.nmdepartamento,f.nmfuncionario, (sum(case when a.situacao = 'Encerrado' then 1 else 0 end)::decimal/count(a.idatividade)::decimal*100)::char(4) as perc from funcionarios f

                inner join departamentos d
                on d.iddepartamento = f.iddepartamento

                inner join atividades a
                on f.idfuncionario = a.idresponsavel

                group by d.nmdepartamento,f.nmfuncionario
                """
        elif opcao == '0':
            print("Voltando ao menu principal...")
            break
        else:
            print("Opção inválida. Tente novamente.")
            continue

        if sql:
            try:
                con = Conector()
                con.conectar()
                resultados = con.consultar(sql, params)
                
                if resultados:
                    colunas = [desc[0] for desc in con.cur.description]
                    print(f"{' | '.join(colunas)}")  
                    print("-" * 100)  

                    
                    for r in resultados:
                        print(" | ".join(str(v) for v in r)) 
                else:
                    print("Nenhum dado encontrado.")
                
                con.fechar()
            except Exception as e:
                print(f"Erro ao consultar dados: {e}")


def main():
    while True:
        opcao = menu()
        if opcao == '1':
            menu_crud()
        elif opcao =='2':
            operacoes_especiais()
        elif opcao =='3':
            menu_relatorios()
        elif opcao == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
