import random

alfabeto = "abcdefghi"
nome_um = "\N{White Circle}"
nome_dois = "\N{Black Circle}"

#D = {'tamanho':3, 'jogadas':{'1ab','12a','23c','3bc'}, nome_um:set(), nome_dois:set()}

#Observações rápidas:
#Tentei escrever as docstrings de forma que uma pessoa que sequer tenha visto o pdf,
#mas saiba o que é e como funciona o Dot and Boxes, consiga usar as funções sem problemas.

#A maioria dos asserts me parecem desncessários, pois as funções não tendem a ser
#usadas separadamente. De qualquer forma, coloquei assert ao menos nos tipos de entrada,
#e expliquei nas docstrings que, caso a função seja usada separadamente, é importante
#tomar cuidado para inserir entradas válidas e na formatação correta.

#Sobre os testes, eu de fato ainda não entendi como fazer testes eficientes, então fiz o que consegui.

#No mais, achei bem divertido elaborar uma parte do jogo e principalmente os jogadores.
#Agradeço pelo tempo investido na elaboração de uma avaliação legal e útil(em diversos sentidos).
 
#Q1
def cria_jogo(tamanho):
    """Função que recebe o tamanho de um tabuleiro(no mínimo 2, e no máximo 9)
    de um jogo de Dot and Boxes e cria um dicionário que representa o 
    tabuleiro do jogo sem nenhuma jogada efetuada."""
    assert type(tamanho) == int , "O tipo de entrada é incorreto."
    if tamanho < 2 or tamanho > 9:
        return "Tamanho de tabuleiro inválido."
    return {'tamanho':tamanho, 'jogadas':set(), nome_um:set(), nome_dois:set()}       

#Q2
def jogadas_válidas(jogo):
    """Função que recebe um dicionário de jogo válido e retorna o conjunto
    contendo exatamente as jogadas válidas naquele jogo.
    Nesse caso, as jogadas são representadas por strings de tamanho 3,
    contendo números em ordem crescente e letras em ordem alfabética, 
    nessa ordem. Por exemplo, a jogada que representa a aresta vertical 
    esquerda num jogo de tamanho 2x2 é dada pela string '12a', sendo qualquer
    outra combinação desses 3 símbolos inválida. Isso é importante pois 
    garante que não teremos 2 strings com mesmos símbolos que possam 
    potenciamente representar duas jogadas distintas.
    Dict --> Conjunto"""
    assert type(jogo) == dict , "O tipo de entrada é incorreto."
    possivel = set()
    for coluna in alfabeto[:jogo['tamanho']]:
        for linha in range(1,jogo['tamanho']):
            possivel.add(f'{linha}{linha+1}{coluna}') #jogadas verticais
    for linha in range(1,jogo['tamanho']+1):
        contador = 1
        for coluna in alfabeto[:jogo['tamanho']-1]:
            prox_col = alfabeto[contador]
            possivel.add(f'{linha}{coluna}{prox_col}') #jogadas horizontais
            contador += 1
    ja_feitas = jogo['jogadas'] #tiramos jogadas já feitas
    return possivel.difference(ja_feitas)

def teste_jogadas_válidas():
    """Função de teste da função jogadas_válidas"""
    assert jogadas_válidas({'tamanho': 3, 'jogadas': {'12a', '1ab', '23c', '3bc'}, '○': set(), '●': set()}) == {'12b','12c','23a','23b','2ab','3ab','1bc','2bc'}

#Q3
def arestas_do_quadrado(quadrado):
    """Função que que recebe uma string representando um quadrado
    e retorna um conjunto contendo exatamente as strings que 
    representam as 4 arestas que formam aquele quadrado.
    Nesse caso, quadrados são representados por um string de comprimento 2,
    sendo ela composta por 1 número e 1 letra, nessa ordem, as quais 
    representam o vértice inferior direito do quadrado. Por exemplo, o único
    quadrado em um jogo de tamanho 2x2 é representado pela string '1b', sendo
    'b1' considerada como entrada incorreta.
    String --> Lista"""
    assert type(quadrado) == str , "O tipo de entrada é incorreto."
    assert len(quadrado) == 2 , "Esse quadrado não existe."
    #Vamos verificar se o quadrado inserido existe
    números = '12345678'
    if quadrado[0] not in números or quadrado[1] not in alfabeto[1:]:
        return "Esse quadrado não existe."
    quadrado_arestas = []
    for coluna in alfabeto[alfabeto.index(quadrado[1])-1:alfabeto.index(quadrado[1])+1]: #arestas verticais
        quadrado_arestas.append(f'{quadrado[0]}{int(quadrado[0])+1}{coluna}')
    for linha in range(int(quadrado[0]),int(quadrado[0])+2):
        quadrado_arestas.append(f'{linha}{alfabeto[alfabeto.index(quadrado[1])-1]}{quadrado[1]}') #arestas horizontais
    return quadrado_arestas

#reconheço que alfabeto[alfabeto.index] foi péssimo

def teste_arestas_do_quadrado():
    """Função de teste da função arestas_do_quadrado."""
    assert arestas_do_quadrado('3b') == ['34a','34b','3ab','4ab']

#Q4
def quadrados_contendo(aresta, tamanho):
    """Função que recebe como entrada uma string representando uma 
    aresta e um inteiro que determina o tamanho do lado da malha,
    e retorna uma lista contendo exatamente as strings representando
    os quadrados da malha que contêm aquela aresta. Como essa função é
    utilizada em conjunto com outras na função 'jogar', não há verificação
    na validade das entradas, o que pode ocasionar problemas
    caso ela seja utilizada de forma separada. Portanto, para seu
    funcionamento correto, é obrigatório que o tamanho esteja entre 2 e 9,
    e a aresta tenha formatação correta e exista em um tabuleiro do 
    tamanho indicado. String, int --> Lista"""
    assert type(aresta) == str , "O tipo de entrada é incorreto."
    assert type(tamanho) == int , "O tipo de entrada é incorreto."
    #Entradas de tamanho válidas estão sendo controladas pela 'cria_jogo'
    #Arestas válidas estão sendo controladas pela 'jogadas_válidas'
    if aresta[1] in alfabeto: #Arestas horizontais
        if aresta[0] == '1': #Se for uma aresta lateral da borda inferior
            return [f'1{aresta[2]}']
        elif aresta[0] == f'{tamanho}': #Se for uma aresta lateral da borda superior
            return [f'{int(aresta[0])-1}{aresta[2]}']
        else: #Qualquer outra fará parte de 2 quadrados
            return [f'{aresta[0]}{aresta[2]}',f'{int(aresta[0])-1}{aresta[2]}']
    else:
        if aresta[2] == 'a': #Se for uma aresta vertical da primeira coluna
            return [f'{aresta[0]}b'] 
        elif aresta[2] == alfabeto[tamanho - 1]: #Se for uma aresta vertical da última coluna
            return [f'{aresta[0]}{aresta[2]}']
        else: #qualquer outra fará parte de 2 quadrados
            return [f'{aresta[0]}{aresta[2]}',f'{aresta[0]}{alfabeto[alfabeto.index(aresta[2]) + 1]}']

def teste_quadrados_contendo():
    """Função de teste da função quadrados_contendo."""
    assert quadrados_contendo('3bc',5) == ['3c','2c']
    assert quadrados_contendo('45a',6) == ['4b']

#Q5
def quadrados_capturados(jogada, jogo): 
    """Função que recebe uma string representando uma jogada e
    um dicionário de jogo, e retorna uma lista contendo exatamente 
    as strings que representam os quadrados daquele jogo que foram
    capturados por aquela jogada, assumindo que a jogada tenha sido 
    a última a ser realizada naquele jogo, desde que o jogo seja válido.
    Caso seja usada de forma separada da função 'jogar', é essencial que
    a jogada fornecida seja válida e no formato correto (números em ordem
    crescente seguidos de letras em ordem alfabética).
    String, Dic --> Lista"""
    assert type(jogada) == str , "O tipo de entrada é incorreto."
    
    #Outras funções estão controlando a validade das entradas
    quadrados_possiveis = quadrados_contendo(jogada,jogo['tamanho']) #Quadrados que podem ser capturados pois são compostos pela string jogada
    if len(quadrados_possiveis) == 1: #Se há apenas 1 quadrado possível
        auxiliar = arestas_do_quadrado(quadrados_possiveis[0]) #Vamos verificar se suas arestas todas foram jogadas
        for aresta in auxiliar:
            if aresta not in jogo['jogadas']: #Se não foram
                return [] #Então o quadrado não é capturado
        return quadrados_contendo(jogada,jogo['tamanho']) #Caso contrário, capturamos
    else:
        cont1 = 0
        cont2 = 0
        auxiliar = arestas_do_quadrado(quadrados_possiveis[0]) + arestas_do_quadrado(quadrados_possiveis[1]) #Agora vamos verificar 2 quadrados, 1 de cada vez
        for aresta in auxiliar[:4]: #Vamos ver se o primeiro quadrado será capturado
            if cont1 == 0: #Se ainda n removemos
                if aresta not in jogo['jogadas']: #Caso alguma aresta do quadrado ainda não tenha sido jogada
                    quadrados_possiveis.remove(quadrados_possiveis[0]) #Esse quadrado não será capturado, portanto remova das possibilidades
                    cont1 += 1 #Agora que já removemos, vamos olhar o outro
        for aresta in auxiliar[4:]: #Vamos ver se o segundo quadrado será capturado
            if cont2 == 0: #Se ainda n removemos
                if aresta not in jogo['jogadas']: #Caso alguma aresta do quadrado ainda não tenha sido jogada
                    if len(quadrados_possiveis) == 2: #Se não removemos o outro quadrado
                        quadrados_possiveis.remove(quadrados_possiveis[1]) #Então temos que remover a segunda string
                        cont2 += 1 #Removido
                    else: #Caso tivermos removido o primeiro também
                        quadrados_possiveis.remove(quadrados_possiveis[0]) #Agora só há um termo na string
                        cont2 += 1 #Removido
    return quadrados_possiveis #Retorna a(s) string(s) do(s) quadrado(s) que sobrou/sobraram

#D_linha = {'tamanho': 3, 'jogadas': {'12a', '23b', '23c', '3bc'}, '○': set(), '●': set()}

def teste_quadrados_capturados():
    """Função de teste da função quadrados_capturados."""
    assert quadrados_capturados('23a',{'tamanho': 3, 'jogadas': {'12a', '1ab', '23a', '3bc'}, '○': set(), '●': set()}) == []
    assert quadrados_capturados('2bc',{'tamanho': 3, 'jogadas': {'12a', '23b', '23c','2bc','3bc'}, '○': set(), '●': set()}) == ['2c']

#Q6            
def jogo_acabou(jogo):
    """Função que recebe um dicionário de jogo e determina se o jogo
     acabou. Retorna False caso o jogo não tenha acabado, a string
    'empate' caso o jogo tenha acabado em empate ou a string contendo
     o nome do vencedor, caso haja algum. A validade da entrada é controlada
     pela função 'jogar', então caso desejar utilizar essa função separadamente,
     é necessário se atentar a fornecer um dicionário com todas as jogadas
     feitas(seguindo a formatação correta) e fornecer as strings que
     representam os quadrados já capturados por cada jogador."""
    assert type(jogo) == dict , "O tipo de entrada é incorreto."
    #A validade da entrada é controlada por outras funções
    N = jogo['tamanho']
    vitória = ((N-1)**2//2) + 1 #Número de quadrados totais + 1
    if len(jogo[nome_um]) >= vitória:
        return nome_um
    elif len(jogo[nome_dois]) >= vitória:
        return nome_dois
    elif len(jogo[nome_um]) == len(jogo[nome_dois]) and len(jogo['jogadas']) == 2*N*(N-1):
        return 'empate'
    else:
        return False

def teste_jogo_acabou():
    """Função de teste da função jogo_acabou."""
    assert jogo_acabou({'tamanho': 3, 'jogadas': set(), nome_um: {'1b','2b','1c'}, nome_dois: set()}) == nome_um
    assert jogo_acabou({'tamanho': 3, 'jogadas': set(), nome_um: set(), nome_dois:{'1b','2b','1c'}}) == nome_dois
    assert jogo_acabou({'tamanho': 3, 'jogadas': {'12a','12b','12c','1ab','1bc','23a','23b','23c','2ab','2bc','3ab','3bc'}, nome_um: {'2c','1c'}, nome_dois:{'1b','2b'}}) == 'empate'
    assert jogo_acabou({'tamanho': 3, 'jogadas': set(), nome_um: set(), nome_dois:{'1b'}}) == False                          

#Q7
def jogador_humano(jogo,vez):
    """Função que recebe duas entradas: o dicionário de jogo e
    uma string que indica se o jogador é o primeiro ou o segundo no
    jogo. A função retorna a jogada do ser humano sentado 
    ao computador, mesmo que a entrada seja digitada fora da ordem 
    estabelecida como padrão(números em ordem crescente primeiro,
    seguidos por letras em ordem alfabética)."""
    assert type(jogo) == dict , "O tipo de entrada é incorreto."
    #Não há muito como usar essa função separadamente, por isso não sei bem se esse assert é útil
    #A validade das entradas é controlada pela função 'jogar' no geral
    while True:
        jogada = str(input('Digite a jogada: '))  
        arrumada = []
        for elemento in jogada:
            arrumada.append(elemento)
        arrumada.sort() #Arrumamos a ordenação, mas está numa lista
        certo = ''
        for elemento in arrumada:
            certo += elemento #Convertendo pra string
        if certo in jogadas_válidas(jogo): #Verificamos se a jogada escolhida é válida
            break #Se for, OK!
        else: #Se não for, avise isso
            print('Essa jogada é inválida, ou já foi feita, tente novamente!')
    return certo  

#Não temos muito bem como fazer testes já que a função recebe uma variável via input.
#Testes foram feitos utilizando a função no modo 'jogar'.                 
    
#Q8
def jogador_aleatório(jogo,vez):
    """Função que representa um jogador aleatório, que escolhe uma jogada
    válida aleatoriamente."""
    assert type(jogo) == dict , "O tipo de entrada é incorreto."
    #Novamente, não sei bem se esse assert é necessário
    jogada = random.sample(jogadas_válidas(jogo),1)
    return jogada[0]

#Não podemos fazer testes pois a variável é aleatória.

#Q9
def Guratonii(jogo,vez):
    """Jogador que implementa a chamada “estratégia gulosa”: caso
    haja quadrados a serem capturados no jogo, ele faz uma das jogadas
    que capture o máximo possível de quadrados, sendo essa uma aleatória dentre
    as encontradas. Caso não haja nenhuma jogada que capture quadrados, ele
    realiza qualquer uma disponível."""
    assert type(jogo) == dict , "O tipo de entrada é incorreto."
    #Novamente, não sei bem se esse assert é necessário
    cache = {1:[]}
    for jogada in jogadas_válidas(jogo):
        jogo['jogadas'].add(jogada)
        if len(quadrados_capturados(jogada,jogo)) == 2:
            jogo['jogadas'].remove(jogada)
            return jogada #Se caimos nesse if, então esse é o máximo de quadrados que podemos capturar com 1 jogada
        elif len(quadrados_capturados(jogada,jogo)) == 1:
            cache[1].append(jogada) #Ainda pode ter outra jogada que capture 2 quadrados
        jogo['jogadas'].remove(jogada)   #Retiramos a jogada hipotética
        
    if len(cache[1]) != 0: #Se chegamos aqui, não temos jogadas que capture dois quadrados, então faça a primeira que capture 1 quadrado se houver
        return random.choice(cache[1]) #Podemos usar choice pois temos uma lista
    qualquer = random.sample(jogadas_válidas(jogo),1) #Se chegamos aqui, não temos jogadas que capturem quadrados, então faça uma qualquer disponível
    return qualquer[0]

#Difícil fazer testes pois existem muitos elementos imprevisiveis,
#a exemplo do random.choice e random.sample .
 
#Q10
  
#OBS : Vou explicar o objetivo de cada chave no cache da função a seguir
#4 : você captura 2 quadrados e mais 2 na rodada seguinte
#3 : você captura 2 quadrados e mais 1 na rodada seguinte
#1.1 : você captura 1 quadrado e mais 1 na rodada seguinte
#2 : você captura 2 quadrados e nenhum na rodada seguinte
#1 : você captura 1 quadrado e nenhum na rodada seguinte
#0 : você não captura nenhum quadrado e o oponente também não
#0.1 : você não captura nenhum quadrado e o oponente captura 1 na seguinte, porém nenhum na depois dessa
#0.11 : você não captura nenhum quadrado e o oponente captura 1 na seguinte, e ainda ao menos 1 na depois dessa
#0.2 : você não captura nenhum quadrado e o oponente também não
   
def Shikamaru(jogo,vez):
    """Jogador que usa uma estratégia que tenta maximizar os quadrados capturados
    e tenta impedir que o oponente capture muitos, caso não seja possível
    evitar que ele capture ao menos 1. Cuidado ao usar na função torneio,
    já que muitos jogos com tabuleiros de 9x9 e contra outros jogadores
    que também utilizam estratégias mais elaboradas podem demorar muito."""
    cache = {4:[], 3:[], 1.1:[], 2:[], 1:[], 0:[], 0.1:[], 0.2:[]} #Cache para salvarmos nossas possiblidades em ordem decrescente da melhor para a pior
    jogada_random = random.sample(jogadas_válidas(jogo),1) 
    jogada = jogada_random[0] #Essa jogada serve apenas pra conferir se é a última, importante para evitar erros
    jogo['jogadas'].add(jogada)
    if len(jogadas_válidas(jogo)) == 0: #Se o jogo ainda não estiver perdido e essa for a unica jogada disponível, ganharemos o jogo com ela
        jogo['jogadas'].remove(jogada)
        return jogada
    else:
        jogo['jogadas'].remove(jogada)
        for jogada1 in jogadas_válidas(jogo): #Vamos verificar algumas ou todas as jogadas disponíveis
            jogo['jogadas'].add(jogada1)
            proxima = Guratonii(jogo,vez) #Uma das jogadas seguinte que captura mais quadrados
            if len(quadrados_capturados(jogada1,jogo)) != 0: #Caso capturemos 1 ou mais quadrados
                if len(quadrados_capturados(jogada1,jogo)) == 2: #Se capturarmos 2 quadrados com a jogada
                    jogo['jogadas'].add(proxima) #Agora vamos verificar nossa proxima jogada
                    if len(quadrados_capturados(proxima,jogo)) == 2: #Quer dizer que podemos capturar 2 quadrados na proxima rodada
                        cache[4].append(jogada1) #Salve essa jogada como a potencialmente melhor
                    elif len(quadrados_capturados(proxima,jogo)) == 1: #Quer dizer que podemos capturar 1 quadrado na proxima rodada
                        cache[3].append(jogada1)
                    else: #Da pra tentar verificar duas jogadas a frente pra ver se o oponente captura muita coisa, mas como não consegui arquitetar uma recursão decente ficaria com muito if
                        cache[2].append(jogada1)
                    jogo['jogadas'].remove(proxima) #Lembrar de remover essa jogada hipotética do jogo
                else:
                    jogo['jogadas'].add(proxima) #Agora vamos verificar nossa proxima jogada
                    if len(quadrados_capturados(proxima,jogo)) == 2: #Quer dizer que podemos capturar 2 quadrados na proxima rodada                    
                        cache[3].append(jogada1)
                    elif len(quadrados_capturados(proxima,jogo)) == 1:
                        cache[1.1].append(jogada1) #Essa jogada é melhor que a do cache[2] pois teremos 2 turnos seguidos de captura (eu penso que seja melhor)
                    else: #Da pra tentar verificar duas jogadas a frente pra ver se o oponente captura muita coisa, mas como não consegui arquitetar uma recursão decente ficaria com muito if
                        cache[1].append(jogada1)
                    jogo['jogadas'].remove(proxima) #Lembrar de remover essa jogada hipotética do jogo
                
            else: #Caso não pudermos capturar nenhum quadrado, vamos ver se a jogada permite que o oponente capture algum
                possivel = quadrados_contendo(jogada1,jogo['tamanho']) #Quadrados que possuem aquela aresta
                contador = 0
                for quadrado in possivel:                    
                    arestas_q = set(arestas_do_quadrado(quadrado))
                    if len(jogo['jogadas'].intersection(arestas_q)) <= 2: #Quer dizer que ainda tem mais de 2 arestas do quadrado atual disponíveis
                        contador += 1
                    else:
                        continue
                if contador == len(possivel): #Caso todos os quadrados ainda tenham mais de 2 arestas disponíveis, pelo menos o oponente não captura nada                  
                    cache[0].append(jogada1)
                #Caso o jogador seguinte possa capturar um quadrado com nossa jogada atual, vamos tentar outra e salvar as potencialmente menos piores(aqui eu considerei apenas quadrados capturados imediatamente depois do turno atual)
                elif contador == 1:                    
                    cache[0.1].append(jogada1) 
                else: #Esse é o pior caso possível(na verdade, às vezes é até o melhor, mas pra essa estratégia seria o pior), mas existe a remota possibilidade de acontecer como obrigatório, então achei melhor inserir                  
                    cache[0.2].append(jogada1)                    
            jogo['jogadas'].remove(jogada1) #Lembrar de remover a jogada hipotética
        
        for chave in cache: #Como o cache está organizado em ordem decrescente de melhores jogadas, basta percorrer as chaves até que apareça alguma que tenha jogada disponível
            if len(cache[chave]) != 0:
                return cache[chave][0] #Essa será nossa a melhor jogada da nossa estratégia (não sei se isso é bem uma estratégia, mas é melhor que o Guratonii)

#OBS : Ao testar algumas vezes na função torneio, vi que ela demora bastante pra ser executada, principalmente contra o Guratonii
#Testando apenas um jogo de 9x9 entre ele e o Guratonii, parece que o jogador de fato demora menos de 2 segundos pra fazer a jogada
#Eu penso em algumas melhorias possíveis, principalmente no caso em que não podemos capturar quadrados e o oponente captura no mínimo 1,
#sendo ideal verificar se ele captura apenas 1 ou fecha uma long chain e ganha o jogo. Isso reduziria bastante a possibilidade de derrota creio eu.
#Porém, dado que a função está bem ineficiente, acho que colocar isso a deixaria ainda pior, então vou fazer essa versão abaixo

#Q10 versão2

#Nova chave + mudança na 0.1

#0.1 : você não captura nenhum quadrado e o oponente captura 1 na seguinte, porém nenhum na rodada depois da seguinte
#0.11 : você não captura nenhum quadrado e o oponente captura 1 na seguinte, e ainda ao menos 1 na rodada depois da seguinte

def Shikaku(jogo,vez):
    """Jogador que usa uma estratégia que tenta maximizar os quadrados capturados
    e tenta impedir que o oponente capture muitos, caso não seja possível
    evitar que ele capture ao menos 1. Cuidado ao usar na função torneio,
    já que muitos jogos com tabuleiros de 9x9 e contra outros jogadores
    que também utilizam estratégias mais elaboradas podem demorar muito."""
    cache = {4:[], 3:[], 1.1:[], 2:[], 1:[], 0:[], 0.1:[], 0.11:[], 0.2:[]} #adicionamos 0.11 que representa que o oponente capturou um quadrado na jogada seguinte e pelo menos 1 na depois dessa
    jogada_random = random.sample(jogadas_válidas(jogo),1) 
    jogada = jogada_random[0] #Essa jogada serve apenas pra conferir se é a última, importante para evitar erros
    jogo['jogadas'].add(jogada)
    if len(jogadas_válidas(jogo)) == 0: #Se o jogo ainda não estiver perdido e essa for a unica jogada disponível, ganharemos o jogo com ela
        jogo['jogadas'].remove(jogada)
        return jogada
    else:
        jogo['jogadas'].remove(jogada)
        for jogada1 in jogadas_válidas(jogo): #Vamos verificar algumas ou todas as jogadas disponíveis
            jogo['jogadas'].add(jogada1)
            proxima = Guratonii(jogo,vez) #Uma das jogadas seguinte que captura mais quadrados
            if len(quadrados_capturados(jogada1,jogo)) != 0: #Caso capturemos 1 ou mais quadrados
                if len(quadrados_capturados(jogada1,jogo)) == 2: #Se capturarmos 2 quadrados com a jogada
                    jogo['jogadas'].add(proxima) #Agora vamos verificar nossa proxima jogada
                    if len(quadrados_capturados(proxima,jogo)) == 2: #Quer dizer que podemos capturar 2 quadrados na proxima rodada
                        cache[4].append(jogada1) #Salve essa jogada como a potencialmente melhor
                    elif len(quadrados_capturados(proxima,jogo)) == 1: #Quer dizer que podemos capturar 1 quadrado na proxima rodada
                        cache[3].append(jogada1)
                    else: #Da pra tentar verificar duas jogadas a frente pra ver se o oponente captura muita coisa, mas como não consegui arquitetar uma recursão decente ficaria com muito if
                        cache[2].append(jogada1)
                    jogo['jogadas'].remove(proxima) #Lembrar de remover essa jogada hipotética do jogo
                else:
                    jogo['jogadas'].add(proxima) #Agora vamos verificar nossa proxima jogada
                    if len(quadrados_capturados(proxima,jogo)) == 2: #Quer dizer que podemos capturar 2 quadrados na proxima rodada                    
                        cache[3].append(jogada1)
                    elif len(quadrados_capturados(proxima,jogo)) == 1:
                        cache[1.1].append(jogada1) #Essa jogada é melhor que a do cache[2] pois teremos 2 turnos seguidos de captura (eu penso que seja melhor)
                    else: #Da pra tentar verificar duas jogadas a frente pra ver se o oponente captura muita coisa, mas como não consegui arquitetar uma recursão decente ficaria com muito if
                        cache[1].append(jogada1)
                    jogo['jogadas'].remove(proxima) #Lembrar de remover essa jogada hipotética do jogo
                
            else: #Caso não pudermos capturar nenhum quadrado, vamos ver se a jogada permite que o oponente capture algum
                possivel = quadrados_contendo(jogada1,jogo['tamanho']) #Quadrados que possuem aquela aresta
                contador = 0
                for quadrado in possivel:                    
                    arestas_q = set(arestas_do_quadrado(quadrado))
                    if len(jogo['jogadas'].intersection(arestas_q)) <= 2: #Quer dizer que ainda tem mais de 2 arestas do quadrado atual disponíveis
                        contador += 1
                    else:
                        continue
                if contador == len(possivel): #Caso todos os quadrados ainda tenham mais de 2 arestas disponíveis, pelo menos o oponente não captura nada                  
                    cache[0].append(jogada1)
                #Caso o jogador seguinte possa capturar um quadrado com nossa jogada atual, vamos tentar outra e salvar as potencialmente menos piores(aqui eu considerei apenas quadrados capturados imediatamente depois do turno atual)
                elif contador == 1: #1 podemos conferir se o oponente pode capturar quadrados em 2 rodadas seguidas ou não                   
                    prox_prox = Guratonii(jogo,vez) #Vamos ver qual a jogada que mais captura quadrados
                    jogo['jogadas'].add(prox_prox)
                    if len(quadrados_capturados(prox_prox,jogo)) == 0: #Nesse caso, apesar do oponente capturar 1 quadrado na proxima, na seguinte ele não captura nada
                        cache[0.1].append(jogada1)
                    else: #Aqui realmente não tem jeito, perderemos quadrados em 2 rodadas seguidas
                        cache[0.11].append(jogada1)
                    jogo['jogadas'].remove(prox_prox)
                else: #Esse é o pior caso possível(na verdade, às vezes é até o melhor, mas pra essa estratégia seria o pior), mas existe a remota possibilidade de acontecer como obrigatório, então achei melhor inserir                  
                    cache[0.2].append(jogada1)                    
            jogo['jogadas'].remove(jogada1) #Lembrar de remover a jogada hipotética
        
        for chave in cache: #Como o cache está organizado em ordem decrescente de melhores jogadas, basta percorrer as chaves até que apareça alguma que tenha jogada disponível
            if len(cache[chave]) != 0:
                return cache[chave][0] #Essa será nossa a melhor jogada da nossa estratégia (não sei se isso é bem uma estratégia, mas é melhor que o Guratonii)

#No final de contas, nos torneios entre esses dois jogadores, o resultado é em torno de 50% de vitórias para cada um(mais ou menos esperado).
#Essa mudança funciona melhor contra jogadores humanos e em situações específicas(em geral em tabuleiros menores).
#Minha métrica foi que meus amigos perderam mais para o Shikaku do que pro Shikamaru, então achei que valia a pena fazer 2 versões.

#Não consegui nada satisfatório para os desafios, mas eu me interessei bastante e vou
#continuar tentando nas férias.

#####################################
####### Funções prontas (não editar):
#####################################

def mostra(jogo):
    """
    Imprime na tela uma representação gráfica da situação atual do jogo de Dots and Boxes
    """
    p = "\N{Middle Dot}"
    h = "\N{Horizontal Bar}"*3
    v = "\N{Vertical Line}"
    
    s = '\n'
    tamanho = jogo['tamanho']
    for i in range(tamanho):
        # imprimir arestas horizontais na linha de rótulo tamanho-i
        s += f"{tamanho-i:<{1+len(str(tamanho))}}"
        s += p
        for j in range(tamanho-1):
            letra_atual = alfabeto[j]
            próxima_letra = alfabeto[j+1]
            if f"{tamanho-i}{letra_atual}{próxima_letra}" in jogo['jogadas']:
                s += h
            else:
                s += ' '*len(h)
            s += p
        s += '\n'
        
        # imprimir arestas verticais entre linhas tamanho-i e tamanho-i-1
        s += ' '*(1+len(str(tamanho)))
        if i < tamanho-1:
            for j,letra in enumerate(alfabeto[:tamanho]):
                if j > 0:
                    if f"{tamanho-i-1}{letra}" in jogo[nome_um]:
                        s += f' {nome_um} '
                    elif f"{tamanho-i-1}{letra}" in jogo[nome_dois]:
                        s += f' {nome_dois} '
                    else:
                        s += ' '*len(h)
                        
                if f"{tamanho-i-1}{tamanho-i}{letra}" in jogo['jogadas']:
                    s += v
                else:
                    s += ' '
            s += '\n'
        else:
            for letra in alfabeto[:tamanho-1]:
                s += letra
                s += ' '*len(h)
            s += alfabeto[tamanho-1]

    print(s)

def outro(vez):
    "Retorna o nome do _outro_ jogador"
    if vez == nome_um:
        return nome_dois
    return nome_um


def jogar(primeiro, segundo, tamanho=4, interativo=True):
    """
    Roda um jogo de Dots and Boxes entre os jogadores  primeiro
    e  segundo , em uma malha de lado  tamanho.
    Se  interativo  for True, o estado do jogo é exibido a cada
    rodada, e o resultado é impresso na tela (sem retorno).
    Se  interativo  for False, nada é exibido na tela, e o resultado
    do jogo é retornado pela função (o vencedor, caso haja, ou a
    string 'empate')
    """
    
    J = cria_jogo(tamanho)
    vez = nome_um
    
    # Loop principal do jogo: mostra o jogo na tela e pede a próxima jogada do jogador da vez.
    while True:
        if interativo:
            mostra(J)
        capturou = False
        
        while True:
            # Recebe a jogada do jogador da vez em loop até que seja uma jogada válida
            if vez == nome_um:
                jogada = primeiro(J,vez)
            else:
                jogada = segundo(J,vez)

            if jogada in jogadas_válidas(J):
                # jogada aceita, podemos sair do loop!
                break
            
        # Registra a jogada
        J['jogadas'].add(jogada)
            
        # Verificamos se a jogada capturou quadrados, e em caso positivo, registramos esse fato:
        capturados = quadrados_capturados(jogada,J)
        if len(capturados) > 0:
            for quadrado in capturados:
                J[vez].add(quadrado)

        # Verificamos se o jogo acabou de ser vencido
        resultado = jogo_acabou(J)
        if resultado in {nome_um, nome_dois}:
            if interativo:
                mostra(J)
                print(f'!!! {resultado} venceu !!!')
                return
            else:
                return resultado
        elif resultado == 'empate':
        # Verificamos se o jogo acabou em empate
            if interativo:
                mostra(J)
                print("Empate...")
                return
            else:
                return 'empate'

        # Vejamos se a vez troca para a próxima rodada
        if len(capturados) == 0:
            vez = outro(vez)

def torneio(jogador_um, jogador_dois, número_partidas=10**2, tamanho=None):
    """
    Roda um 'torneio' de 2*número_partidas jogos entre os jogadores passados como argumento (metade como cada um sendo o primeiro a jogar).
    Se for passado o argumento  tamanho  , todos os jogos são jogados na malha com o tamanho especificado; senão, as partidas são jogadas em malhas de tamanho aleatório de 3 a 9.
    O valor retornado é um dicionário com as porcentagens de vezes em que cada resultado foi obtido nos jogos.
    """
    s = ''
    if jogador_um == jogador_dois:
        # Vamos usar asteriscos para diferencias as duas "cópias" do mesmo jogador
        s = '*'
        
    um = f"{jogador_um.__name__}{s}"
    dois = f"{jogador_dois.__name__}{s*2}"
    
    resultados = {um: 0, dois: 0, 'empate': 0}
    
    for _ in range(número_partidas):
        if tamanho is None:
            tamanho = random.randint(3,9)
            
        res = jogar(jogador_um, jogador_dois, tamanho, interativo=False)
        if res == nome_um:
            resultados[um] += 1
        elif res == nome_dois:
            resultados[dois] += 1
        else:
            resultados['empate'] += 1
        
        res = jogar(jogador_dois, jogador_um, tamanho, interativo=False)
        if res == nome_um:
            resultados[dois] += 1
        elif res == nome_dois:
            resultados[um] += 1
        else:
            resultados['empate'] += 1
            
    for c in resultados:
        resultados[c] = f"{100*resultados[c]/(2*número_partidas):.2f}%"
    return resultados
