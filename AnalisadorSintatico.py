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
from AnalisadorLexico import TipoToken as tt, Lexico


# Classe principal do analisador sintatico
class Sintatico:

    def __init__(self):
        self.lex = None
        self.tokenAtual = None

    def interprete(self, nomeArquivo):
        if not self.lex is None:
            print('ERRO: Já existe um arquivo sendo processado.')
        else:
            self.lex = Lexico(nomeArquivo)
            self.lex.abreArquivo()
            self.tokenAtual = self.lex.getToken()

            self.A()
            # Talvez pode ser retirado
            # self.consome(tt.FIMARQ)

            self.lex.fechaArquivo()

    def atualIgual(self, token):
        (const, msg) = token
        return self.tokenAtual.const == const

    def consome(self, token):
        if self.atualIgual(token):
            self.tokenAtual = self.lex.getToken()
        else:
            (const, msg) = token
            print('ERRO DE SINTAXE [linha %d]: era esperado "%s" mas foi recebido "%s"'
                  % (self.tokenAtual.linha, msg, self.tokenAtual.lexema))
            quit()

    def A(self):
        self.PROG()
        self.consome(tt.FIMARQ)

    def PROG(self):
        self.consome(tt.PROGRAMA)
        self.consome(tt.ID)
        self.consome(tt.PVIRG)
        self.DECLS()
        self.C_COMP()

    def DECLS(self):
        if self.atualIgual(tt.VARIAVEIS):
            self.consome(tt.VARIAVEIS)
            self.LIST_DECLS()
        else:
            pass

    def LIST_DECLS(self):
        self.DECL_TIPO()
        self.D()

    def D(self):
        if self.atualIgual(tt.ID):
            self.LIST_DECLS()
        else:
            pass

        # if self.atualIgual(tt.FIMARQ):
        #   pass
        # else:
        #   self.LIST_DECLS()

    def DECL_TIPO(self):
        self.LIST_ID()
        self.consome(tt.DPONTOS)
        self.TIPO()
        self.consome(tt.PVIRG)

    def LIST_ID(self):
        self.consome(tt.ID)
        self.E()

    def E(self):
        if self.atualIgual(tt.VIRG):
            self.consome(tt.VIRG)
            self.LIST_ID()
        else:
            pass

    def TIPO(self):
        if self.atualIgual(tt.INTEIRO):
            self.consome(tt.INTEIRO)
        elif self.atualIgual(tt.REAL):
            self.consome(tt.REAL)
        elif self.atualIgual(tt.LOGICO):
            self.consome(tt.LOGICO)
        elif self.atualIgual(tt.CARACTER):
            self.consome(tt.CARACTER)

    def C_COMP(self):
        self.consome(tt.ABRECH)
        self.LISTA_COMANDOS()
        self.consome(tt.FECHACH)

    def LISTA_COMANDOS(self):
        self.COMANDOS()
        self.G()

    def G(self):

        if self.atualIgual(tt.SE) or self.atualIgual(tt.ENQUANTO) or self.atualIgual(tt.LEIA) or self.atualIgual(
                tt.ESCREVA) or self.atualIgual(tt.ID):  ##########
            self.LISTA_COMANDOS()
        else:
            pass

        # if self.atualIgual(tt.FIMARQ):
        #    pass
        # else:
        #    self.LISTA_COMANDOS()

    def COMANDOS(self):
        if self.atualIgual(tt.SE):
            self.IF()
        elif self.atualIgual(tt.ENQUANTO):
            self.WHILE()
        elif self.atualIgual(tt.LEIA):
            self.READ()
        elif self.atualIgual(tt.ESCREVA):
            self.WRITE()
        elif self.atualIgual(tt.ID):  #######3
            self.ATRIB()

    def IF(self):
        self.consome(tt.SE)
        self.consome(tt.ABREPAR)
        self.EXPR()
        self.consome(tt.FECHARPAR)
        self.C_COMP()
        self.H()

    def H(self):
        if self.atualIgual(tt.SENAO):
            self.consome(tt.SENAO)
            self.C_COMP()
        else:
            pass

    def WHILE(self):
        self.consome(tt.ENQUANTO)
        self.consome(tt.ABREPAR)
        self.EXPR()
        self.consome(tt.FECHARPAR)
        self.C_COMP()

    def READ(self):
        self.consome(tt.LEIA)
        self.consome(tt.ABREPAR)
        self.LIST_ID()
        self.consome(tt.FECHARPAR)
        self.consome(tt.PVIRG)

    def ATRIB(self):
        self.consome(tt.ID)
        self.consome(tt.ATRIB)
        self.EXPR()
        self.consome(tt.PVIRG)

    def WRITE(self):
        self.consome(tt.ESCREVA)
        self.consome(tt.ABREPAR)
        self.LIST_W()
        self.consome(tt.FECHARPAR)
        self.consome(tt.PVIRG)

    def LIST_W(self):
        self.ELEM_W()
        self.L()

    def L(self):
        if self.atualIgual(tt.VIRG):
            self.consome(tt.VIRG)
            self.LIST_W()
        else:
            pass

    def ELEM_W(self):
        if self.atualIgual(tt.CADEIA):
            self.consome(tt.CADEIA)
        else:
            self.EXPR()

    def EXPR(self):
        self.SIMPLES()
        self.P()

    def P(self):
        if self.atualIgual(tt.OPREL):
            self.consome(tt.OPREL)
            self.SIMPLES()
        else:
            pass

    def SIMPLES(self):
        self.TERMO()
        self.R()

    def R(self):
        if self.atualIgual(tt.OPAD):
            self.consome(tt.OPAD)
            self.SIMPLES()
        else:
            pass

    def TERMO(self):
        self.FAT()
        self.S()

    def S(self):
        if self.atualIgual(tt.OPMUL):
            self.consome(tt.OPMUL)
            self.TERMO()
        else:
            pass

    def FAT(self):
        if self.atualIgual(tt.ID):
            self.consome(tt.ID)
        elif self.atualIgual(tt.CTE):
            self.consome(tt.CTE)
        elif self.atualIgual(tt.ABREPAR):
            self.consome(tt.ABREPAR)
            self.EXPR()
            self.consome(tt.FECHARPAR)
        elif self.atualIgual(tt.VERDADEIRO):
            self.consome(tt.VERDADEIRO)
        elif self.atualIgual(tt.FALSO):
            self.consome(tt.FALSO)
        elif self.atualIgual(tt.OPNEG):
            self.consome(tt.OPNEG)
            self.FAT()


if __name__ == "__main__":
    nome = "exemplo10.txt"

    parser = Sintatico()
    parser.interprete(nome)
