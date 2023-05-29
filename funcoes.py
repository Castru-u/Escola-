def cadastro(parametro):

    #Abre os arquivos a serem usados
    with open("alunos.txt", "a", encoding="utf-8") as alunos, open("turmas.txt", "a", encoding="utf-8") as turmas, open("boletins.txt", "a", encoding="utf-8") as boletins:

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

            matricula=1+alunos.readlines()

                arquivo.write(f"{matricula} | {aluno} | {email} | {telefone}")


    


