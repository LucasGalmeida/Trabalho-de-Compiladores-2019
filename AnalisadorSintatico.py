##################################################################################################
### Nome do aplicativo: Analisador Sintatico	##################################################
##################################################################################################
##################### Instruçoes para compilação e execução do programa ##########################
#
#		1.	Para compilar o arquivo, deve-se usar o compilador de python
#		2.	Usando o terminal, passe o seguinte comando:
#		3.	python <codigo.py> <arquivo_de_entrada.txt> -t <nome_arquivo_saida.txt>
#		4.	Exemplo:  python AnalisadorSintatico.py exemplo2.txt -t saida1.txt
#		5.	Caso tudo esteja certo, o arquivo sera compilado e a tabela de símbolos gerada
#
#
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

#  Importe o analisador lexico
from AnalisadorLexico import TipoToken as tt, Token, Lexico
import sys


# Classe principal do analisador sintatico
class Sintatico:

    def __init__(self):
        self.lex = None
        self.tokenAtual = None

        self.tabela = {'programa': tt.PROGRAMA, 'variaveis': tt.VARIAVEIS, 'inteiro': tt.INTEIRO,
                       'real': tt.REAL, 'logico': tt.LOGICO, 'caracter': tt.CARACTER,
                       'se': tt.SE, 'senao': tt.SENAO, 'enquanto': tt.ENQUANTO, 'leia': tt.LEIA,
                       'escreva': tt.ESCREVA, 'falso': tt.FALSO, 'verdadeiro': tt.VERDADEIRO}

        self.strIDS = ""

    # Inicia o analisador sintatico
    def interprete(self, nomeArquivo):
        if not self.lex is None:  # Verifica se ja ha um arquivo sendo lido pelo lexico
            print('ERRO: ja existe um arquivo sendo processado.')
        else:  # Se nao houver, inicia a leitura
            self.lex = Lexico(nomeArquivo)
            self.lex.abreArquivo()
            self.tokenAtual = self.lex.getToken()  # Pede ao lexico para enviar o primeiro token

            self.A()  # Nao terminal inicial da gramatica

            self.lex.fechaArquivo()  # Fecha o arquivo

    def atualIgual(self, token):  # Verifica se o token lido é igual ao esperado
        (const, msg) = token
        return self.tokenAtual.const == const

    def consome(self, token):  # Consome o token atual, e chama o proximo

        if self.atualIgual(tt.ERROR):
            (const, msg) = token
            print('ERRO DE SINTAXE [linha %d]: foi recebido "%s"'
                  % (self.tokenAtual.linha, self.tokenAtual.lexema))

        elif self.atualIgual(token):  # Verifica se o token foi o esperado
            self.tokenAtual = self.lex.getToken()

        elif not self.atualIgual(tt.FIMARQ):
            print('ERRO DE SINTAXE [linha %d]: foi recebido "%s"'
                  % (self.tokenAtual.linha, self.tokenAtual.lexema))

    def A(self):  # Nao terminal Inicial
        self.PROG()  # Chama o "Main"
        self.consome(tt.FIMARQ)  # Consome o fim de arquivo

    def PROG(self):  # Nao terminal "Main"

        self.consome(tt.PROGRAMA)  # Consome o terminal programa
        self.tabela.__setitem__(self.tokenAtual.lexema, tt.PROGRAMA)
        self.consome(tt.ID)  # Consome o terminal que indica o "nome" do programa
        self.consome(tt.PVIRG)  # Consome o terminal ponto e virgula

        if self.atualIgual(tt.ERROR):
            while self.tokenAtual.const != 14 and self.tokenAtual.const != 16:
                self.tokenAtual = self.lex.getToken()
            self.DECLS()  # Chama as declaracoes
        else:
            self.DECLS()  # Chama as declaracoes

        self.C_COMP()  # Chama a funcao que abre chaves, chama os comandos e fecha chaves

    def DECLS(self):  # Nao terminal das declaracoes

        if self.atualIgual(tt.ERROR):
            while self.tokenAtual.const != 14 and self.tokenAtual.const != 16:
                self.tokenAtual = self.lex.getToken()
            if self.atualIgual(tt.VARIAVEIS):  # Se houver alguma variavel nova
                self.consome(tt.VARIAVEIS)  # Consome o terminal variaveis
                self.LIST_DECLS()  # Chama o nao terminal responsavel pela estrutura das variaveis
            else:  # Se nao houver mais nenhuma variavel
                pass
        else:
            if self.atualIgual(tt.VARIAVEIS):  # Se houver alguma variavel nova
                self.consome(tt.VARIAVEIS)  # Consome o terminal variaveis
                self.LIST_DECLS()  # Chama o nao terminal responsavel pela estrutura das variaveis
            else:  # Se nao houver mais nenhuma variavel
                pass

    def LIST_DECLS(self):  # Nao terminal responsavel pela estrutura das variaveis

        if self.atualIgual(tt.ERROR):

            (const, msg) = tt.ERROR
            print('ERRO DE SINTAXE [linha %d]: foi recebido "%s"'
                  % (self.tokenAtual.linha, self.tokenAtual.lexema))

            while (self.tokenAtual.const != 14 and self.tokenAtual.const != 16 and self.tokenAtual.const != 10
                   and self.tokenAtual.const != 1 and self.tokenAtual.const != 11):
                self.tokenAtual = self.lex.getToken()
            self.DECL_TIPO()  # Chama o nao terminal responsavel pela estrutura das variaveis
        else:
            self.DECL_TIPO()  # Chama o nao terminal responsavel pela estrutura das variaveis

        if self.atualIgual(tt.ERROR):
            (const, msg) = tt.ERROR
            print('ERRO DE SINTAXE [linha %d]: foi recebido "%s"'
                  % (self.tokenAtual.linha, self.tokenAtual.lexema))
            while (self.tokenAtual.const != 14 and self.tokenAtual.const != 16 and self.tokenAtual.const != 10
                   and self.tokenAtual.const != 1 and self.tokenAtual.const != 11):
                self.tokenAtual = self.lex.getToken()
            self.D()  # Chama o nao terminal que verifica se ha mais outra variavel
        else:
            self.D()  # Chama o nao terminal que verifica se ha mais outra variavel

    def D(self):  # Terminal que verifica se ha mais outra variavel

        if self.atualIgual(tt.ID):  # Se tiver lido um ID, é outra variavel
            self.LIST_DECLS()
        else:  # Se nao, acabou
            pass

    def DECL_TIPO(self):  # Nao terminal responsavel pela estrutura das variaveis

        if self.atualIgual(tt.CTE):
            print('ERRO DE SINTAXE [linha %d]: Variaveis nao podem começar com numeros.'
                  % self.tokenAtual.linha)
        elif not (self.atualIgual(tt.ID)):
            print('ERRO DE SINTAXE [linha %d]: Era esperado um ID após "%s"'
                  % (self.tokenAtual.linha, self.tokenAtual.lexema))

        self.LIST_ID()  # Primeiro chama o nao terminal responsavel por ler um ID
        self.consome(tt.DPONTOS)  # Depois consome o terminal DoisPontos
        self.TIPO()  # Depois chama o nao terminal responsavel pelo tipo da variavel
        self.consome(tt.PVIRG)  # Depois consome o terminal ponto e virgula

    def LIST_ID(self):  # Nao terminal responsavel por ler um identificador

        if self.tokenAtual.const != 1:
            while (self.tokenAtual.const != 10 and self.tokenAtual.const != 16 and
                   self.tokenAtual.const != 13 and self.tokenAtual.const != 1):
                self.tokenAtual = self.lex.getToken()

        if self.atualIgual(tt.ID):
            self.strIDS = self.strIDS + ' "%s"' % self.tokenAtual.lexema

        self.consome(tt.ID)  # Consome um identificador
        self.E()  # Chama o nao terminal para verificar se a mais um ID

    def E(self):  # Nao terminal responsavel por verificar se os ID acabaram, ou se mais um foi declarado

        if self.atualIgual(tt.ERROR):
            while (self.tokenAtual.const != 10 and self.tokenAtual.const != 16 and
                   self.tokenAtual.const != 13 and self.tokenAtual.const != 1):
                self.tokenAtual = self.lex.getToken()

            if self.atualIgual(tt.VIRG):  # Se leu uma virgula, significa que ha mais uma declaracao
                self.consome(tt.VIRG)  # Consome o terminal virgula
                self.LIST_ID()  # Chama o nao terminal para ler mais um ID
            else:  # Se nao ler uma virgula, os ID acabaram.
                pass

        else:
            if self.atualIgual(tt.VIRG):  # Se leu uma virgula, significa que ha mais uma declaracao
                self.consome(tt.VIRG)  # Consome o terminal virgula
                self.LIST_ID()  # Chama o nao terminal para ler mais um ID
            else:  # Se nao ler uma virgula, os ID acabaram.
                pass

    def TIPO(self):  # Nao terminal responsalvel por verificar a declaracao da variavel

        if self.atualIgual(tt.INTEIRO):  # Se a variavel for do tipo inteiro
            self.tabela.__setitem__(self.strIDS, tt.INTEIRO)
            self.consome(tt.INTEIRO)  # Consome o terminal inteiro

        elif self.atualIgual(tt.REAL):  # Se a variavel for do tipo real
            self.tabela.__setitem__(self.strIDS, tt.REAL)
            self.consome(tt.REAL)  # Consome o terminal real

        elif self.atualIgual(tt.LOGICO):  # Se a variavel for do tipo logico
            self.tabela.__setitem__(self.strIDS, tt.LOGICO)
            self.consome(tt.LOGICO)  # Consome o terminal logico

        elif self.atualIgual(tt.CARACTER):  # Se a variavel for do tipo caracter
            self.tabela.__setitem__(self.strIDS, tt.CARACTER)
            self.consome(tt.CARACTER)  # Consome o terminal caracter

        self.strIDS = ""

    def C_COMP(self):  # Nao terminal que verifica a estrutura dos comandos

        if self.atualIgual(tt.ERROR):

            (const, msg) = tt.ERROR
            print('ERRO DE SINTAXE [linha %d]: foi recebido "%s"'
                  % (self.tokenAtual.linha, self.tokenAtual.lexema))

            while (self.tokenAtual.const != 26 and self.tokenAtual.const != 16 and
                   self.tokenAtual.const != 28 and self.tokenAtual.const != 1 and
                   self.tokenAtual.const != 27 and self.tokenAtual.const != 24 and
                   self.tokenAtual.const != 25):
                self.tokenAtual = self.lex.getToken()
        else:
            self.consome(tt.ABRECH)  # Consome o terminal abre chaves

        self.LISTA_COMANDOS()  # Chama o nao terminal para verificar os comandos declarados

        if self.atualIgual(tt.ERROR):
            while (self.tokenAtual.const != 26 and self.tokenAtual.const != 16 and
                   self.tokenAtual.const != 28 and self.tokenAtual.const != 1 and
                   self.tokenAtual.const != 27 and self.tokenAtual.const != 24 and
                   self.tokenAtual.const != 25):
                self.tokenAtual = self.lex.getToken()
        else:
            self.consome(tt.FECHACH)  # Consome o terminal fecha chaves

    def LISTA_COMANDOS(self):  # Nao terminal que verifica se um comando foi declarado

        if self.atualIgual(tt.ERROR):
            while (self.tokenAtual.const != 26 and self.tokenAtual.const != 16 and
                   self.tokenAtual.const != 24 and self.tokenAtual.const != 28 and
                   self.tokenAtual.const != 1 and self.tokenAtual.const != 27):
                self.tokenAtual = self.lex.getToken()
            self.COMANDOS()  # Nao terminal que verifica a estrutura do comando declarado
        else:
            self.COMANDOS()  # Nao terminal que verifica a estrutura do comando declarado

        if self.atualIgual(tt.ERROR):
            while self.tokenAtual.const != 15 and self.tokenAtual.const != 16 and self.tokenAtual.const != 9:
                self.tokenAtual = self.lex.getToken()
            self.G()  # Nao terminal que verifica se mais um comando foi declarado
        else:
            self.G()  # Nao terminal que verifica se mais um comando foi declarado

    def G(self):  # Nao terminal que verifica se mais algum comando foi declarado

        if self.atualIgual(tt.PVIRG):
            self.tokenAtual = self.lex.getToken()

        if self.atualIgual(tt.SE) or self.atualIgual(tt.ENQUANTO) or self.atualIgual(tt.LEIA) or self.atualIgual(
                tt.ESCREVA) or self.atualIgual(tt.ID) or self.atualIgual(tt.ERROR):  # Se um comando foi declarado

            if self.atualIgual(tt.ERROR):
                self.consome(tt.ERROR)

            self.LISTA_COMANDOS()  # Chama o nao terminal para verificar qual comando foi declarado
        else:  # Se nenhum tiver sido declarado
            pass

    def COMANDOS(self):  # Nao terminal que verifica qual comando foi declarado

        if self.atualIgual(tt.SE):  # Se foi declarado um comando do tipo SE
            self.IF()  # Chama o nao terminal responsavel pela estrutura do tipo IF
        elif self.atualIgual(tt.ENQUANTO):  # Se foi declarado um comando do tipo ENQUANTO
            self.WHILE()  # Chama o nao terminal responsavel pela estrutura do tipo WHILE
        elif self.atualIgual(tt.LEIA):  # Se foi declarado um comando do tipo LEIA
            self.READ()  # Chama o nao terminal responsavel pela estrutura do tipo READ
        elif self.atualIgual(tt.ESCREVA):  # Se foi declarado um comando do tipo ESCREVA
            self.WRITE()  # Chama o nao terminal responsavel pela estrutura do tipo WRITE
        elif self.atualIgual(tt.ID):  # Se foi declarado um comando do tipo ID
            self.ATRIB()  # Chama o nao terminal responsavel pela estrutura do tipo ATRIB

    def IF(self):  # Nao terminal responsavel pela estrutura do tipo SE

        self.consome(tt.SE)  # Consome o token SE
        self.consome(tt.ABREPAR)  # Consome o token abre parenteses
        self.EXPR()  # Chama o nao terminal responsavel pela declaracao da expressao
        self.consome(tt.FECHARPAR)  # Consome o token fecha parenteses
        if self.tokenAtual.const != '14' and self.tokenAtual.lexema != '{' and not self.atualIgual(tt.ERROR):
            print('ERRO DE SINTAXE [linha %d]: era esperado "{" ' % self.tokenAtual.linha)
        self.C_COMP()  # Chama o nao terminal responsavel pela estrutura do comando
        self.H()  # Chama o nao terminal que verifica se a estrutura condicional possui o SENAO

    def H(self):  # Nao terminal que verifica se o SENAO foi declarado

        if self.atualIgual(tt.SENAO):  # Se o token atual for SENAO
            self.consome(tt.SENAO)  # Consome o terminal SENAO
            if self.tokenAtual.const != '14' and self.tokenAtual.lexema != '{' and not self.atualIgual(tt.ERROR):
                print('ERRO DE SINTAXE [linha %d]: era esperado "{" ' % self.tokenAtual.linha)
            self.C_COMP()  # Chama o nao terminal responsavel pela declaracao dos comandos
        else:  # Nao houve o SENAO
            pass

    def WHILE(self):  # Nao terminal responsavel pela declaracao ENQUANTO

        self.consome(tt.ENQUANTO)  # Consome o terminal ENQUANTO
        self.consome(tt.ABREPAR)  # Consome o terminal abre parenteses
        self.EXPR()  # Chama o nao terminal para ler a expressao
        self.consome(tt.FECHARPAR)  # Consome o terminal fecha parenteses
        if self.tokenAtual.const != '14' and self.tokenAtual.lexema != '{' and not self.atualIgual(tt.ERROR):
            print('ERRO DE SINTAXE [linha %d]: era esperado "{" ' % self.tokenAtual.linha)
        self.C_COMP()  # Chama o nao terminal responsavel pela declaracao dos comandos

    def READ(self):  # Nao terminal responsavel pela declaracao LEIA

        self.consome(tt.LEIA)  # Consome o terminal LEIA
        self.consome(tt.ABREPAR)  # Consome o terminal abre parenteses
        self.LIST_ID()  # Chama o nao terminal responsavel por ler um identificador
        self.consome(tt.FECHARPAR)  # Chama o terminal fechha parenteses
        self.consome(tt.PVIRG)  # Chama o terminal ponto e virgula

    def ATRIB(self):  # Nao terminal responsavel pela atribuicao

        self.consome(tt.ID)  # Consome o terminal identificador
        self.consome(tt.ATRIB)  # Consome o terminal de atribuicao
        self.EXPR()  # Chama o nao terminal responsavel por ler a expressao
        self.consome(tt.PVIRG)  # Consome o terminal ponto e virgula

    def WRITE(self):  # Nao terminal responsavel pela declaracao ESCRITA
        self.consome(tt.ESCREVA)  # Consome o terminal ESCREVA
        self.consome(tt.ABREPAR)  # Consome o terminal abre parenteses
        self.LIST_W()  # Chama o nao terminal responsavel por escrever a string
        self.consome(tt.FECHARPAR)  # Consome o terminal fecha parenteses
        self.consome(tt.PVIRG)  # Consome o terminal ponto e virgula

    def LIST_W(self):  # Nao terminal responsavel pela estrutura da escrita
        self.ELEM_W()  # Chama o nao terminal responsavel por escrever a cadeia de caracteres
        self.L()  # Chama o nao terminal que verifica se mais alguma cadeia necessita ser escrita

    def L(self):  # Nao terminal que verifica se mais alguma cadeia necessita ser escrita
        if self.atualIgual(tt.VIRG):  # Se ler uma virgula, ha mais uma cadeia a ser escrita
            self.consome(tt.VIRG)  # Consome o terminal virgula
            self.LIST_W()  # Chama o nao terminal para escrever outra string
        else:  # Se acabou
            pass

    def ELEM_W(self):  # Nao terminal que verifica o que sera escrito
        if self.atualIgual(tt.CADEIA):  # Se for o token cadeia
            self.consome(tt.CADEIA)  # Consome o terminal cadeia
        else:  # Se for uma expressao
            self.EXPR()  # Chama o nao terminal responsavel pela expressao

    def EXPR(self):  # Nao terminal que le uma serie de numeros e operacoes
        self.SIMPLES()  # Chama o nao terminal que le uma serie de numeros e operacoes
        self.P()  # Chama o nao terminal que verifica se houve uma declaracao do tipo relacional

    def P(self):  # Nao terminal que verifica se houve uma declaracao do tipo relacional
        if self.atualIgual(tt.OPREL):  # Se o token  atual for do tipo OPREL
            self.consome(tt.OPREL)  # Consome o terminal OPREL
            self.SIMPLES()  # Chama o nao terminal para ler mais numeros/operacoes
        else:  # Se nao, acabou
            pass

    def SIMPLES(self):  # Nao terminal que le uma serie de numeros e operacoes
        self.TERMO()  # Chama o nao terminal que le  uma serie de numeros e operacoes
        self.R()  # Chama o nao terminal que verifica se a mais numeros/operacoes

    def R(self):  # Nao terminal que verifica se houve uma declaracao de adicao/subtracao
        if self.atualIgual(tt.OPAD):  # Se houve
            self.consome(tt.OPAD)  # Consome o terminal OPAD
            self.SIMPLES()  # Chama o nao terminal para ler a declaracao de outra expressao
        else:  # Se nao houve, acabou
            pass

    def TERMO(self):  # Nao terminal que le uma serie de numeros e operacoes
        self.FAT()  # Chama o nao terminal para ler os numeros e operacoes
        self.S()  # Chama o nao terminal para verificar se houve uma declaracao do tipo multiplicacao/divisao

    def S(self):  # Nao terminal que verifica se houve uma declaracao de multiplicacao/divisao
        if self.atualIgual(tt.OPMUL):  # Se houve
            self.consome(tt.OPMUL)  # Consome o terminal OPMUL
            self.TERMO()  # Chama o nao terminal para repetir o processo
        else:  # Se nao houve, acabou
            pass

    def FAT(self):  # Nao terminal que le os numeros e operacoes
        if self.atualIgual(tt.ID):  # Se o token atual for um identificador
            self.consome(tt.ID)  # Consome o terminal identificador
        elif self.atualIgual(tt.CTE):  # Se o token atual for um numero
            self.consome(tt.CTE)  # Consome o terminal de numero
        elif self.atualIgual(tt.ABREPAR):  # Se o token atual for um abre parenteses
            self.consome(tt.ABREPAR)  # Consome o terminal abre parenteses
            self.EXPR()  # Chama o nao terminal para ler a expressao
            self.consome(tt.FECHARPAR)  # Consome o terminal fecha parentes
        elif self.atualIgual(tt.VERDADEIRO):  # Se o token atual for um bolleano verdadeiro
            self.consome(tt.VERDADEIRO)  # Consome o terminal verdadeiro
        elif self.atualIgual(tt.FALSO):  # Se o token atual for um bolleano falso
            self.consome(tt.FALSO)  # Consome o terminal falso
        elif self.atualIgual(tt.OPNEG):  # Se o token atual for uma negacao
            self.consome(tt.OPNEG)  # Consome o terminal negacao
            self.FAT()  # Chama novamente o nao terminal que le os numeros e operacoes


if __name__ == "__main__":

    #nome = "exemplo1.txt"
    nome = sys.argv[1]
    parser = Sintatico()  # Cria o sintatico
    tabela_simbolos = None
    parser.interprete(nome)  # Comeca a ler o arquivo
    if len(sys.argv) > 2:
        if sys.argv[2] == "-t":
            tabela_simbolos = open(sys.argv[3], "w")
            # tabela_simbolos.writelines(lex.reservadas)
            tabela_simbolos.write(str(parser.tabela))
            # tabela_simbolos.write(parser.strIDS)

    print("----- FIM - DA - ANALISE -----")
