##################################################################################################
### Nome do aplicativo: Analisador Lexico	######################################################
##################################################################################################
##################################################################################################
#####  Ambiente(s) de Desenvolvimento utilizado(s): PyCharm ######################################
##################################################################################################
##### Data de inicio da implementação do codigo: 23/10/2019 ######################################
##### Data de verificação final do codigo: 07/11/2019 ############################################
##################################################################################################
##################################################################################################
##### Nome: Pedro Daniel Camargos Soares 		Matricula: 0020640      ##########################
##################################################################################################
##### Nome: Lucas Gabriel de Almeida		 	Matricula: 0035333	##############################
##################################################################################################
##################################################################################################

# Biblioteca usada para pegar o caminho dos arquivos .txt
from os import path

import sys


# Classe que define os tokens
# Sao definidos por uma tupla, contendo um identificador (numero) e uma string (o token)
class TipoToken:
    # Tokens "Normais"
    ID = (1, 'identificador')
    CTE = (2, 'numero')
    CADEIA = (3, 'cadeia')
    ATRIB = (4, 'atribucao')
    OPREL = (5, 'relacional')
    OPAD = (6, 'maisoumenos')
    OPMUL = (7, 'multoudiv')
    OPNEG = (8, '!')
    PVIRG = (9, ';')
    DPONTOS = (10, ':')
    VIRG = (11, ',')
    ABREPAR = (12, '(')
    FECHARPAR = (13, ')')
    ABRECH = (14, '{')
    FECHACH = (15, '}')
    FIMARQ = (16, 'fim-de-arquivo')
    ERROR = (17, 'erro')

    # Tokens das palavras reservadas
    PROGRAMA = (18, 'programa')
    VARIAVEIS = (19, 'variaveis')
    INTEIRO = (20, 'inteiro')
    REAL = (21, 'real')
    LOGICO = (22, 'logico')
    CARACTER = (23, 'caracter')
    SE = (24, 'se')
    SENAO = (25, 'senao')
    ENQUANTO = (26, 'enquanto')
    LEIA = (27, 'leia')
    ESCREVA = (28, 'escreva')
    FALSO = (29, 'falso')
    VERDADEIRO = (30, 'verdadeiro')


# Classe que define as caracteristicas do token
# É definido pelo seu tipo (TipoToken), seu lexema (o que foi lido) e a linha em que foi lido
class Token:
    def __init__(self, tipo, lexema, linha):
        self.tipo = tipo
        (const, msg) = tipo
        self.const = const
        self.msg = msg
        self.lexema = lexema
        self.linha = linha


# Parte principal do analisador lexico
class Lexico:
    # Estrutura do tipo dicionario, que relaciona uma string (lida no arquivo) com um token
    reservadas = {'programa': TipoToken.PROGRAMA, 'variaveis': TipoToken.VARIAVEIS, 'inteiro': TipoToken.INTEIRO,
                  'real': TipoToken.REAL, 'logico': TipoToken.LOGICO, 'caracter': TipoToken.CARACTER,
                  'se': TipoToken.SE, 'senao': TipoToken.SENAO, 'enquanto': TipoToken.ENQUANTO, 'leia': TipoToken.LEIA,
                  'escreva': TipoToken.ESCREVA, 'falso': TipoToken.FALSO, 'verdadeiro': TipoToken.VERDADEIRO}

    # Funcao que recebe o nome do arquivo
    def __init__(self, nomeArquivo):
        self.nomeArquivo = nomeArquivo
        self.arquivo = None
        # os atributos buffer e linha sao incluidos no metodo abreArquivo

    # Funcao que abre o arquivo
    def abreArquivo(self):
        if not self.arquivo is None:  # Verifica se o arquivo esta aberto
            print('ERRO: Arquivo ja aberto')
            quit()
        elif path.exists(self.nomeArquivo):  # Verifica se e um caminho valido, se for abre
            self.arquivo = open(self.nomeArquivo, "r")  # Abre no modo de leitura
            # fila de caracteres 'deslidos' pelo ungetChar
            self.buffer = ''  # Acho que limpa o buffer para iniciar a leitura
            self.linha = 1  # Contador de linhas, iniciando em 1
        else:  # Caso algum erro ocorra
            print('ERRO: Arquivo "%s" inexistente.' % self.nomeArquivo)
            quit()

    # Funcao que fecha o arquivo
    def fechaArquivo(self):
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        else:
            self.arquivo.close()

    # Funcao responsavel por ler o arquivo, caracter por caracter
    def getChar(self):
        if self.arquivo is None:  # Verifica se o arquivo esta aberto
            print('ERRO: Nao ha arquivo aberto')
            quit()
        elif len(self.buffer) > 0:  # ??
            c = self.buffer[0]
            self.buffer = self.buffer[1:]
            return c
        else:  # Le um caracter do arquivo
            c = self.arquivo.read(1)
            # se nao foi eof, pelo menos um car foi lido
            # senao len(c) == 0
            if len(c) == 0:
                return None
            else:
                return c.lower()  # Retorna o caracter lido em letra minuscula, pois a linguagem P nao e case sensitive

    def ungetChar(self, c):  # ??
        if not c is None:
            self.buffer = self.buffer + c

    # Funcao que fica lendo caracteres ate eles formarem um token
    def getToken(self):
        lexema = ''  # String que armazena o nome do token lido
        estado = 1  # Estado inicial que le um caracter
        car = None  # Variavel que armazena o caracter lido

        #  Laco infinito que le ate for fim de arquivo
        while True:
            if estado == 1:  # estado inicial que faz primeira classificacao

                car = self.getChar()  # Le um caracter

                if car is None:  # Se nao tiver lido nada, foi fim de arquivo
                    return Token(TipoToken.FIMARQ, '<eof', self.linha)  # Retorna o token fim de arquivo
                elif car in {' ', '\t', '\n'}:  # Se tiver lido um espaco em branco nao faz nada, a nao ser que seja \n
                    if car == '\n':  # Se for \n, conta mais uma linha
                        self.linha = self.linha + 1
                elif car.isalpha():  # Se o caracter lido for uma letra
                    estado = 2
                elif car.isdigit():  # Se o caracter lido for um numero
                    estado = 3
                elif car in {'=', '<', '>', ',', ':', ';', '+', '-', '*', '(', ')', '{',
                             '}'}:  # Se o caracter lido for especial
                    estado = 4
                elif car == '/':  # Se o caracter lido for uma barra (comentario ou divisao)
                    estado = 5
                elif car == '"':  # Se o caractere lido for aspas duplas (string)
                    estado = 6
                else:  # Se leu algo invalido
                    return Token(TipoToken.ERROR, '<' + car + '>', self.linha)  # Retorna token do tipo erro

            elif estado == 2:  # estado que trata nomes (identificadores ou palavras reservadas)

                lexema = lexema + car  # String que armazena os caracteres lidos

                car = self.getChar()  # Le o proximo caractere
                if car is None or (not car.isalnum()):  # Se algo nao foi lido ou o caractere lido nao for um numero

                    # terminou o nome
                    self.ungetChar(car)  # ??
                    if lexema in Lexico.reservadas:  # Verifica se o lexema lido e uma palavra reservada
                        return Token(Lexico.reservadas[lexema], lexema,
                                     self.linha)  # Se for retorna o token da palavra reservada

                    # Verifica se o identificador lido possui caracteres invalidos
                    elif 'ç' in lexema or lexema[0].isdigit():
                        return Token(TipoToken.ERROR, 'caracter(es) invalido(s)', self.linha)

                    elif len(lexema) > 32:
                        return Token(TipoToken.ERROR, 'id com mais de 32 caracteres', self.linha)

                    else:  # Se tudo deu certo, retorna um token do tipo identificador
                        return Token(TipoToken.ID, lexema, self.linha)

            elif estado == 3:  # estado que trata numeros

                lexema = lexema + car  # String que armazena os caracteres lidos
                car = self.getChar()  # Le o proximo caractere

                # Se terminou de ler ou o caractere nao for um numero e for diferente de um ponto (REAL)
                if car is None or (not car.isdigit() and car != '.'):
                    # terminou o numero
                    self.ungetChar(car)
                    return Token(TipoToken.CTE, lexema, self.linha)  # Retorna token do tipo numero

            elif estado == 4:  # estado que trata outros tokens primitivos comuns

                lexema = lexema + car  # String que armazena os caracteres lidos

                #  Se o caracter lido for dois pontos, e preciso tratar se é um token do
                #  tipo atribuicao ou dois pontos
                if car == ':':
                    car2 = self.getChar()  # "Ve no futuro" qual sera o proximo token a vir
                    # self.ungetChar(car)
                    # Se for um igual, é atribuição, se nao, é dois pontos
                    if car2 != '=':
                        return Token(TipoToken.DPONTOS, lexema, self.linha)
                    else:
                        return Token(TipoToken.ATRIB, lexema, self.linha)

                elif car in {'=', '<', '>'}:  # Se for um caracter de comparacao
                    return Token(TipoToken.OPREL, lexema, self.linha)  # Retorna token do tipo relacional

                elif car in {'+', '-'}:  # Se for um caracter de soma ou subtracao
                    return Token(TipoToken.OPAD, lexema, self.linha)  # Retorna um token do tipo operacao adicao

                elif car == '*':  # Se for um caractere de multiplicao
                    return Token(TipoToken.OPMUL, lexema, self.linha)  # Retorna um token do tipo operacao multiplicacao

                elif car == '!':  # se for um ponto de exclamacao
                    return Token(TipoToken.OPNEG, lexema, self.linha)  # Retorna um token do tipo negacao

                elif car == ',':  # Se for uma virgula
                    return Token(TipoToken.VIRG, lexema, self.linha)  # Retorna um token do tipo virgula

                elif car == ';':  # Se for um caractere ponto e virgula
                    return Token(TipoToken.PVIRG, lexema, self.linha)  # Retorna um token do tipo ponto e virgula

                elif car == '(':  # Se for um caractere do tipo abre parentes
                    return Token(TipoToken.ABREPAR, lexema, self.linha)  # Retorna um token do tipo abre parenteses

                elif car == ')':  # Se for um caractere do tipo fecha parentes
                    return Token(TipoToken.FECHARPAR, lexema, self.linha)  # Retorna um token do tipo fecha parenteses

                elif car == '{':  # Se for um caractere do tipo abre parentes
                    return Token(TipoToken.ABRECH, lexema, self.linha)  # Retorna um token do tipo abre chaves

                elif car == '}':  # Se for um caractere do tipo abre parentes
                    return Token(TipoToken.FECHACH, lexema, self.linha)  # Retorna um token do tipo fecha chaves

            elif estado == 5:  # Estado que trata comentarios

                car2 = self.getChar()  # "Ve no futuro" qual sera o proximo token a vir
                # self.ungetChar(car)
                if car2 != '/' and car2 != '*':  # Se nao for um comentario
                    return Token(TipoToken.OPMUL, lexema, self.linha)  # Retorna token de operacao de multiplicacao
                elif car2 == '/':  # Se for comentario em linha
                    # consumindo comentario
                    while (not car is None) and (car != '\n'):  # Le os caracters e nao faz nada ate o fim da linha
                        car = self.getChar()
                    self.linha = self.linha + 1  # Atualiza a linha atual
                    estado = 1  # Retorna ao estado de iniciar a leitura
                elif car2 == '*':  # Se for comentario em bloco
                    # consumindo comentario
                    while (not car is None) and (car != '*'):
                        car = self.getChar()
                        if car is None:
                            # Se nunca foi fechado, retorna erro
                            return Token(TipoToken.ERROR, "comentario nao fechado", self.linha)
                        if car == '*':  # Verifica se o bloco de comentario foi fechado
                            car = self.getChar()
                            if car == '/':
                                estado = 1
                                break

            elif estado == 6:  # Estado que trata strings

                if car == '"':

                    lexema = lexema + '"'  # String que armazena os caracteres lidos
                    car = self.getChar()  # Le o proximo caracter
                    lexema = lexema + car  # Armazena na string
                    while (not car is None) and (car != '"'):  # Le a string ate ela ser fechada
                        car = self.getChar()

                        if car is None:  # Se nao tiver lido nada, foi fim de arquivo
                            # Retorna o token de erro, pois as aspas nao foram fechadas
                            return Token(TipoToken.ERROR, "Aspas nao fechadas", self.linha)

                        lexema = lexema + car

                    estado = 1

                return Token(TipoToken.CADEIA, lexema, self.linha)  # Retorna o token do tipo string


if __name__ == "__main__":

    # Variavel nome armazena o nome do arquivo
    # nome = input("Digite o nome do arquivo e sua extensão")
    # nome = "exemplo1.txt"
    nome = sys.argv[1]

    lex = Lexico(nome)  # Define o nome do arquivo
    lex.abreArquivo()  # Abre o arquivo

    tabela_simbolos = None

    if len(sys.argv) > 2:

        if sys.argv[2] == "-t":
            print("Teste")
            tabela_simbolos = open(sys.argv[3], "w")
            #tabela_simbolos.writelines(lex.reservadas)
            tabela_simbolos.write(str(lex.reservadas))

    while True:  # Laço infinito ate ler o fim do arquivo
        token = lex.getToken()  # Le um token
        print("token= %s , lexema= (%s), linha= %d\n" % (token.msg, token.lexema, token.linha))
        if token.const == TipoToken.FIMARQ[0]:  # Se for fim de arquivo, sai do laço
            break
    lex.fechaArquivo()  # Fecha o arquivo