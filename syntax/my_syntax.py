from syntax.parser_1 import Parser  
from syntax.executer import Executer
 
#file = "test/010_goodboy.txt"

def my_syntax(tokens):
        
    ################################################################3
    parser = Parser(tokens)
    three,syntax_errors = parser.parse()
    print( three)
    if syntax_errors:
        print (syntax_errors)
    ################################################################3
    else:
        executer = Executer()
        print(three)
        print(executer.operation(three.nodo))
        errores_semantico = executer.executer_errors
        for name, symbol in executer.symboltable.symbol.items():
            print(f"Variable: {name}, Type: {symbol['type']}, Value: {symbol['value']}")

        print(errores_semantico)



