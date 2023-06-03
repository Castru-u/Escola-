from json import *
import os

#Função para verificar a existência e fazer a criação do arquivo
def verifica():
    if not os.path.exists('alunos.json'):
        with open('alunos.json', "w") as arq:
            dump({}, arq)
    if not os.path.exists('turmas.json'):
        with open('turmas.json', "w") as arq:
            dump({}, arq)
    if not os.path.exists('boletins.json'):
        with open('boletins.json', "w") as arq:
            dump({}, arq)

#Cria a função de cadastro
def cadastro(parametro):
    verifica()

    #Abre os arquivos a serem usados
    with open('alunos.json','r+') as alunos, open('turmas.json','r+') as turmas, open('boletins.json','r+') as boletins:

        #Verificam o parametro inserido:

        if parametro.upper() == "ALUNO":
            novoalunos=load(alunos) #Cria um dicionário com o arquivo de alunos

            #Pede as informações do aluno a ser inserido
            aluno=input("Insira o nome do(a) aluno(a): ")
            email=input("Insira o email do(a) aluno(a): ")
            telefone=int(input("Insira o telefone do responsável do(a) aluno(a): "))
            turma=input("Insira o código de turma: ")
            
            if turma not in load(turmas):   #Verifica se o cod. de turma existe no sistema
                print("Turma inserida não existe no sistema, procure as existentes ou crie uma")
                
            else:
                matricula=1+list(novoalunos.keys())[-1] if len(novoalunos)>0 else 1   #Cria o número de matrícula

                novoalunos[matricula]={"nome":aluno,"email":email,"telefone":telefone,"turma":turma} #Adiciona o novo aluno no dicionário

                alunos.seek(0,0)
                dump(novoalunos,alunos,indent=4)   #Adiciona o dicionário com o novo aluno ao arquivo
                os.system("cls")
                print("Aluno cadastrado com sucesso!\n")

        elif parametro.upper() == "TURMA":
            novaturmas=load(turmas)  #Cria um dicionário com o arquivo de turmas

            #pede as informações da turma a ser cadastrada
            nome=input("Insira o nome da turma: ")
            turno=(input("Insira o turno da turma(M/T/N/I): "))
            if turno.upper() not in ["M","T","N","I"]:
                print("Turno inserido não existe")
            else:
                ano=input("Insira o ano da turma(1-9): ")
                if int(ano) not in range(1,10):
                    print("Ano inserido não existe")
                else:
                    idturma=str(1+int(list(novaturmas.keys())[-1])) if len(novaturmas)>0 else "1"      #Cria o ID para a turma

                    novaturmas[idturma]={"nome":nome,"turno":turno,"ano":ano}   #Adiciona a nova turma no dicionário    

                    turmas.seek(0,0)
                    dump(novaturmas,turmas,indent=4)   #Adiciona o dicionário com a nova turma no arquivo
                    os.system("cls")
                    print("Turma cadastrada com sucesso!\n")

        elif parametro.upper() == "BOLETIM":
            novoboletins=load(boletins)    #Cria um dicionário com o arquivo de boletins

            #pede as informações do boletim a ser inserido
            idaluno=input("Insira a matrícula do aluno a ser inserido o boletim")

            if idaluno not in load(alunos):
                print("Matrícula inserida não existe entre os alunos no sistema")
            elif idaluno in [i["idaluno"] for i in novoboletins.values()]:
                print("Matrícula inserida já existe nos boletins cadastrados. Tente usar a função 'editar()'")
            else:
                nota1=float(input("Insira a 1° nota: "))
                nota2=float(input("Insira a 2° nota: "))
                nota3=float(input("Insira a 3° nota: "))
                nota4=float(input("Insira a 4° nota: "))
                faltas=int(input("Insira o n° de faltas: "))
                situ=""
                if sum([nota1,nota2,nota3,nota4])/4>=7 and faltas<15:   #Vai atribuir a situação do aluno dependendo de suas notas e faltas
                    situ="Aprovado"
                else:
                    situ="Reprovado"

                idboletim=1+list(novoboletins.keys())[-1] if len(novoboletins)>0 else 1   #Cria o ID para o boletim

                novoboletins[idboletim]={"idaluno":idaluno,"notas":[nota1,nota2,nota3,nota4],"faltas":faltas,"situação":situ}   #Adiciona o novo boletim no dicionário    

                boletins.seek(0,0)
                dump(novoboletins,boletins,indent=4)   #Adiciona o dicionário com o novo boletim no arquivo
                os.system("cls")
                print("Boletim cadastrado com sucesso!\n")

        else:
            #Caso não seja informado um dos parametros acima
            print("Parametro não informado (ALUNO/TURMA/BOLETIM)")




        
