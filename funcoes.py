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


    


