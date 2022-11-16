# Driver de instalação ODBC - Windows: https://learn.microsoft.com/pt-br/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15

# Importações de Bibliotecas:
import pyodbc
from tokenize import String
import json
import time
from datetime import datetime
import platform
import mysql.connector
from mysql.connector import errorcode
from ast import Str
import os
import sys
import random
import string

print("\U0001F916 Ola Usuario, seja bem-vindo, irei te auxiliar em todo o processo de adequação do sistema!", "\n--------")

print("\U0001F916 Estou identificando qual é o seu sistema operacional para me permitir validar algumas coisas...", "\n--------")


def buscar_sistema_operacional():
    os_type = sys.platform.lower()
    if "win" in os_type:
        command = 'pip list | findstr /c:"{}"'
    elif "linux" in os_type:
        command = 'pip list | grep {}'
    return command


print("\U0001F916 O seu sistema operacional é",
      platform.uname().system, "\n--------")

bibliotecas = ['mysql-connector-python', 'pyodbc']


def validLibrary(bibliotecas):
    print("\U0001F916 Vou iniciar algumas validações de bibliotecas agora.", "\n--------")
    for i in bibliotecas:
        command = buscar_sistema_operacional().format(i)
        exibir = os.popen(command).read()

        if (exibir == ''):
            print("\U0001F916 Opa! identifiquei que a biblioteca",
                  i, "não esta instalada!", "\n--------")
            time.sleep(2)
            print("\U0001F916 Mas não se preocupe, vou instalar a biblioteca",
                  i, "para você.", "\n--------")
            ins = 'pip install {}'.format(i)
            os.system(ins)

        else:
            print("\U0001F916 Que ótimo, você ja tem a biblioteca",
                  exibir, "\n--------")


validLibrary(bibliotecas)

escolha = 1


def buscar_serial():
    os_type = sys.platform.lower()
    if "win" in os_type:
        command = "wmic bios get serialnumber"
    elif "linux" in os_type:
        command = "hal-get-property --udi /org/freedesktop/Hal/devices/computer --key system.hardware.uuid"
    elif "darwin" in os_type:
        command = "ioreg -l | grep IOPlatformSerialNumber"
    return os.popen(command).read().replace("\n", "").replace("	", "").replace(" ", "")


def captura(conn, coxn):
    cursor = conn.cursor()
    cursor_sql = coxn.cursor()

    print("Seja bem-vindo ao sistema de captura de dados do seu Hardware \U0001F604")

    print("\U0001F750 Iniciando captura dos dados...", "\n--------")

    meu_sistema = platform.uname()
    sistema = meu_sistema.system
    arqmaquina = meu_sistema.machine
    nomeMaquina = meu_sistema.node
    modelo = meu_sistema.processor
    numero_serial = buscar_serial()

    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open(dir_path + '/' + 'estadosCidades.json') as file:
        data = json.load(file)

    while True:
        def validacaoRegiao():
            # MySQL
            cursor.execute(
                "SELECT COUNT(idRegiao) FROM GustavoRegiao")
            rowRegi = cursor.fetchone()
            Regiao = int(''.join(map(str, rowRegi)))
            print("\U0001F916 MySQL - Regiões detectadas:", Regiao, "\n--------")

            if Regiao == 0:
                nomeRegiao = data['regiao']
                cursor.execute("INSERT INTO GustavoRegiao (nomeRegiao) VALUES (%s);",
                               (nomeRegiao,))
                conn.commit()
                print("\U0001F916 MySQL - Inserção de dados de Regiões: 1", "\n--------")

            # SQL Server
            cursor_sql.execute(
                "SELECT COUNT(idRegiao) FROM GustavoRegiao")
            rowRegi_sql = cursor_sql.fetchone()
            Regiao_sql = int(''.join(map(str, rowRegi_sql)))
            print("\U0001F916 SQL Server - Regiões detectadas:",
                  Regiao_sql, "\n--------")

            if Regiao_sql == 0:
                nomeRegiao = data['regiao']
                print(nomeRegiao)
                cursor_sql.execute("INSERT INTO GustavoRegiao (nomeRegiao) VALUES (?);",
                                   (nomeRegiao,))
                coxn.commit()
                print("\U0001F916 SQL Server - Inserção de dados de Regiões: 1")

            time.sleep(2)

            # MySQL
            cursor.execute(
                "SELECT COUNT(idRegiao) FROM GustavoRegiao")
            rowRegi = cursor.fetchone()
            Regiao = int(''.join(map(str, rowRegi)))
            print("\U0001F916 MySQL - Validação de Regiões detectadas:",
                  Regiao, "\n--------")

            # SQL Server
            cursor_sql.execute(
                "SELECT COUNT(idRegiao) FROM GustavoRegiao")
            rowRegi_sql = cursor_sql.fetchone()
            Regiao_sql = int(''.join(map(str, rowRegi_sql)))
            print("\U0001F916 SQL Server - Validação Regiões detectadas:",
                  Regiao_sql, "\n--------")

            if Regiao and Regiao_sql != 0:
                validacaoEstado(Regiao, Regiao_sql)
            else:
                validacaoRegiao()

        def validacaoEstado(Regiao, Regiao_sql):
            # MySQL
            cursor.execute(
                "SELECT COUNT(idEstado) FROM GustavoEstado")
            rowEsta = cursor.fetchone()
            Estado = int(''.join(map(str, rowEsta)))
            print("\U0001F916 MySQL - Estados detectados:", Estado, "\n--------")

            if Estado == 0:
                tamanhoEstado = len(data['estados'])
                print(tamanhoEstado)
                for i in range(tamanhoEstado):

                    nomeSigla = data['estados'][i]['sigla']
                    nomeEstado = data['estados'][i]['nome']

                    cursor.execute(
                        "INSERT INTO GustavoEstado (sigla, nomeEstado) VALUES (%s,%s);", (nomeSigla, nomeEstado))
                    print("\U0001F916 MySQL - Inserção de dados de Estados:",
                          i, nomeSigla, nomeEstado,  "\n--------")
                    conn.commit()

            # SQL Server
            cursor_sql.execute(
                "SELECT COUNT(idEstado) FROM GustavoEstado")
            rowEsta_sql = cursor_sql.fetchone()
            Estado_sql = int(''.join(map(str, rowEsta_sql)))
            print("\U0001F916 SQL Server - Estados detectados:",
                  Estado_sql, "\n--------")

            if Estado_sql == 0:
                tamanhoEstado = len(data['estados'])
                print(tamanhoEstado)
                for i in range(tamanhoEstado):

                    nomeSigla = data['estados'][i]['sigla']
                    nomeEstado = data['estados'][i]['nome']

                    cursor_sql.execute(
                        "INSERT INTO GustavoEstado (sigla, nomeEstado) VALUES (?,?);", (nomeSigla, nomeEstado))
                    print("\U0001F916 SQL Server - Inserção de dados de Estados:",
                          i, nomeSigla, nomeEstado, "\n--------")
                    coxn.commit()

            time.sleep(2)

            # MySQL
            cursor.execute(
                "SELECT COUNT(idEstado) FROM GustavoEstado")
            rowEsta = cursor.fetchone()
            Estado = int(''.join(map(str, rowEsta)))
            print("\U0001F916 MySQL - Validação de Estados detectados:",
                  Estado, "\n--------")

            # SQL Server
            cursor_sql.execute(
                "SELECT COUNT(idEstado) FROM GustavoEstado")
            rowEsta_sql = cursor_sql.fetchone()
            Estado_sql = int(''.join(map(str, rowEsta_sql)))
            print("\U0001F916 SQL Server - Validação de Estados detectados:",
                  Estado_sql, "\n--------")

            if Estado and Estado_sql != 0:
                validacaoCidade(Regiao, Estado, Regiao_sql, Estado_sql)
            else:
                validacaoEstado(Regiao, Regiao_sql)

        def validacaoCidade(Regiao, Estado, Regiao_sql, Estado_sql):
            # MySQL
            cursor.execute(
                "SELECT COUNT(idCidade) FROM GustavoCidade")
            rowCid = cursor.fetchone()
            Cids = int(''.join(map(str, rowCid)))
            print("\U0001F916 MySQL - Cidades detectadas:", Cids, "\n--------")

            if Cids == 0:
                for p in range(Regiao):
                    p = p + 1
                    a = p - 1

                    for x in range(Estado):
                        b = x + 1

                        cidade = data['estados'][x]['cidades'][0]
                        cursor.execute("INSERT INTO GustavoCidade (fkRegiao, fkEstado, nomeCidade) VALUES (%s, %s, %s);",
                                       (p, b, cidade))
                        print(
                            "\U0001F916 MySQL - Inserção de dados de Cidades:", b, cidade, "\n--------")
                        conn.commit()

            # SQL Server
            cursor_sql.execute(
                "SELECT COUNT(idCidade) FROM GustavoCidade")
            rowCid_sql = cursor_sql.fetchone()
            Cids_sql = int(''.join(map(str, rowCid_sql)))
            print("\U0001F916 SQL Server - Cidades detectadas:",
                  Cids_sql, "\n--------")

            if Cids_sql == 0:
                for p in range(Regiao_sql):
                    p = p + 1
                    a = p - 1

                    for x in range(Estado_sql):
                        b = x + 1

                        cidade = data['estados'][x]['cidades'][0]
                        cursor_sql.execute("INSERT INTO GustavoCidade (fkRegiao, fkEstado, nomeCidade) VALUES (?, ?, ?);",
                                           (p, b, cidade))
                        print(
                            "\U0001F916 SQL Server - Inserção de dados de Cidades:", b, cidade, "\n--------")
                        coxn.commit()

            time.sleep(2)

            # MySQL
            cursor.execute(
                "SELECT COUNT(idCidade) FROM GustavoCidade")
            rowCid = cursor.fetchone()
            Cids = int(''.join(map(str, rowCid)))
            print("\U0001F916 MySQL - Validação de Cidades detectadas:",
                  Cids, "\n--------")

            # SQL Server
            cursor_sql.execute(
                "SELECT COUNT(idCidade) FROM GustavoCidade")
            rowCid_sql = cursor_sql.fetchone()
            Cids_sql = int(''.join(map(str, rowCid_sql)))
            print("\U0001F916 SQL Server - Validação Cidades detectadas:",
                  Cids_sql, "\n--------")

            if Cids and Cids_sql != 0:
                validacaoEquip(Cids, Cids_sql)
            else:
                validacaoCidade(Regiao, Estado, Regiao_sql, Estado_sql)

        def validacaoEquip(Cids, Cids_sql):
            # MySQL
            cursor.execute(
                "SELECT COUNT(idEquipamento) FROM GustavoEquipamento")
            rowEquip = cursor.fetchone()
            Equipamentos = int(''.join(map(str, rowEquip)))
            print("\U0001F916 MySQL - Equipamentos detectados: ",
                  Equipamentos, "\n--------")

            if Equipamentos == 0:

                serialnumber = [numero_serial]
                processadores = [modelo]
                nomemaquinas = [nomeMaquina]
                arquiteturas = [arqmaquina]
                sistemas = [sistema]

                letras = string.ascii_uppercase

                for serial in range(Cids):
                    numeroSerial = ''.join(random.choice(letras)
                                           for _ in range(7))
                    formatSerial = f"SerialNumber{numeroSerial}"
                    serialnumber.append(formatSerial)

                    modeloIntel = 'INTEL CORE I5-10400F, 6-CORE, 12-THREADS, 2.9GHZ '
                    modeloAmd = 'AMD RYZEN 7 5700X, 8-CORE, 16-THREADS, 3.4GHZ'
                    processadores.append(modeloIntel)
                    processadores.append(modeloAmd)

                    apelidoMaquina = ''.join(
                        random.choice(letras) for _ in range(10))
                    nomemaquinas.append(apelidoMaquina)

                    arqIntel = 'x86'
                    arquiteturas.append(arqIntel)
                    arqAMD = 'AMD64'
                    arquiteturas.append(arqAMD)

                    soLinux = 'Linux'
                    sistemas.append(soLinux)
                    soWin = 'Windows'
                    sistemas.append(soWin)
                    soMac = 'MacOS'
                    sistemas.append(soMac)

                cursor.execute(
                    "SELECT COUNT(idRegiao) FROM GustavoRegiao WHERE nomeRegiao = 'Brasil'")
                rowRegi = cursor.fetchone()
                Regiao = int(''.join(map(str, rowRegi)))

                for i in range(Cids):
                    i = i + 1
                    b = i - 1

                    cursor.execute("INSERT INTO GustavoEquipamento (fkRegiao, fkEstado, fkCidade, numeroSerial, apelido, sistemaOperacional, arquitetura, modelo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                                   (Regiao, i, i, serialnumber[b], nomemaquinas[b], sistemas[b], arquiteturas[b], processadores[b]))
                    print("\U0001F916 MySQL - Inserção de dados de Equipamento:", i,
                          serialnumber[b], nomemaquinas[b], sistemas[b], arquiteturas[b], processadores[b], "\n--------")
                    conn.commit()

            # SQL Server
            cursor_sql.execute(
                "SELECT COUNT(idEquipamento) FROM GustavoEquipamento")
            rowEquip_sql = cursor_sql.fetchone()
            Equipamentos_sql = int(''.join(map(str, rowEquip_sql)))
            print("\U0001F916 SQL Server - Equipamentos detectados: ",
                  Equipamentos_sql, "\n--------")

            if Equipamentos_sql == 0:

                serialnumber = [numero_serial]
                processadores = [modelo]
                nomemaquinas = [nomeMaquina]
                arquiteturas = [arqmaquina]
                sistemas = [sistema]

                letras = string.ascii_uppercase

                for serial in range(Cids):
                    numeroSerial = ''.join(random.choice(letras)
                                           for _ in range(7))
                    formatSerial = f"SerialNumber{numeroSerial}"
                    serialnumber.append(formatSerial)

                    modeloIntel = 'INTEL CORE I5-10400F, 6-CORE, 12-THREADS, 2.9GHZ '
                    modeloAmd = 'AMD RYZEN 7 5700X, 8-CORE, 16-THREADS, 3.4GHZ'
                    processadores.append(modeloIntel)
                    processadores.append(modeloAmd)

                    apelidoMaquina = ''.join(
                        random.choice(letras) for _ in range(10))
                    nomemaquinas.append(apelidoMaquina)

                    arqIntel = 'x86'
                    arquiteturas.append(arqIntel)
                    arqAMD = 'AMD64'
                    arquiteturas.append(arqAMD)

                    soLinux = 'Linux'
                    sistemas.append(soLinux)
                    soWin = 'Windows'
                    sistemas.append(soWin)
                    soMac = 'MacOS'
                    sistemas.append(soMac)

                cursor_sql.execute(
                    "SELECT COUNT(idRegiao) FROM GustavoRegiao WHERE nomeRegiao = 'Brasil'")
                rowRegi_sql = cursor_sql.fetchone()
                Regiao_sql = int(''.join(map(str, rowRegi_sql)))

                for i in range(Cids_sql):
                    i = i + 1
                    b = i - 1

                    cursor.execute("INSERT INTO GustavoEquipamento (fkRegiao, fkEstado, fkCidade, numeroSerial, apelido, sistemaOperacional, arquitetura, modelo) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
                                   (Regiao_sql, i, i, serialnumber[b], nomemaquinas[b], sistemas[b], arquiteturas[b], processadores[b]))
                    print("\U0001F916 SQL Server - Inserção de dados de Equipamento:", i,
                          serialnumber[b], nomemaquinas[b], sistemas[b], arquiteturas[b], processadores[b], "\n--------")
                    coxn.commit()

            time.sleep(2)

            # MySQL
            cursor.execute(
                "SELECT COUNT(idEquipamento) FROM GustavoEquipamento")
            rowEquip = cursor.fetchone()
            Equipamentos = int(''.join(map(str, rowEquip)))
            print("\U0001F916 MySQL - Validação de Equipamentos detectados: ",
                  Equipamentos, "\n--------")

            # SQL Server
            cursor_sql.execute(
                "SELECT COUNT(idEquipamento) FROM GustavoEquipamento")
            rowEquip_sql = cursor_sql.fetchone()
            Equipamentos_sql = int(''.join(map(str, rowEquip_sql)))
            print("\U0001F916 SQL Server - Validação de Equipamentos detectados: ",
                  Equipamentos_sql, "\n--------")

            if Equipamentos and Equipamentos_sql != 0:
                validacaoComp()
            else:
                validacaoEquip(Cids, Cids_sql)

        def validacaoComp():
            # MySQL
            cursor.execute("SELECT COUNT(idComponente) FROM GustavoComponente")
            rowComp = cursor.fetchone()
            Componente = int(''.join(map(str, rowComp)))
            print("\U0001F916 MySQL - Componentes detectados: ",
                  Componente, "\n--------")

            if Componente == 0:
                componentes = ['CPU']

                for i in range(len(componentes)):
                    cursor.execute("INSERT INTO GustavoComponente (nomeComponente) VALUES (%s);",
                                   (componentes[i],))
                    conn.commit()
                    print("\U0001F916 MySQL - Inserção de dados de Componentes:",
                          i + 1, componentes[i], "\n--------")

            # SQL Server
            cursor_sql.execute(
                "SELECT COUNT(idComponente) FROM GustavoComponente")
            rowComp_sql = cursor_sql.fetchone()
            Componente_sql = int(''.join(map(str, rowComp_sql)))
            print("\U0001F916 SQL Server - Componentes detectados: ",
                  Componente_sql, "\n--------")

            if Componente_sql == 0:
                componentes = ['CPU', 'Memoria', 'Disco', 'GPU']

                for i in range(len(componentes)):
                    cursor_sql.execute("INSERT INTO GustavoComponente (nomeComponente) VALUES (?);",
                                       (componentes[i],))
                    coxn.commit()
                    print("\U0001F916 SQL Server - Inserção de dados de Componentes:",
                          i + 1, componentes[i], "\n--------")

            if Componente and Componente_sql == 0:
                validacaoComp()

        print("\U0001F916 Iniciando validações de dados: ", "\n--------")
        print("Validação Final - MySQL", "\n--------")
        # MySQL
        cursor.execute("SELECT COUNT(idRegiao) FROM GustavoRegiao")
        rowRegiao = cursor.fetchone()
        Regiao = int(''.join(map(str, rowRegiao)))
        print("\U0001F916 MySQL - Regiões detectadas: ", Regiao, "\n--------")

        cursor.execute("SELECT COUNT(idEstado) FROM GustavoEstado")
        rowEstado = cursor.fetchone()
        Estado = int(''.join(map(str, rowEstado)))
        print("\U0001F916 MySQL - Estados detectados: ", Estado, "\n--------")

        cursor.execute("SELECT COUNT(idCidade) FROM GustavoCidade")
        rowCidade = cursor.fetchone()
        Cidade = int(''.join(map(str, rowCidade)))
        print("\U0001F916 MySQL - Cidades detectadas: ", Cidade, "\n--------")

        cursor.execute("SELECT COUNT(idEquipamento) FROM GustavoEquipamento")
        rowEquip = cursor.fetchone()
        Equipamento = int(''.join(map(str, rowEquip)))
        print("\U0001F916 MySQL - Equipamentos detectados: ",
              Equipamento, "\n--------")

        cursor.execute("SELECT COUNT(idComponente) FROM GustavoComponente")
        rowComponente = cursor.fetchone()
        Componentes = int(''.join(map(str, rowComponente)))
        print("\U0001F916 MySQL - Componentes detectados: ",
              Componentes, "\n--------")

        cursor.execute("SELECT COUNT(idLeitura) FROM GustavoLeitura")
        rowLeitura = cursor.fetchone()
        Leitura = int(''.join(map(str, rowLeitura)))
        print("\U0001F916 MySQL - Leituras detectadas: ",
              Leitura, "\n--------")

        print("Validação Final - SQL Server", "\n--------")
        # SQL Server
        cursor_sql.execute("SELECT COUNT(idRegiao) FROM GustavoRegiao")
        rowRegiao_sql = cursor_sql.fetchone()
        Regiao_sql = int(''.join(map(str, rowRegiao_sql)))
        print("\U0001F916 SQL Server - Regiões detectadas: ",
              Regiao_sql, "\n--------")

        cursor_sql.execute("SELECT COUNT(idEstado) FROM GustavoEstado")
        rowEstado_sql = cursor_sql.fetchone()
        Estado_sql = int(''.join(map(str, rowEstado_sql)))
        print("\U0001F916 SQL Server - Estados detectados: ",
              Estado_sql, "\n--------")

        cursor_sql.execute("SELECT COUNT(idCidade) FROM GustavoCidade")
        rowCidade_sql = cursor_sql.fetchone()
        Cidade_sql = int(''.join(map(str, rowCidade_sql)))
        print("\U0001F916 SQL Server - Cidades detectadas: ",
              Cidade_sql, "\n--------")

        cursor_sql.execute(
            "SELECT COUNT(idEquipamento) FROM GustavoEquipamento")
        rowEquip_sql = cursor_sql.fetchone()
        Equipamento_sql = int(''.join(map(str, rowEquip_sql)))
        print("\U0001F916 SQL Server - Equipamentos detectados: ",
              Equipamento_sql, "\n--------")

        cursor_sql.execute("SELECT COUNT(idComponente) FROM GustavoComponente")
        rowComponente_sql = cursor_sql.fetchone()
        Componentes_sql = int(''.join(map(str, rowComponente_sql)))
        print("\U0001F916 SQL Server - Componentes detectados: ",
              Componentes_sql, "\n--------")

        cursor_sql.execute("SELECT COUNT(idLeitura) FROM GustavoLeitura")
        rowLeitura_sql = cursor_sql.fetchone()
        Leitura_sql = int(''.join(map(str, rowLeitura_sql)))
        print("\U0001F916 SQL Server - Leituras detectadas: ",
              Leitura_sql, "\n--------")

        if Regiao == 0 or Estado == 0 or Cidade == 0 or Equipamento == 0 or Componentes == 0 or Regiao_sql == 0 or Estado_sql == 0 or Cidade_sql == 0 or Equipamento_sql == 0 or Componentes_sql == 0:
            print("\U0001F916 Reiniciando validação geral...")
            validacaoRegiao()
        elif Regiao != 0 and Estado != 0 and Cidade != 0 and Equipamento != 0 and Componentes != 0 and Regiao_sql != 0 and Estado_sql != 0 and Cidade_sql != 0 and Equipamento_sql != 0 and Componentes_sql != 0:
            print(
                "\U0001F916 Ótimo, todo o sistema de tabelas esta parametrizado, iremos para o proximo passo...")
            print("\U0001F916 Estou validando agora se você tem dados nas tabelas de Leitura no MySQL e no SQL Server.")

            print(
                "\U0001F916 Você tem na tabela de Leitura do MySQL um total de registros:", Leitura)
            print("\U0001F916 Você tem na tabela de Leitura do SQL Server no Azure um total de registros:", Leitura_sql)

            conn.close()
            coxn.close()
            break
        else:
            print("\U0001F916 Terei que validar novamente...")
            validacaoRegiao()

        validacaoRegiao()


def validacaoMysql(conn, coxn):
    print("Iniciando validações...")

    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS dashboard;")

    cursor.execute("USE dashboard;")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS GustavoRegiao (
    idRegiao INT PRIMARY KEY AUTO_INCREMENT,
    nomeRegiao VARCHAR(45)
);""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS GustavoEstado (
    idEstado INT PRIMARY KEY AUTO_INCREMENT,
    sigla CHAR(2),
    nomeEstado VARCHAR(45)
);""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS GustavoCidade (
    fkRegiao INT,
    FOREIGN KEY (fkRegiao)
        REFERENCES GustavoRegiao (idRegiao),
    fkEstado INT,
    FOREIGN KEY (fkEstado)
        REFERENCES GustavoEstado (idEstado),
    idCidade INT AUTO_INCREMENT,
    PRIMARY KEY (fkRegiao , fkEstado),
    KEY (idCidade),
    nomeCidade VARCHAR(45)
);""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS GustavoEquipamento (
    fkRegiao INT,
    FOREIGN KEY (fkRegiao)
        REFERENCES GustavoRegiao (idRegiao),
    fkEstado INT,
    FOREIGN KEY (fkEstado)
        REFERENCES GustavoEstado (idEstado),
    fkCidade INT,
    FOREIGN KEY (fkCidade)
        REFERENCES GustavoCidade (idCidade),
    idEquipamento INT AUTO_INCREMENT,
    PRIMARY KEY (fkRegiao , fkEstado , fkCidade),
    KEY (idEquipamento),
    numeroSerial VARCHAR(45),
    apelido VARCHAR(45),
    sistemaOperacional VARCHAR(45),
    arquitetura VARCHAR(45),
    modelo VARCHAR(100)
);
""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS GustavoComponente (
    idComponente INT PRIMARY KEY AUTO_INCREMENT,
    nomeComponente VARCHAR(45)
);""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS GustavoLeitura (
    fkRegiao INT,
    FOREIGN KEY (fkRegiao)
        REFERENCES GustavoRegiao (idRegiao),
    fkEstado INT,
    FOREIGN KEY (fkEstado)
        REFERENCES GustavoEstado (idEstado),
    fkCidade INT,
    FOREIGN KEY (fkCidade)
        REFERENCES GustavoCidade (idCidade),
    fkEquipamento INT,
    FOREIGN KEY (fkEquipamento)
        REFERENCES GustavoEquipamento (idEquipamento),
    fkComponente INT,
    FOREIGN KEY (fkComponente)
        REFERENCES GustavoComponente (idComponente),
    idLeitura INT PRIMARY KEY AUTO_INCREMENT,
	KEY (fkRegiao , fkEstado , fkCidade , fkEquipamento , fkComponente),
    valor FLOAT NOT NULL,
    momento DATE NOT NULL
);""")

    print("MySQL - Validações de tabelas finalizada com sucesso.")
    captura(conn, coxn)


if escolha == 1:
    try:
        print("\U0001F916 Estou tentando me conectar ao banco de dados MySQL e o Banco de dados SQL Server no Azure.", "\n--------")

        conn = mysql.connector.connect(
            host='172.17.0.1',
            user='root',
            password='root',
            port=3305
        )
        print("Consegui! Conexão com o Banco de Dados MySQL efetuada com sucesso.")

        server = 'healthsystem.database.windows.net'
        database = 'healthsystem'
        username = 'grupo01sis'
        password = '#GfHealthSystem01'
        coxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server +
                              ';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD=' + password)

        print("Opa! Conexão com o Banco de Dados SQL Server Azure efetuada com sucesso.")
        validacaoMysql(conn, coxn)

        # Validações de Erro:
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Algo está errado com o Usuário do Banco ou a Senha.")
            time.sleep(10)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("O banco de dados direcionado não existe.")
            time.sleep(10)
        else:
            print(err)
            time.sleep(10)

# DBCC CHECKIDENT('Nome da tabela', RESEED, 0)
