# BAN-II
Projeto realziado para a disciplina de Banco de Dados II da Udesc CCT

A execução principal, é feita pelo arquivo main.py

Esse projeto foi criado em Python e utiliza da biblioteca de psycopg2 para utilizar dos recursos de banco de dados, sendo necessário executar a primeira vez o seguinte comando para instalar as dependencias em seu computador, recomendavel realizar por meio do vscode a instalação do python nas extensões e a execução deste comando abaixo:
py -m pip install psycopg2-binary

Caso ocorra em falha por versão do Python:
python -m pip install psycopg2-binary ou pip install psycopg2-binary

Lembre de ter primeiramente o Python instalado em seu computador e o Postgresql também, caso ainda não tenha
Se por acaso, a versão do python em seu computador for antigo, é preciso instalar ainda o Pip, sendo necessário instalar uma versão mais recente do Python.

Também é preciso que para conectar em seu banco de dados, altere as credencias do arquivo config.py, como foi mostrado em vídeo, trocando a senha para conectar ao banco, que é somente para colocar as credencias configuradas em seu localhost usadas para conectar ao banco.


Para executar este projeto, no seu VSCODE descompacte o arquivo .zip, abra essa pasta pelo VSCODE e após ter todas as premissas acima, faça a execução por meio do arquivo main.py. Este arquivo contem todas as dependencias para realizar a execução correta, os demais arquivos foram feitos para facilitar na manipulação das tabelas. Toda a execução deve ser realizada por meio do arquivo main.py
