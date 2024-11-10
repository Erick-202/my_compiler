import ply.lex as lex

tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_NUMBER = r'\d+'

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

# Test lexer
data = '3 + 4 -       5'
lexer.input(data)

for tok in lexer:
    print(tok)
