import sys

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'
DESENHAR = 'g'

class Compromisso: 
    def __init__(self, data:str, horaMin:str, prio:str, desc:str, ctx:str, proj:str):
      self.data = data
      self.horaMin = horaMin
      self.prio = prio
      self.desc = desc
      self.ctx = ctx
      self.proj = proj

# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(texto, cor) :
  print(cor + texto + RESET)
  

# Adiciona um compromisso aa agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais podem ser implementados como uma tupla, dicionário  ou objeto. A função
# recebe esse item através do parâmetro extras.
#
# extras tem como elementos data, hora, prioridade, contexto, projeto
#
def adicionar(itemParaAdicionar:Compromisso):

  # não é possível adicionar uma atividade que não possui descrição. 
  if itemParaAdicionar.desc  == '' :
    return False
  else:
      novaAtividade = itemParaAdicionar
  try: 
      fp = open(todo.txt, 'a')
      fp.write(novaAtividade + "\n")
  except IOError as err:
      print("Não foi possível escrever para o arquivo " + TODO_FILE)
      print(err)
      return False
  finally:
      fp.close()
  return True


# Valida a prioridade.
def prioridadeValida(pri:str):
  if len(pri) == 3:
    if pri[0] == "(" and pri[2] == ")" and ((pri[1] > "a" and pri[1] < "z") or (pri[1] > "A" and pri[1] < "Z")):
      return True
    return False
  return False

# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin:str) :
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  else:
    h = horaMin[0] + horaMin[1]
    m = horaMin[2] + horaMin[3]
    if h > "23" or m > "59":
        return False
    return True

# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto. 
def dataValida(data:str) :
  if len(data) != 8 or not soDigitos(data):
    return False
  else:
    d = data[0] + data[1]
    m = data[2] + data[3]
    a = data[4] + data[5] + data[6] + data[7]
    if m >= "01" and m <= "12":
      if (m == "01" or m == "03" or m == "05" or m == "07" or m == "08" or m == "10" or m == "12") and d <= "31":
        return True
      elif (m == "04" or m == "06" or m == "09" or m == "11") and d <= "30":
        return True
      elif (m == "02") and d <= "29":
        return True
      else:
        return False
    else:
      return False

# Valida que o string do projeto está no formato correto.
def projetoValido(proj:str):
  if len(proj) >= 2:
    if proj[0] == "+":
      return True
    return False
  return False

# Valida que o string do contexto está no formato correto. 
def contextoValido(cont:str):
  if len(cont) >= 2:
    if cont[0] == "@":
      return True
    return False
  return False

# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero:str) :
  if type(numero) != str:
    return False
  for x in numero :
    if x < '0' or x > '9':
      return False
  return True

# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de  objetos do tipo Compromisso
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.  
def organizar(linhas:str):
    itens = []

    x = 1
    for l in linhas:
        data = ''
        horaMin = ''
        prio = ''
        desc = ''
        ctx = ''
        proj = ''

        l = l.strip() #remove espaços em branco e quebras de linha do começo e do fim
        tokens = l.split() # quebra o string em palavras

        # Processa os tokens um a um, verificando se são as partes da atividade.
        # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
        # na variável data e posteriormente removido a lista de tokens. Feito isso,
        # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
        # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
        # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
        # corresponde à descrição. É só transformar a lista de tokens em um string e
        # construir a tupla com as informações disponíveis.

        i = 0
        while i < len(tokens):
            if dataValida(i) == True:
                data = data + tokens[i]
                tokens.pop(i)
                itens.append(data)
            i = i + 1

        i = 0
        while i < len(tokens):
            if horaValida(i) == True:
                horaMin = horaMin + tokens[i]
                tokens.pop(i)
                itens.append(horaMin)
            i = i + 1

        i = 0
        while i < len(tokens):
            if prioridadeValida(i) == True:
                prio = prio + tokens[i]
                tokens.pop(i)
                itens.append(prio)
            i = i + 1


        i = 0
        while i < len(tokens):
            if contextoValido(i) == True:
                ctx = ctx + tokens[i]
                tokens.pop(i)
                itens.append(ctx)
            i = i + 1

        i = 0
        while i < len(tokens):
            if projetoValido(i) == True:
                proj = proj + tokens[i]
                itens.append(proj)
                tokens.pop(i)
            i = i + 1

        for i in tokens:
            desc = desc + tokens[i]
            itens.append(desc)


        atividade[x] = (data, horaMin, prio, desc, ctx, proj)
        itens.append(atividade[x])
        # A linha abaixo inclui em itens um objeto contendo as informações relativas aos compromissos
        # nas várias linhas do arquivo.
        # itens.append(...)

    return itens

# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém. 
def listar():
    try:
        fp = open('todo.txt', 'r')
    except IOError as err:
        print("Não foi possível abrir o arquivo " + TODO_FILE)
        print(err)
        return False
    finally:
        for i in fp:
            organizar(i)
            print(itens)
        fp.close()


def ordenarPorDataHora(itens):

  ################ COMPLETAR

  return itens
   
def ordenarPorPrioridade(itens):

  ################ COMPLETAR

  return itens

def fazer(num):

  ################ COMPLETAR

  return 

def remover():

  ################ COMPLETAR

  return

# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(num, prioridade):

  ################ COMPLETAR

  return 

def desenhar(dias): 

  ################ COMPLETAR
  
  return



# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bncipal fica responsável tambémloco pri por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos.

def processarComandos(comandos):
  if comandos[1] == ADICIONAR:
    comandos.pop(0) #remove 'agenda.py'
    comandos.pop(0) #remove 'adicionar'
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    return itemParaAdicionar

  elif comandos[1] == LISTAR:
    return listar()

  elif comandos[1] == REMOVER:
    return remover()

  elif comandos[1] == FAZER:
    return    

    ################ COMPLETAR

  elif comandos[1] == PRIORIZAR:
    return    

    ################ COMPLETAR

  elif comandos[1] == DESENHAR
      desenhar()
      dias = comandos[2]
      return dias

  else :
    print("Comando inválido.")
    
  
# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
processarComandos(sys.argv)
