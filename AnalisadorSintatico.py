"""

    Gramatica:

    A               -> PROG $
    PROG            -> programa id pvirg DECLS C-COMP
    DECLS           -> lambda | variaveis LIST-DECLS
    LIST-DECLS      -> DECL-TIPO D
    D               -> lambda | LIST-DECLS
    DECL-TIPO       -> LIST-ID dpontos TIPO pvirg
    LIST-ID         -> id E
    E               -> lambda | virg LIST-ID
    TIPO            -> inteiro | real | logico | caracter
    C-COMP          -> abrech LISTA-COMANDOS fechach
    LISTA-COMANDOS  -> COMANDOS G
    G               -> lambda | LISTA-COMANDOS
    COMANDOS        -> IF | WHILE | READ | WRITE | ATRIB
    IF              -> se abrepar EXPR fechapar C-COMP H
    H               -> lambda | senao C-COMP
    WHILE           -> enquanto abrepar EXPR fechapar C-COMP
    READ            -> leia abrepar LIST-ID fechapar pvirg
    ATRIB           -> id atrib EXPR pvirg
    WRITE           -> escreva abrepar LIST-W fechapar pvirg
    LIST-W          -> ELEM-W L
    L               -> lambda | virg LIST-W
    ELEM-W          -> EXPR | cadeia
    EXPR            -> SIMPLES P
    P               -> lambda | oprel SIMPLES
    SIMPLES         -> TERMO R
    R               -> lambda | opad SIMPLES
    TERMO           -> FAT S
    S               -> lambda | opmul TERMO
    FAT             -> id | cte | abrepar EXPR fechapar | verdadeiro | falso | opneg FAT

    Tokens:
    ID CTE CADEIA ATRIB OPREL OPAD OPMUL OPNEG PVIRG DPONTOS VIRG ABREPAR FECHARPAR ABRECH FECHACH FIMARQ ERROR
    PROGRAMA VARIAVEIS INTEIRO REAL LOGICO CARACTER SE SENAO ENQUANTO LEIA ESCREVA FALSO VERDADEIRO

    Comentarios:

    Iniciam com // e vao ate o fim da linha
    ou
    Iniciam com /* e vao ate */

"""

#  Importe o analisador lexico
from AnalisadorLexico import TipoToken as tt, Token, Lexico


# Classe principal do analisador sintatico
class Sintatico:

    def __init__(self):
        self.lex = None
        self.tokenAtual = None

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
        if self.atualIgual(token):  # Verifica se o token foi o esperado
            self.tokenAtual = self.lex.getToken()
        else:  # Se o token nao for o esperado
            (const, msg) = token
            print('ERRO DE SINTAXE [linha %d]: era esperado "%s" mas foi recebido "%s"'
                  % (self.tokenAtual.linha, msg, self.tokenAtual.lexema))

            # self.tokenAtual = self.lex.getToken()
            quit()

    def A(self):  # Nao terminal Inicial
        self.PROG()  # Chama o "Main"
        self.consome(tt.FIMARQ)  # Consome o fim de arquivo

    def PROG(self):  # Nao terminal "Main"
        self.consome(tt.PROGRAMA)  # Consome o terminal programa
        self.consome(tt.ID)  # Consome o terminal que indica o "nome" do programa
        self.consome(tt.PVIRG)  # Consome o terminal ponto e virgula
        self.DECLS()  # Chama as declaracoes
        self.C_COMP()  # Chama a funcao que abre chaves, chama os comandos e fecha chaves

    def DECLS(self):  # Nao terminal das declaracoes
        if self.atualIgual(tt.VARIAVEIS):  # Se houver alguma variavel nova
            self.consome(tt.VARIAVEIS)  # Consome o terminal variaveis
            self.LIST_DECLS()  # Chama o nao terminal responsavel pela estrutura das variaveis
        else:  # Se nao houver mais nenhuma variavel
            pass

    def LIST_DECLS(self):  # Nao terminal responsavel pela estrutura das variaveis
        self.DECL_TIPO()  # Chama o nao terminal responsavel pela estrutura das variaveis
        self.D()  # Chama o nao terminal que verifica se ha mais outra variavel

    def D(self):  # Terminal que verifica se ha mais outra variavel
        if self.atualIgual(tt.ID):  # Se tiver lido um ID, é outra variavel
            self.LIST_DECLS()
        else:  # Se nao, acabou
            pass

    def DECL_TIPO(self):  # Nao terminal responsavel pela estrutura das variaveis
        self.LIST_ID()  # Primeiro chama o nao terminal responsavel por ler um ID
        self.consome(tt.DPONTOS)  # Depois consome o terminal DoisPontos
        self.TIPO()  # Depois chama o nao terminal responsavel pelo tipo da variavel
        self.consome(tt.PVIRG)  # Depois consome o terminal ponto e virgula

    def LIST_ID(self):  # Nao terminal responsavel por ler um identificador
        self.consome(tt.ID)  # Consome um identificador
        self.E()  # Chama o nao terminal para verificar se a mais um ID

    def E(self):  # Nao terminal responsavel por verificar se os ID acabaram, ou se mais um foi declarado
        if self.atualIgual(tt.VIRG):  # Se leu uma virgula, significa que ha mais uma declaracao
            self.consome(tt.VIRG)  # Consome o terminal virgula
            self.LIST_ID()  # Chama o nao terminal para ler mais um ID
        else:  # Se nao ler uma virgula, os ID acabaram.
            pass

    def TIPO(self):  # Nao terminal responsalvel por verificar a declaracao da variavel
        if self.atualIgual(tt.INTEIRO):  # Se a variavel for do tipo inteiro
            self.consome(tt.INTEIRO)  # Consome o terminal inteiro
        elif self.atualIgual(tt.REAL):  # Se a variavel for do tipo real
            self.consome(tt.REAL)  # Consome o terminal real
        elif self.atualIgual(tt.LOGICO):  # Se a variavel for do tipo logico
            self.consome(tt.LOGICO)  # Consome o terminal logico
        elif self.atualIgual(tt.CARACTER):  # Se a variavel for do tipo caracter
            self.consome(tt.CARACTER)  # Consome o terminal caracter

    def C_COMP(self):  # Nao terminal que verifica a estrutura dos comandos
        self.consome(tt.ABRECH)  # Consome o terminal abre chaves
        self.LISTA_COMANDOS()  # Chama o nao terminal para verificar os comandos declarados
        self.consome(tt.FECHACH)  # Consome o terminal fecha chaves

    def LISTA_COMANDOS(self):  # Nao terminal que verifica se um comando foi declarado
        self.COMANDOS()  # Nao terminal que verifica a estrutura do comando declarado
        self.G()  # Nao terminal que verifica se mais um comando foi declarado

    def G(self):  # Nao terminal que verifica se mais algum comando foi declarado
        if self.atualIgual(tt.SE) or self.atualIgual(tt.ENQUANTO) or self.atualIgual(tt.LEIA) or self.atualIgual(
                tt.ESCREVA) or self.atualIgual(tt.ID):  # Se um comando foi declarado
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
        self.C_COMP()  # Chama o nao terminal responsavel pela estrutura do comando
        self.H()  # Chama o nao terminal que verifica se a estrutura condicional possui o SENAO

    def H(self):  # Nao terminal que verifica se o SENAO foi declarado
        if self.atualIgual(tt.SENAO):  # Se o token atual for SENAO
            self.consome(tt.SENAO)  # Consome o terminal SENAO
            self.C_COMP()  # Chama o nao terminal responsavel pela declaracao dos comandos
        else:  # Nao houve o SENAO
            pass

    def WHILE(self):  # Nao terminal responsavel pela declaracao ENQUANTO
        self.consome(tt.ENQUANTO)  # Consome o terminal ENQUANTO
        self.consome(tt.ABREPAR)  # Consome o terminal abre parenteses
        self.EXPR()  # Chama o nao terminal para ler a expressao
        self.consome(tt.FECHARPAR)  # Consome o terminal fecha parenteses
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
    nome = "exemplo2.txt"

    parser = Sintatico()  # Cria o sintatico
    parser.interprete(nome)  # Comeca a ler o arquivo

""" TENTIVA FALHA DE IMPLEMENTAR O MODO PANICO 

            if self.atualIgual(tt.PROGRAMA):
                self.tokenAtual = tt.FIMARQ

            elif self.atualIgual(tt.VARIAVEIS):
                while self.tokenAtual != tt.ABRECH:
                    self.tokenAtual = self.lex.getToken()

            elif self.atualIgual(tt.ID):
                while (self.tokenAtual != tt.ABRECH or self.tokenAtual != tt.ID or
                       self.tokenAtual != tt.FECHACH or self.tokenAtual != tt.DPONTOS or
                       self.tokenAtual != tt.FECHARPAR or self.tokenAtual != tt.ENQUANTO or
                       self.tokenAtual != tt.ESCREVA or self.tokenAtual != tt.LEIA or
                       self.tokenAtual != tt.SE or self.tokenAtual != tt.VIRG or
                       self.tokenAtual != tt.PVIRG or self.tokenAtual != tt.OPREL or
                       self.tokenAtual != tt.OPMUL or self.tokenAtual != tt.OPAD):
                    self.tokenAtual = self.lex.getToken()

            elif self.atualIgual(tt.ATRIB):  # Marcado
                while (self.tokenAtual != tt.ABRECH or self.tokenAtual != tt.ID or
                       self.tokenAtual != tt.FECHACH or self.tokenAtual != tt.DPONTOS or
                       self.tokenAtual != tt.FECHARPAR or self.tokenAtual != tt.ENQUANTO or
                       self.tokenAtual != tt.ESCREVA or self.tokenAtual != tt.LEIA or
                       self.tokenAtual != tt.SE or self.tokenAtual != tt.VIRG or
                       self.tokenAtual != tt.PVIRG or self.tokenAtual != tt.OPREL or
                       self.tokenAtual != tt.OPMUL or self.tokenAtual != tt.OPAD):
                    self.tokenAtual = self.lex.getToken()

            elif self.atualIgual(tt.DPONTOS):  # Marcado
                pass

            elif self.atualIgual(tt.PVIRG):  # Marcado
                pass

            elif self.atualIgual(tt.VIRG):
                while self.tokenAtual != tt.DPONTOS or self.tokenAtual != tt.FECHARPAR:
                    self.tokenAtual = self.lex.getToken()

            elif self.atualIgual(tt.CARACTER):
                while self.tokenAtual != tt.PVIRG:
                    self.tokenAtual = self.lex.getToken()

            elif self.atualIgual(tt.INTEIRO):
                while self.tokenAtual != tt.PVIRG:
                    self.tokenAtual = self.lex.getToken()

            elif self.atualIgual(tt.LOGICO):
                while self.tokenAtual != tt.PVIRG:
                    self.tokenAtual = self.lex.getToken()

            elif self.atualIgual(tt.REAL):
                while self.tokenAtual != tt.PVIRG:
                    self.tokenAtual = self.lex.getToken()

            elif self.atualIgual(tt.ABRECH):
                while (self.tokenAtual != tt.ENQUANTO or self.tokenAtual != tt.ESCREVA or
                       self.tokenAtual != tt.FIMARQ or self.tokenAtual != tt.ID or
                       self.tokenAtual != tt.LEIA or self.tokenAtual != tt.SE or
                       self.tokenAtual != tt.SENAO):
                    self.tokenAtual = self.lex.getToken()

            elif self.atualIgual(tt.FECHACH):  # Marcado
                pass

            elif self.atualIgual(tt.ENQUANTO):
                while (self.tokenAtual != tt.FECHACH or self.tokenAtual != tt.ENQUANTO or
                       self.tokenAtual != tt.ESCREVA or self.tokenAtual != tt.ID or
                       self.tokenAtual != tt.LEIA or self.tokenAtual != tt.SE):
                    self.tokenAtual = self.lex.getToken()

            elif self.atualIgual(tt.ESCREVA):
                while (self.tokenAtual != tt.FECHACH or self.tokenAtual != tt.ENQUANTO or
                       self.tokenAtual != tt.ESCREVA or self.tokenAtual != tt.ID or
                       self.tokenAtual != tt.LEIA or self.tokenAtual != tt.SE):
                    self.tokenAtual = self.lex.getToken()

            elif self.atualIgual(tt.LEIA):
                while (self.tokenAtual != tt.FECHACH or self.tokenAtual != tt.ENQUANTO or
                       self.tokenAtual != tt.ESCREVA or self.tokenAtual != tt.ID or
                       self.tokenAtual != tt.LEIA or self.tokenAtual != tt.SE):
                    self.tokenAtual = self.lex.getToken()

            elif self.atualIgual(tt.SE):
                while (self.tokenAtual != tt.FECHACH or self.tokenAtual != tt.ENQUANTO or
                       self.tokenAtual != tt.ESCREVA or self.tokenAtual != tt.ID or
                       self.tokenAtual != tt.LEIA or self.tokenAtual != tt.SE):
                    self.tokenAtual = self.lex.getToken()

            elif self.atualIgual(tt.SENAO):
                while (self.tokenAtual != tt.ENQUANTO or
                       self.tokenAtual != tt.ESCREVA or self.tokenAtual != tt.ID or
                       self.tokenAtual != tt.LEIA or self.tokenAtual != tt.SE):
                    self.tokenAtual = self.lex.getToken()

            elif self.atualIgual(tt.ABREPAR):
                while (self.tokenAtual != tt.FECHARPAR or self.tokenAtual != tt.VIRG or
                       self.tokenAtual != tt.PVIRG or self.tokenAtual != tt.OPREL or
                       self.tokenAtual != tt.OPAD or self.tokenAtual != tt.OPMUL):
                    self.tokenAtual = self.lex.getToken()

            elif self.atualIgual(tt.FECHARPAR):  # Marcado
                pass

            elif self.atualIgual(tt.CADEIA):
                while self.tokenAtual != tt.FECHARPAR or self.tokenAtual != tt.VIRG:
                    self.tokenAtual = self.lex.getToken()

            elif self.atualIgual(tt.CTE):
                while (self.tokenAtual != tt.FECHARPAR or self.tokenAtual != tt.VIRG or
                       self.tokenAtual != tt.PVIRG or self.tokenAtual != tt.OPREL or
                       self.tokenAtual != tt.OPAD or self.tokenAtual != tt.OPMUL):
                    self.tokenAtual = self.lex.getToken()

            elif self.atualIgual(tt.FALSO):
                while (self.tokenAtual != tt.FECHARPAR or self.tokenAtual != tt.VIRG or
                       self.tokenAtual != tt.PVIRG or self.tokenAtual != tt.OPREL or
                       self.tokenAtual != tt.OPAD or self.tokenAtual != tt.OPMUL):
                    self.tokenAtual = self.lex.getToken()

            elif self.atualIgual(tt.OPNEG):
                while (self.tokenAtual != tt.FECHARPAR or self.tokenAtual != tt.VIRG or
                       self.tokenAtual != tt.PVIRG or self.tokenAtual != tt.OPREL or
                       self.tokenAtual != tt.OPAD or self.tokenAtual != tt.OPMUL):
                    self.tokenAtual = self.lex.getToken()

            elif self.atualIgual(tt.VERDADEIRO):
                while (self.tokenAtual != tt.FECHARPAR or self.tokenAtual != tt.VIRG or
                       self.tokenAtual != tt.PVIRG or self.tokenAtual != tt.OPREL or
                       self.tokenAtual != tt.OPAD or self.tokenAtual != tt.OPMUL):
                    self.tokenAtual = self.lex.getToken()

            elif self.atualIgual(tt.OPREL):
                while (self.tokenAtual != tt.FECHARPAR or self.tokenAtual != tt.VIRG or
                       self.tokenAtual != tt.PVIRG):
                    self.tokenAtual = self.lex.getToken()

            elif self.atualIgual(tt.OPAD):
                while (self.tokenAtual != tt.FECHARPAR or self.tokenAtual != tt.VIRG or
                       self.tokenAtual != tt.PVIRG or self.tokenAtual != tt.OPREL):
                    self.tokenAtual = self.lex.getToken()

            elif self.atualIgual(tt.OPMUL):
                while self.tokenAtual != tt.OPAD:
                    self.tokenAtual = self.lex.getToken()

            elif self.atualIgual(tt.OPNEG):  # Marcado
                pass   

"""
