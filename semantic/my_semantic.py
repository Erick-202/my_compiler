from semantic.executer import Executer


def my_semantic(three):

    executer = Executer()
    #print("RESULTADO EXECUTER: "+ str(three))
    #print("RESULTADO FINAL "+ str(executer.operation(three.nodo)))
    res = executer.operation(three.nodo)
    message = None
    errores_semantico = executer.executer_errors

    if errores_semantico:
        message = errores_semantico
        print(message)
    
    return res, message