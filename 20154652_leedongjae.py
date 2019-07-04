import ply.lex as lex
import ply.yacc as yacc


include = 0
function = 0
variable = 0
condition = 0
loop = 0
called_function = 0

tokens = (
        'OPER', 'COMPARE', 'WORD', 'NUMBER', 'SENTENCE', 'EQUALS', 'LPAREN', 'RPAREN', 'SHOP', "DOT",
        'SEMICOLON', 'LBAR', 'RBAR', 'LBRACE', 'COPER', 'RBRACE', 'COMMA', 'UNARY', 'AND', 'BANG'
    )

# Tokens
t_BANG = r'!'
t_AND = r'&'
t_COMMA = r','
t_WORD = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SHOP = r'\#'
t_EQUALS = r'='
t_DOT = r'\.'
t_SEMICOLON = r';'
t_LBAR = r'\['
t_RBAR = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'


def t_UNARY(t):
    r'\+\+|--'
    return t
    
def t_SENTENCE(t):
    r'"[^\n]*?(?<!\\)"'
    return t

def t_NUMBER(t):
    r'0(?!\d)|([1-9]\d*)'
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_OPER(t):
    r'\+|-|\*|/|%'
    return t

def t_COMPARE(t):
    r'==|!=|<=|>=|<|>'
    return t

def t_COPER(t):
    r'&&|\|\|'
    return t

# Build the lexer
lexer = lex.lex()

# Parsing rules

# dictionary of WORDs
names = {}

def p_statement_include(t):
    '''statement : SHOP WORD COMPARE WORD DOT WORD COMPARE
                | SHOP WORD COMPARE WORD COMPARE'''
    global include
    include += 1

def p_statement_declared_function(t):
    '''statement : WORD WORD LPAREN  RPAREN LBRACE 
                | WORD WORD LPAREN WORD WORD COMMA WORD WORD RPAREN LBRACE
                | WORD WORD LPAREN WORD WORD RPAREN LBRACE
                | WORD WORD LPAREN WORD RPAREN LBRACE'''
    global function
    function += 1
    

def p_statement_declared_variable(t):
    '''statement : WORD WORD SEMICOLON
                | WORD WORD EQUALS NUMBER SEMICOLON
                | WORD WORD LBAR NUMBER RBAR SEMICOLON'''
    global variable
    variable += 1
    
def p_statement_conditional_statement(t):
    '''statement : WORD LPAREN WORD OPER WORD COMPARE NUMBER RPAREN LBRACE 
                | WORD LPAREN WORD COMPARE NUMBER RPAREN LBRACE
                | WORD LPAREN WORD COMPARE WORD RPAREN LBRACE
                | WORD LPAREN WORD COMPARE NUMBER COPER WORD COMPARE NUMBER RPAREN LBRACE'''
    global condition
    condition += 1

def p_statement_loop_statement(t):
    '''statement : WORD LPAREN WORD EQUALS NUMBER SEMICOLON WORD COMPARE NUMBER SEMICOLON WORD UNARY RPAREN LBRACE 
                | WORD LPAREN WORD EQUALS NUMBER SEMICOLON WORD COMPARE WORD SEMICOLON WORD UNARY RPAREN LBRACE
                | WORD LPAREN WORD EQUALS WORD OPER NUMBER SEMICOLON WORD COMPARE NUMBER SEMICOLON WORD UNARY RPAREN LBRACE
                | WORD LPAREN NUMBER RPAREN LBRACE'''
    global loop
    loop += 1

def p_statement_called_function(t):
    '''statement : WORD LPAREN SENTENCE RPAREN SEMICOLON
                 | WORD LPAREN SENTENCE COMMA AND WORD RPAREN SEMICOLON
                 | WORD LPAREN SENTENCE COMMA WORD COMMA WORD COMMA WORD OPER WORD RPAREN SEMICOLON
                 | WORD LPAREN SENTENCE COMMA WORD COMMA WORD COMMA LPAREN WORD OPER WORD RPAREN RPAREN SEMICOLON
                 | WORD LPAREN SENTENCE COMMA WORD LBAR WORD RBAR RPAREN SEMICOLON
                 | WORD LPAREN RPAREN SEMICOLON'''
    global called_function
    called_function += 1

def p_statement_double_called_function(t):
    'statement : WORD LPAREN SENTENCE COMMA WORD LPAREN WORD RPAREN RPAREN SEMICOLON'
    global called_function
    called_function += 2

def p_statement_function_and_variable(t):
    'statement : WORD WORD EQUALS WORD LPAREN WORD COMMA WORD RPAREN SEMICOLON'
    global variable
    global called_function
    variable += 1
    called_function +=1

def p_statement_garbage(t):
    '''statement :   WORD SEMICOLON
                   | RBRACE
                   | RBRACE WORD LBRACE
                   | WORD NUMBER SEMICOLON
                   | WORD WORD OPER WORD SEMICOLON
                   | WORD UNARY 
                   | WORD LBAR WORD RBAR EQUALS WORD LBAR WORD OPER NUMBER RBAR SEMICOLON
                   | WORD LBAR NUMBER RBAR EQUALS WORD SEMICOLON
                   | WORD LPAREN LPAREN WORD COMPARE NUMBER RPAREN COPER BANG LPAREN WORD AND LPAREN WORD OPER NUMBER RPAREN RPAREN RPAREN SEMICOLON
                   | WORD UNARY SEMICOLON'''

    
def p_error(t):
    print("Syntax error at '%s'" % t.value)

# Test it out
data = ''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)


parser = yacc.yacc()

# file input
path = input("Enter the file path: ")
file = open(path, 'r')
line = file.readlines()

# Tokenize
for i in line:
    if len(i)>2:
        parser.parse(i.strip('\n'))
        
# Use raw_input on Python 2

print("#include: ", include)
print("Declared Functions: ", function)
print("Declared Variables: ", variable)
print("Conditional statements: ", condition)
print("Loop: ", loop)
print("Called Functions: ", called_function)     
file.close()