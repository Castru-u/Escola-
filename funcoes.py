from json import *
import os

#Função para retornar turno
def rturno(parametro):
    if parametro=="I":
        return "Integrado"
    elif parametro=="M":
        return "Matutino"
    elif parametro=="V":
        return "Vespertino"
    elif parametro=="N":
        return "Noturno"
    
#Função para retornar texto com os dados do aluno organizados
def raluno(matricula, dados, turmas):
    return f"""
     {matricula}        |    {dados["nome"]}
{'―'*42}
|    email    |    {dados["email"]}
|    telefone |    {dados["telefone"]}
|    turma    |    {dados["turma"]} - {turmas[dados["turma"]]["nome"]}
{'―'*42}
    """

#Função para retornar texto com os dados da turma organizados
def rturma(id, dados):
    return f"""
     {id}        |    {dados["nome"]}
{'―'*42}
|    turno    |    {rturno(dados["turno"])}
|    ano      |    {dados["ano"]}°
{'―'*42}\n
    """

#Função para retornar texto com os dados do boletim organizados
def rboletim(id, dados, media=None):
    return f"""
    Boletim     |      {id}
    Aluno       |      {dados["idaluno"]}
{'―'*42}
|   notas       |    {' '.join(map(str,dados["notas"]))}
|   média       |    {sum(dados["notas"])/4}
|   faltas      |    {dados["faltas"]}
|   situação    |    {dados["situação"]}
{'―'*42}\n\n
    """

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
    os.system('cls')
    #Abre os arquivos a serem usados
    with open('alunos.json','r+') as alunos, open('turmas.json','r+') as turmas, open('boletins.json','r+') as boletins:

        #Verificam o parametro inserido:

        if parametro.upper() == "ALUNO":
            novoalunos=load(alunos) #Cria um dicionário com o arquivo de alunos

            #Pede as informações do aluno a ser inserido
            aluno=input("Insira o nome do(a) aluno(a): ")
            email=input("Insira o email do(a) aluno(a): ")
            telefone=input("Insira o telefone do responsável do(a) aluno(a): ")
            turma=input("Insira o código de turma: ")
            
            if turma not in load(turmas):   #Verifica se o cod. de turma existe no sistema
                print("Turma inserida não existe no sistema, procure as existentes ou crie uma")
                
            else:
                matricula=1+int(list(novoalunos.keys())[-1]) if len(novoalunos)>0 else 1   #Cria o número de matrícula

                novoalunos[matricula]={"nome":aluno,"email":email,"telefone":telefone,"turma":turma} #Adiciona o novo aluno no dicionário

                alunos.seek(0,0)
                dump(novoalunos,alunos,indent=4)   #Adiciona o dicionário com o novo aluno ao arquivo
                os.system("cls")
                print("Aluno cadastrado com sucesso!\n")

        elif parametro.upper() == "TURMA":
            novaturmas=load(turmas)  #Cria um dicionário com o arquivo de turmas

            #pede as informações da turma a ser cadastrada
            nome=input("Insira o nome da turma: ")
            turno=input("Insira o turno da turma(M/V/N/I): ").upper()
            if turno not in ["M","T","N","I"]:
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
            os.system("cls")
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

                idboletim=1+int(list(novoboletins.keys())[-1]) if len(novoboletins)>0 else 1   #Cria o ID para o boletim

                novoboletins[idboletim]={"idaluno":idaluno,"notas":[nota1,nota2,nota3,nota4],"faltas":faltas,"situação":situ}   #Adiciona o novo boletim no dicionário    

                boletins.seek(0,0)
                dump(novoboletins,boletins,indent=4)   #Adiciona o dicionário com o novo boletim no arquivo
                os.system("cls")
                print("Boletim cadastrado com sucesso!\n")

        else:
            print("Parametro inserido inválido")   

#Cria a função de edição
def editar(parametro):
    verifica()

    #Abre os arquivos a serem usados
    with open('alunos.json', 'r+') as alunos, open('turmas.json', 'r+') as turmas, open('boletins.json', 'r+') as boletins:

        # Carrega os dados dos arquivos JSON
        alunos_edit = load(alunos)
        turmas_edit = load(turmas)
        boletins_edit = load(boletins)
        #Verificam o parametro inserido:

        if parametro.upper() == "ALUNO":
            matricula = input("Digite o numero de matricula do aluno a qual deseje editar algum dado\n: ")
            
            
            if matricula in alunos_edit:
                perg = input("Qual dado do aluno você deseja editar?\n").lower()
                if perg == "nome":
                    nome = input("Digite o novo nome para o(a) aluno:\n")
                    confirmacao = input(f"Tem certeza de que deseja mudar o nome do(a) aluno para '{nome}'? (s/n)\n")

                    if confirmacao.lower() == "s":
                        alunos_edit[matricula]["nome"] = nome
                        print("Nome do(a) aluno atualizado com sucesso!")
                    else:
                        print("Operação cancelada. O nome do(a) aluno não foi alterado.")
                elif perg == "email":
                    email = input("Digite o novo email para o(a) aluno:\n")
                    confirmacao = input(f"Tem certeza de que deseja mudar o email do(a) aluno para '{email}'? (s/n)\n")

                    if confirmacao.lower() == "s":
                        alunos_edit[matricula]["email"] = email
                        print("email do(a) aluno atualizado com sucesso!")
                    else:
                        print("Operação cancelada. O email do(a) aluno não foi alterado.")
                elif perg == "telefone":
                    telefone = input("Digite o novo numero de telefone para o(a) aluno:\n")
                    confirmacao = input(f"Tem certeza de que deseja mudar o telefone do(a) aluno para '{telefone}'? (s/n)\n")

                    if confirmacao.lower() == "s":
                        alunos_edit[matricula]["telefone"] = telefone
                        print("telefone do(a) aluno atualizado com sucesso!")
                    else:
                        print("Operação cancelada. O telefone do(a) aluno não foi alterado.")                       
                elif perg == "turma":
                    turma = input("Digite a nova turma para o(a) aluno:\n")
                    confirmacao = input(f"Tem certeza de que deseja mudar a turma do(a) aluno para '{turma}'? (s/n)\n")

                    if confirmacao.lower() == "s":
                        alunos_edit[matricula]["turma"] = turma
                        print("turma do(a) atualizado com sucesso!")
                    else:
                        print("Operação cancelada. a turma do(a) aluno não foi alterado.")
                
                else:
                    print("Opção inválida!")
              
            else : 
                print("Nao foi possivel achar a matricula do aluno! tente novamente")
            alunos.seek(0)  # Move o cursor para o início do arquivo
            dump(alunos_edit,alunos, indent=4)
        elif parametro.upper() == "TURMA":
            cod_turma = input("Digite o codigo da turma a qual deseje editar algum dado\n: ")
            if cod_turma in turmas_edit:
                perg = input("Qual dado da turma você deseja editar?\n").lower()
                if perg == "nome":
                    nome = input("Digite um novo nome para a turma\n: ")
                    confirmacao = input(f"Tem certeza de que deseja mudar o nome da turma para '{nome}'? (s/n)\n")

                    if confirmacao.lower() == "s":
                        turmas_edit[cod_turma]["nome"] = nome
                        print("Nome do(a) aluno atualizado com sucesso!")
                    else:
                        print("Operação cancelada. O nome da turma não foi alterado.") 
                elif perg == "turno":
                    turno=(input("Insira o novo turno para a turma\nTurnos disponiveis '(M/T/N/I)': "))
                    
                    if turno.upper() not in ["M","T","N","I"]:
                        print("Turno inserido não existe")
                    else:
                        confirmacao = input(f"Tem certeza de que deseja mudar o turno da turma para '{turno}'? (s/n)\n")

                    if confirmacao.lower() == "s":
                        turmas_edit[cod_turma]["turno"] = turno
                        print("Turno da turma atualizado com sucesso!")
                    else:
                        print("Operação cancelada. O Turno da turma não foi alterado.")

                elif perg == "ano":
                    ano=input("Insira o novo ano da turma(1-9): ")
                    if int(ano) not in range(1,10):
                        print("Ano inserido não existe")
                    else:
                        confirmacao = input(f"Tem certeza de que deseja mudar o ano da turma para '{ano}'? (s/n)\n")
                    if confirmacao.lower() == "s":
                        turmas_edit[cod_turma]["ano"] = ano
                        print("Ano da turma atualizado com sucesso!")
                    else:
                        print("Operação cancelada. O Ano da turma não foi alterado.") 
                turmas.seek(0)  # Move o cursor para o início do arquivo
                dump(turmas_edit,turmas, indent=4)
        elif parametro.upper() == "BOLETIM":
            print("Para Editar o Boletim Insira o código do mesmo")
            cod_boletim = input("Digite o Codigo do Boletim\n: ")
            opcoes = ["faltas","notas"]
            if cod_boletim in boletins_edit:
                perg = input("Qual dado do boletim voce deseja editar?\n: ").lower()
                if perg in opcoes:
                    nts = [1,2,3,4]
                    if perg == "notas":
                        nt = int(input("dentre as 4 notas do aluno qual voce deseja editar? (1°,2°,3°,4°)?\n Digite apenas o numero\n: "))
                        if nt not in nts :
                            print("Opçao invalida tente novamente !!")
                        else:
                            if nt == 1:
                                nota = float(input("Digite a nova nota\n: "))
                                
                                confirmacao = input(f"Tem certeza de que deseja mudar a nota do Boletin para '{nota}'? (s/n)\n")

                                if confirmacao.lower() == "s":
                                    boletins_edit[cod_boletim]["notas"][0]  = nota
                                    print("Nota atualizada com sucesso")
                                else:
                                    print("Operação cancelada. A nota não foi alterada.")
                            if nt == 2:
                                nota = float(input("Digite a nova nota\n: "))
                                
                                confirmacao = input(f"Tem certeza de que deseja mudar a nota do Boletin para '{nota}'? (s/n)\n")

                                if confirmacao.lower() == "s":
                                    boletins_edit[cod_boletim]["notas"][1]  = nota
                                    print("Nota atualizada com sucesso")
                                else:
                                    print("Operação cancelada. A nota não foi alterada.")    
                            if nt == 3:
                                nota = float(input("Digite a nova nota\n: "))
                                
                                confirmacao = input(f"Tem certeza de que deseja mudar a nota do Boletin para '{nota}'? (s/n)\n")

                                if confirmacao.lower() == "s":
                                    boletins_edit[cod_boletim]["notas"][2]  = nota
                                    print("Nota atualizada com sucesso")
                                else:
                                    print("Operação cancelada. A nota não foi alterada.")
                            if nt == 4:
                                nota = float(input("Digite a nova nota\n: "))
                                
                                confirmacao = input(f"Tem certeza de que deseja mudar a nota do Boletin para '{nota}'? (s/n)\n")

                                if confirmacao.lower() == "s":
                                    boletins_edit[cod_boletim]["notas"][3]  = nota
                                    print("Nota atualizada com sucesso")
                                else:
                                    print("Operação cancelada. A nota não foi alterada.")
                    if perg == "faltas":
                        print("Houve um erro na quantidade de faltas do aluno?")
                        falt = int(input("Digite a nova quantidade de faltas do aluno\n: "))
                        
                        confirmacao = input(f"Tem certeza de que deseja mudar a quantidade de faltas do aluno para '{falt}'? (s/n)\n")

                        if confirmacao.lower() == "s":
                            boletins_edit[cod_boletim]["faltas"] = falt
                            print("Quantidade de faltas atualizada com sucesso")
                        else:
                            print("Operação cancelada. A quantidade de faltas não foi alterada.")
                    if sum(boletins_edit[cod_boletim]["notas"])/4>=7 and boletins_edit[cod_boletim]["faltas"] < 15:   #Vai atribuir a situação do aluno dependendo de suas notas e faltas
                        situ="Aprovado"
                        boletins_edit[cod_boletim]["situa\u00e7\u00e3o"] = situ
                    else:
                        situ="Reprovado"
                        boletins_edit[cod_boletim]["situa\u00e7\u00e3o"] = situ              
                
                else:
                    print("A opção nao existe ou voce nao tem permissão para muda-la")
            boletins.seek(0)  # Move o cursor para o início do arquivo
            dump(boletins_edit,boletins, indent=4) 

        else:
            print("Parametro inserido inválido")   
            
#Cria a função de pesquisa
def pesquisa(parametro,item):
    verifica()
    os.system("cls")

    with open('alunos.json','r+') as alunos, open('turmas.json','r+') as turmas, open('boletins.json','r+') as boletins:

        alunos = load(alunos)
        turmas = load(turmas)
        boletins = load(boletins)

    if parametro.upper()=="ALUNO":
        
        #Caso queira achar pela matrícula
        if item=='matricula':
            matricula=input('Insira a matrícula do aluno que deseja achar\n:')    #Pede a matrícula do aluno a ser achado

            if matricula in alunos:    #Checa se a matrícula informada existe
                os.system("cls")
                for i in alunos:    #Entra na lista de alunos
                    if i==matricula:    #Verifica se a matrícula corresponde com a informada
                        dados=alunos[i]
                        print(raluno(i,dados,turmas))

            else:    #Caso não tenha nenhuma matrícula correspondente
                print("Não foi possível achar nenhum aluno com a matrícula informada")

        #Caso queira achar pelo nome (Passivo a achar mais de 1 aluno)
        elif item=='nome':
            nome=input('Insira o nome do aluno que deseja achar\n:')    #Pede o nome do aluno a ser achado

            if nome in [i["nome"] for i in alunos.values()]:    #Checa se o nome existe entre os alunos
                os.system("cls")
                print("    Aluno(s) achado(s):\n")
                for i in alunos:    #Entra na lista de alunos
                    if alunos[i]["nome"]==nome:    #Verifica se o nome corresponde com o informado
                        dados=alunos[i]
                        print(raluno(i,dados,turmas))

            else:    #Caso o nome não exista entre os alunos
                print("Não foi possível achar nenhum aluno com o nome informado")

        else:
            print("Segundo parametro inserido ininválido")

    elif parametro.upper()=="TURMA":

        #Caso queira achar pelo código de turma
        if item=="codigo":
            codigo=input("Insira o código da turma que deseja achar\n:")    #Pede o código da turma a ser procurada

            if codigo in turmas:    #Checa se o código existe entre as turmas
                os.system("cls")
                for i in turmas:    #Entra na lista de turmas
                    if i==codigo:    #Verifica se o código corresponde com o informado
                        dados=turmas[i]
                        print(rturma(i,dados))
            
            else:    #Caso não exista nenhuma turma com o código inserido
                print("Não foi possível achar nenhuma turma com o código informado")

        #Caso queira achar pelo nome da turma
        elif item=="nome":
            nome=input("Insira o nome da turma que deseja achar\n:")    #Pede o nome da turma a ser procurada

            if nome in [i["nome"] for i in turmas.values()]:    #Checa se o nome existe entre as turmas
                os.system("cls")
                print("    Turma(s) achada(s):\n")
                for i in turmas:    #Entra na lista de turmas
                    if turmas[i]["nome"]==nome:    #Verifica se o nome corresponde com o informado
                        dados=turmas[i]
                        print(rturma(i,dados))
            
            else:    #Caso não exista nenhuma turma com o nome inserido
                print("Não foi possível achar nenhuma turma com o nome informado")

        #Caso queira achar pelo turno da turma
        elif item=="turno":
            turno=input("Insira o turno da turma que deseja achar(M/V/N/I)\n:").upper()    #Pede o turno da turma a ser procurada

            if turno in [i["turno"] for i in turmas.values()]:    #Checa se o turno existe entre as turmas
                os.system("cls")
                print("    Turma(s) achada(s):\n")
                for i in turmas:    #Entra na lista de turmas
                    if turmas[i]["turno"]==turno:    #Verifica se o turno corresponde com o informado
                        dados=turmas[i]
                        print(rturma(i,dados))

            elif turno not in ["M","V","N","I"]:
                print("Turno inserido não existe no sistema ")
        
            else:    #Caso não exista nenhuma turma com o turno inserido
                print("Não foi possível achar nenhuma turma com o turno informado")

        #Caso queira achar pelo ano da turma
        elif item=="ano":
            ano=input("Insira o ano da turma que deseja achar\n:").upper()    #Pede o ano da turma a ser procurada

            if ano in [i["ano"] for i in turmas.values()]:    #Checa se o ano existe entre as turmas
                os.system("cls")
                print("    Turma(s) achada(s):\n")
                for i in turmas:    #Entra na lista de turmas
                    if turmas[i]["ano"]==ano:    #Verifica se o ano corresponde com o informado
                        dados=turmas[i]
                        print(rturma(i,dados))

            elif int(ano) not in range(1,10):    #Caso o ano inserido não exista dentro do sistema
                print("Ano inserido não existe no sistema ")
        
            else:    #Caso não exista nenhuma turma com o ano inserido
                print("Não foi possível achar nenhuma turma com o ano informado")
            
        else:
            print("Segundo parametro inserido inválido")
        
    elif parametro.upper()=="BOLETIM":
        
        #Caso queira achar pelo código do aluno
        if item=="matricula":
            matricula=input("Insira a matrícula do aluno que deseja achar o boletim\n:")

            if matricula in alunos:    #Checa se a matrícula informada existe
                os.system("cls")
                for i in boletins:    #Entra na lista de boletins
                    dados=boletins[i]
                    if matricula==dados["idaluno"]:    #Checa se a matricula do aluno corresponde com a do boletim
                        os.system("cls")
                        print(rboletim(i,dados))

            else:    #Caso não ache nenhum boletim com a matrícula
                print("Não foi possível achar nenhum boletim com a matricula informada")

        elif item=="nome":
            nome=input("Insira o nome do aluno que deseja achar o boletim\n:")

            if nome in [i["nome"] for i in alunos.values()]:    #Checa se o nome informado existe entre os alunos
                print("    Boletim(ns) achado(s):\n")
                os.system("cls")

                for i in alunos:    #Entra na lista de alunos
                    for x in boletins:    #Entra na lista de boletins
                        dados=boletins[x]
                        if alunos[i]["nome"]==nome and i==dados["idaluno"]:    #Checa se a matricula do aluno corresponde com a do boletim
                            os.system("cls")
                            print(rboletim(x,dados))

            else:    #Caso não ache nenhum boletim com o nome
                print("Não foi possível achar nenhum boletim com o nome informado")

        else:
            print("Segundo parametro inserido ininválido")
    else:
        print("Primeiro parametro inserido inválido")
        
#Cria a função de listar
def lista(parametro,parametro2=None):
    verifica()
    os.system("cls")

    with open('alunos.json','r+') as alunos, open('turmas.json','r+') as turmas, open('boletins.json','r+') as boletins:

        alunos = load(alunos)
        turmas = load(turmas)
        boletins = load(boletins)
    
    #Caso deseja listar as turmas
    if parametro.upper()=="TURMA" and parametro2==None:
        for i in turmas:
            dados=turmas[i]
            print(rturma(i,dados))

    elif parametro.upper()=="ALUNO" and parametro2.upper()=="NORMAL":
        for x in turmas:
            print(f"{'―'*42}\n    {x}  |  {turmas[x]['nome']}\n{'―'*42}")
            for i in alunos:
                dados=alunos[i]
                if dados["turma"]==x:
                    print(raluno(i,dados,turmas))

    elif parametro.upper()=="ALUNO" and parametro2.upper()=="BOLETIM":
        for x in turmas:
            print(f"{'―'*42}\n    {x}  |  {turmas[x]['nome']}\n{'―'*42}")
            for i in alunos:
                dados=alunos[i]
                if dados["turma"]==x:
                    print(raluno(i,dados,turmas))
                    for z in boletins:
                        bdados=boletins[z]
                        if bdados["idaluno"]==i:
                            print(rboletim(z,bdados,"media"))

    elif parametro.upper()=="ALUNO" and parametro2.upper()=="APROVADOS":
        for x in turmas:
            print(f"{'―'*42}\n    {x}  |  {turmas[x]['nome']}\n{'―'*42}")
            for i in alunos:
                for z in boletins:
                    dados=alunos[i]
                    bdados=boletins[z]
                    if dados["turma"]==x and bdados["idaluno"]==i and bdados["situação"]=="Aprovado":
                        print(raluno(i,dados,turmas))
                        print(rboletim(z,bdados,"media"))

    elif parametro.upper()=="ALUNO" and parametro2.upper()=="REPROVADOS":
        for x in turmas:
            print(f"{'―'*42}\n    {x}  |  {turmas[x]['nome']}\n{'―'*42}")
            for i in alunos:
                for z in boletins:
                    dados=alunos[i]
                    bdados=boletins[z]
                    if dados["turma"]==x and bdados["idaluno"]==i and bdados["situação"]=="Reprovado":
                        print(raluno(i,dados,turmas))
                        print(rboletim(z,bdados,"media"))

    else:
            print("Insira um parametro válido")
                     
 
#Cria a função remover            
def remover(parametro):
    verifica()
    #abre os arquivos
    with open('alunos.json', 'r+') as alunos, open('turmas.json', 'r+') as turmas, open('boletins.json', 'r+') as boletins:
        
        # Carrega os dados dos arquivos JSON
        lalunos= load(alunos)
        lturmas= load(turmas)
        lboletins= load(boletins)

        if parametro.upper() == 'ALUNO':    #Caso deseja ser removido um aluno

            matricula = input('Digite o número de matricula do aluno que deseja remover: ')
            
            if matricula not in lalunos:    #Caso o n° de matrícula não exista no sistema
                print('O número de matrícula digitado é inválido, tente outro.')

            else:
                nalunos={}    #Cria um novo dicionário
                for i in lalunos:
                    dados=lalunos[i]
                    if i!=matricula:
                        nalunos[i]=dados     #Adiciona todos os alunos, menos o a ser removido
                alunos.seek(0,0)
                dump(nalunos,alunos,indent=4)    #Adiciona o dicionário ao arquivo de alunos
                alunos.truncate()    #Apaga o restante do conteúdo do arquivo

                #remove o boletim do aluno
                nboletins={}    #Cria um novo dicionário
                for i in lboletins:
                    dados=lboletins[i]
                    if dados["idaluno"]!=matricula:
                        nboletins[i]=dados     #Adiciona todos os boletins, menos o do aluno
                boletins.seek(0,0)
                dump(nboletins,boletins,indent=4)    #Adiciona o dicionário ao arquivo de boletins
                boletins.truncate()    #Apaga o restante do conteúdo do arquivo

                print("Aluno removido!")

        elif parametro.upper() == 'TURMA':    #Caso deseja ser removido uma turma

            num = input('Digite o número da turma que deseja remover: ')
            
            if num not in lturmas:    #Caso o n° de turma não exista no sistema
                print('O número de turma digitado é inválido, tente outro.')

            else:
                nturmas={}    #Cria um novo dicionário
                for i in lturmas:
                    dados=lturmas[i]
                    if i!=num:
                        nturmas[i]=dados    #Adiciona todas as turmas, menos a que vai ser removida
                turmas.seek(0,0)
                dump(nturmas,turmas,indent=4)   #Adiciona o dicionário ao arquivo de turmas
                turmas.truncate()    #Apaga o restante do conteúdo do arquivo

                #Remove os alunos pertencentes a turma
                nalunos={}    #Cria um novo dicionário
                for i in lalunos:
                    dados=lalunos[i]
                    if dados["turma"]!=num:    #Caso o aluno não pertença a turma
                        nalunos[i]=dados     #Adiciona todos os alunos, menos os pertencentes a turma
                alunos.seek(0,0)
                dump(nalunos,alunos,indent=4)    #Adiciona o dicionário ao arquivo de alunos
                alunos.truncate    #Apaga o restante do conteúdo do arquivo

                print("Turma removida!")

        elif parametro.upper() == 'BOLETIM':    #Caso deseja ser removido um boletim

                boletim = input('Digite o número do boletim que deseja remover: ')
                
                if boletim not in lboletins:    #Caso o boletim não exista no sistema
                    print('O número de boletim digitado é inválido, tente outro.')

                else:
                    nboletins={}    #Cria um novo dicionário
                    for i in lboletins:
                        dados=lboletins[i]
                        if i!=boletim:
                            nboletins[i]=dados     #Adiciona todos os boletins, menos o a ser removido
                    boletins.seek(0,0)
                    dump(nboletins,boletins,indent=4)    #Adiciona o dicionário ao arquivo de boletins
                    boletins.truncate()    #Apaga o restante do conteúdo do arquivo

                    print("Boletim removido!")

        else:
            print("Insira um parametro válido")


#Cria a função de gerar relatório
def relatorio():
    verifica()
    os.system('cls')

    with open('relatorio.txt', 'w',encoding='utf-8') as relatorio, open('alunos.json','r+') as alunos, open('turmas.json','r+') as turmas, open('boletins.json','r+') as boletins:    #Abre o arquivo a ser criado o relatório e os arquivos do sistema

        # Carrega os dados dos arquivos JSON
        alunos= load(alunos)
        turmas= load(turmas)
        boletins= load(boletins)

        #Relata o total de turmas
        relatorio.write(f"""    RELATÓRIO
{'_'*42}\n
    Total de turmas : {len(turmas)}
{'_'*42}\n
        """)

        for i in turmas:    #Entra na lista de turmas
            talunos,tapro,trepro,acimalimit,abaixolimit,medias=0,0,0,0,0,[]    #Cria as variáveis para armazenar os relatórios por turma
            tdados=turmas[i]
            for x in alunos:    #Entra na lista de aluno
                dados=alunos[x]
                if dados["turma"]==i:    #Confere se o aluno pertence a turma
                    talunos+=1
                    for z in boletins:    #Entra na lista de boletins
                        bdados=boletins[z]
                        if bdados["idaluno"]==x:    #Confere se o boletim pertence ao aluno
                            if bdados["situação"]=="Aprovado":    #Se o aluno estiver aprovado
                                tapro+=1
                            elif bdados["situação"]=="Reprovado":    #Se o aluno estiver reprovado
                                trepro+=1
                            if bdados["faltas"]>=15:    #Se o aluno passar do limite de faltas
                                acimalimit+=1
                            else:    #Se o aluno estiver dentro do limite de faltas
                                abaixolimit+=1
                            medias.append(sum(bdados["notas"])/4)    #Salva a média do Aluno

            relatorio.write(f"""
    {i}  |  {tdados['nome']}    
{'='*42}
        Total de alunos : {talunos}
        Total de alunos aprovados : {tapro}
        Total de alunos reprovados : {trepro}
        Maior média : {max(medias) if len(medias)>0 else 'Nenhuma média disponível'}
        Menor média : {min(medias) if len(medias)>0 else 'Nenhuma média disponível'}
        Alunos acima do limite de falta : {acimalimit}
        Alunos abaixo do limite de falta : {abaixolimit}
            
            """)    #Escreve no arquivo o relatório dos dados da turma
    
    print("Relatório gerado.\nTente checar o arquivo 'relatório' ")

#Cria a função de menu
def menu():
    while True:
        print(f"""
{'‾'*42}\n{' '*18}ESCOLA\n{'_'*42}

    1 - Cadastrar
    2 - Editar
    3 - Remover
    4 - Pesquisar
    5 - Listar
    6 - Relatório
    7 - Créditos
    0 - Sair
{'_'*42}
""")
        r=input("")
        os.system('cls')

        if r=='1':
            prmt=input("Insira o tipo que você quer cadastrar (ALUNO/TURMA/BOLETIM)\n: ")
            cadastro(prmt)
        elif r=='2':
            prmt=input("Insira o tipo que você quer editar (ALUNO/TURMA/BOLETIM)\n: ")
            editar(prmt)
        elif r=='3':
            prmt=input("Insira o tipo que você quer remover (ALUNO/TURMA/BOLETIM)\n: ")
            remover(prmt)
        elif r=='4':
            prmt=input("""
Insira o tipo que você quer pesquisar e o item a ser usado como referência
ALUNO - (matricula/nome)
TURMA - (codigo/turno/nome/ano)
BOLETIM - (matricula/nome)
tipo: """)
            item=input("item:")
            pesquisa(prmt,item)
        elif r=='5':
            prmt=input("Insira o que você quer listar (ALUNO/TURMA)")
            if prmt.upper()=='ALUNO':
                prmt2=input("""
Deseja adicionar outra dessas opções?
NORMAL - Lista apenas os alunos
BOLETIM - Lista os alunos com os respectivos boletins
APROVADOS - Lista os alunos aprovados com os boletins
REPROVADOS - Lista os alunos reprovados com os boletins
: """)
                lista(prmt,prmt2)
            else:
                lista(prmt)
        elif r=='6':
            relatorio()
        elif r=='7':
            print("""
Integrantes:
    Amanda
    Eric
    Gustavo Medeiros
    Gustavo de Souza
    João Pedro
    Layla
    Luiz
    Noemi
    Sofia\n\n
Agradecimentos:
    Pepe Moreno
    Bruno Henrique do Flamengo
    Adam Sandler   
    Dj Azeitona
    Thorfinn Karlsefni
            """)
        elif r=='0':
            print("Hasta la vista, Baby!")
            break


