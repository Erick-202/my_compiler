import lexical
import err
from tabulate import tabulate
 

file = "test/008_errors.txt"

def main():
    
    tokens,errores_lexicos = lexical.lexical_analysis(file)
    headers = ['Token', 'Type', 'Row', 'Column']
    #print(tabulate(tokens, headers=headers, tablefmt="grid"))
    errores =  (err.process_errors(errores_lexicos))
    
    headers = ['Line', 'Col', 'message', 'place']
    table_data = [
        [error['code'], error['line'], error['col'], error['message'],error['place']]
        for error in errores
    ]
    
    
    if not table_data:
        print("Todo gucci")
    else:
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        tabla_errores = err.extract_error_lines(file,errores)

        for detail in tabla_errores:
            print(f"{detail['content']}")
            print(" " * (detail['column'] - 1) + "^")
            print(f"Mensaje: {detail['message']}")



    

main()