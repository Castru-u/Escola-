#Cria a função de cadastro
def cadastro(parametro):

    #Abre os arquivos a serem usados
    with open("alunos.txt", "a+", encoding="utf-8") as alunos, open("turmas.txt", "a+", encoding="utf-8") as turmas, open("boletins.txt", "a+", encoding="utf-8") as boletins:

        alunos.write(""), turmas.write(""), boletins.write("")   #Cria os arquivos caso não existam

        #Verificam o parametro inserido:

        if parametro.upper() not in ["ALUNO","TURMA","BOLETIM"]:
            #Caso não seja informado um dos parametros acima
            print("Parametro não informado (ALUNO/TURMA/BOLETIM)")

        elif parametro.upper() == "ALUNO":
            #Pede as informações do aluno a ser inserido
            aluno=input("Insira o nome do(a) aluno(a): ")
            email=input("Insira o email do(a) aluno(a): ")
            telefone=int(input("Insira o telefone do responsável do(a) aluno(a): "))
            turma=int(input("Insira o código de turma: "))
            
            turmas.seek(0,0)
            if str(turma) not in [i.split(" | ")[0] for i in turmas.readlines()]:   #Verifica se o cod. de turma existe no sistema
                print("Turma inserida não existe no sistema, procure as existentes ou crie uma")
                
            else:
                alunos.seek(0,0)
                linhas=alunos.readlines()
                matricula=1+int(linhas[-1].split(" | ")[0]) if linhas!=[] else 1   #Cria o número de matrícula

                alunos.write(f"{matricula} | {aluno} | {email} | {telefone} | {turma}\n")   #Adiciona o aluno

        elif parametro.upper() == "TURMA":
            #pede as informações da turma a ser cadastrada
            nome=input("Insira o nome da turma: ")
            turno=(input("Insira o turno da turma(M/T/N/I): ")).upper()
            if turno not in ["M","T","N","I"]:
                print("Turno inserido não existe")
            else:
                ano=input("Insira o ano da turma(1-9): ")
                if int(ano) not in range(1,10):
                    print("Ano inserido não existe")
                else:
                    turmas.seek(0,0)
                    linhas=turmas.readlines()
                    idturma=1+int(linhas[-1].split(" | ")[0]) if linhas!=[] else 1   #Cria o ID para a turma

                    turmas.write(f"{idturma} | {nome} | {turno} | {ano}°\n")   #Adiociona a turma

        elif parametro.upper() == "BOLETIM":
            #pede as informações do boletim a ser inserido
            idaluno=input("Insira a matrícula do aluno a ser inserido o boletim")
            alunos.seek(0,0)
            if idaluno not in [i.split(" | ")[0] for i in alunos.readlines()]:
                print("Matrícula inserida não existe entre os alunos no sistema")
            else:
                nota1=float(input("Insira a 1° nota: "))
                nota2=float(input("Insira a 2° nota: "))
                nota3=float(input("Insira a 3° nota: "))
                nota4=float(input("Insira a 4° nota: "))
                faltas=input("Insira o n° de faltas: ")
                situ=""
                if mean([nota1,nota2,nota3,nota4])>=7 and int(faltas)<15:   #Vai atribuir a situação do aluno dependendo de suas notas e faltas
                    situ="Aprovado"
                else:
                    situ="Reprovado"

                idboletim=1+int(linhas[-1].split(" | ")[0]) if linhas!=[] else 1   #Cria o ID para o boletim  AJEITAR AQUI AAAAAAAAAAAAAAAAAAAAAAAAAA

                turmas.write(f"{idboletim} | {idaluno} | {[nota1,nota2,nota3,nota4]} | {faltas} | {situ}\n")   #Adiociona o boletim
