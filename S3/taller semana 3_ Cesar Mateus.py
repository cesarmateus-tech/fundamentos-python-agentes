import datetime ### librería para obtener la fecha actual
from ast import Dict, List ### Importa las clases Dict y List del módulo ast para definir tipos de datos personalizados.
usuario_inv="invitado"
usuario_admin = "admin"
pass_inv="12345678"
pass_admin="abcdefgh"
error_sesion=0
sistema_activo = True
memoria=dict[str, str]
historial_chat: memoria = []
mensaje= ""

### Función para gestionar el historial de comandos ingresados por el usuario, permitiendo buscar palabras clave en las descripciones del historial.
def gest_Historial(accion: str, historial: historial_chat)-> str:
    """realiza acciones relacionadas con el historial de comandos, como limpiar el historial, mostrar todo el historial o buscar palabras clave en las descripciones del historial."""
    if cmd=="historial_clear":
        historial.clear()
        return "Historial de comandos eliminado"
    if cmd=="historial_all":
        return f"Historial de comandos: {str(historial)}"
    if cmd == "historial":
                pal_busq = input ("Ingrese la palabra a buscar en el historial:  ").lower()
                coinc = [] ### Lista para almacenar las coincidencias encontradas
                for pal_en in historial_chat:
                ### Busca la palabra ingresada por el usuario en la desscripcion del historial guardado
                    if pal_busq in pal_en["Descripción"].lower():
                        ### Si encuentra coincidencia, muestra el usuario y la descripción
                        coinc.append((pal_en['Usuario'], pal_en['Descripción']))
                ### Muestra las coincidencias encontradas
                if coinc:
                    return "\n".join(f"{usuario}: {descripcion}" for usuario, descripcion in coinc)#### Si no se encuentran coincidencias, muestra un mensaje indicando que no se encontraron resultados para la palabra buscada.
                else:
                    return f"No se encontró coincidencias para la palabra '{pal_busq}' en el historial de comandos.\n\n"


def calculadora(num1: float, num2: float, op: str)-> float:
    """Realiza una operación matemática básica entre dos números."""
    if op == "+": return num1 + num2
    if op == "-": return num1 - num2
    if op == "*": return num1 * num2
    if op == "/":
        if num2 != 0:
            return num1 / num2
        else:
            raise ZeroDivisionError("Error: No es posible dividir por 0")
    raise ValueError(f"Operador '{op}' no es válido.")

def obtener_fecha(rol: str)-> str:
    """Retorna la fecha si el rol es administrador, de lo contrario retorna un mensaje de acceso denegado."""
    if rol == "Administrador":
        fecha_actual= datetime.datetime.now()
        formato_fecha = fecha_actual.strftime("%d-%m-%Y %H:%M:%S")
        return (f"La fecha de hoy es: {formato_fecha}\n\n")
    else:
        raise PermissionError("Acceso denegado. Solo los administradores pueden ver la fecha.")
    
def validar_pass(pass_actual: str, nueva_pass: str, pass_sesion: str, usuario_sesion: str)-> str:
    """Valida la contraseña actual y actualiza a una nueva contraseña si se cumplen los criterios de seguridad."""
    if pass_sesion != pass_actual:
        raise PermissionError("Contraseña actual incorrecta. No se pudo actualizar la contraseña.") 
    
    if len(nueva_pass) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres.")
    if nueva_pass == pass_actual:
        raise ValueError("La nueva contraseña no puede ser igual a la contraseña actual.")
    if nueva_pass == usuario_sesion:
        raise ValueError("La contraseña no puede ser igual al nombre de usuario.")
       
    return nueva_pass

def contar(palabra: str)-> Dict[str, int]:
    """Cuenta el número de vocales, consonantes y letras totales en una palabra dada."""
    tot_letras = len(palabra)
    tot_vocales= sum(1 for p in palabra if p in "aeiou")
    tot_cons= tot_letras - tot_vocales
    return {
        "Total de vocales": tot_vocales,
        "Total de consonantes": tot_cons,
        "Total de letras": tot_letras
    }

### Controla la sesión del usuario, permitiendo 3 intentos para ingresar las credenciales correctas.
while error_sesion <3 and sistema_activo:
    user_sesion= input("Ingrese su usuario: ").lower()
    pass_sesion= input("Ingrese su Contraseña: ")
### Verifica si las credenciales ingresadas corresponden a un usuario invitado o administrador, y otorga acceso al sistema.
    if (user_sesion == usuario_inv and pass_sesion == pass_inv) or (user_sesion == usuario_admin and pass_sesion == pass_admin):
        ### Valida el rol con el que el usuario ingresó
        if user_sesion == usuario_inv:
            print("Acceso concedido como Invitado")
            rol= "Invitado"
        elif user_sesion == usuario_admin:
            print ("Acceso concedido como Administrador")
            rol= "Administrador"
        while sistema_activo:
            ###muestra un menu de opciones disponibles para el usuario.
            print ("\n")
            cmd = input (
"""Agente> :
* ping
* contar
* fecha_hoy
* validar_pass
* calculadora
* Historial
* Historial_all
* Historial_clear
* salir \n\n""").lower()

            ### Ejecuta el comando ingresado por el usuario, realizando la acción correspondiente según el comando y el rol del usuario, y registra cada acción en el historial de comandos con una descripción detallada.
            try:
                if cmd == "salir":
                    print("■■■■■☻■■■■■  Agente Apagado  ■■■■■☻■■■■■")
                    sistema_activo= False
                elif cmd == "ping":
                        print ("pong")
                        mensaje = f"{rol}, ha pedido ping, para recibir un pong."
                elif cmd == "contar":
                    resultado_contar= contar(input("Ingrese la palabra a contar: "))
                    tot_vocales= resultado_contar["Total de vocales"]
                    tot_cons= resultado_contar["Total de consonantes"]
                    print (f"En la palabra ingresada hay {tot_vocales} vocales, {tot_cons} consonantes, y un total de {tot_vocales + tot_cons} letras.") 
                    mensaje = f"""{rol}, ha solicitado contar letras de la palabra {resultado_contar}.
                    El resultado fue: {tot_vocales} vocales, {tot_cons} consonantes, y un total de {tot_vocales + tot_cons} letras."""
                ### El comando "fecha_hoy" muestra la fecha y hora actual, pero solo si el usuario tiene rol de administrador.
                elif cmd == "fecha_hoy":
                    resultado_fecha= obtener_fecha(rol)
                    print (resultado_fecha)
                    if rol == "Administrador":
                        mensaje = f"{rol}, ha solicitado la fecha de hoy {resultado_fecha}."
                    else:
                        mensaje = f"{rol}, ha solicitado la fecha de hoy sin tener los privilegios necesarios."
                ### El comando "validar_pass" permite a los usuarios cambiar su contraseña, despues de confirmar la contraseña actual correctamente y deben cumplir con ciertos criterios para la nueva contraseña.
                elif cmd == "validar_pass":
                    if rol == "Invitado":
                        user_sesion = usuario_inv
                        pass_sesion= pass_inv
                    elif rol == "Administrador":
                        user_sesion = usuario_admin
                        pass_sesion= pass_admin
                    pass_ingresada= input("Ingrese su Contraseña actual: ")
                    if pass_ingresada != pass_sesion:
                        print (f"Contraseña actual incorrecta. No se pudo actualizar la contraseña.")
                        mensaje = f"{rol}, ha intentado cambiar su contraseña pero ingresó la contraseña actual incorrecta."
                    else:
                        nueva_pass= input("Ingrese su nueva contraseña: ")
                        resultado_validar_pass= validar_pass(pass_sesion, nueva_pass, pass_ingresada, user_sesion)
                        if rol == "Invitado":
                            pass_inv= nueva_pass
                        else:
                            pass_admin= nueva_pass
                        print ("Contraseña actualizada exitosamente.")
                        mensaje = f"{rol}, ha solicitado validar pass."
                elif cmd == "calculadora":
                    ### Se solicita al usuario ingresar dos numeros y un operador para que el sistema realice la operación correspondiente, manejando casos de división por cero.
                    num_1= float(input("Ingrese primer número: "))
                    op= input("Ingresa el operador (+, -, *, /): ")
                    num_2= float(input("Ingrese segundo número: "))              
                    resultado_calculadora= calculadora(num_1, num_2, op)
                    print (f"El resultado de {num_1} {op} {num_2} es: {resultado_calculadora}")
                    mensaje = f"""{rol}, ha solicitado operación Matematica. 
                    Los datos ingresados fueron: {num_1} {op} {num_2}.
                    El resultado de la operación fue: {resultado_calculadora}."""
                elif cmd in ["historial_clear", "historial_all", "historial"]:
                    if cmd=="historial":
                        resultado_hist= gest_Historial(cmd, historial_chat)
                    else:
                        resultado_hist= gest_Historial(cmd, historial_chat)
                    print (resultado_hist)
                    mensaje = f"{rol}, ha solicitado {cmd}."
                else:
                    print("--- Comando desconocido. Intente de nuevo\n\n")
            
                d_log = {"Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                        "Usuario": rol, 
                        "Comando": cmd, 
                        "Descripción": mensaje}
                historial_chat.append(d_log)
                print (historial_chat)
            
            except PermissionError as e:
                print(f"Error de seguridad: {e}")
            except ZeroDivisionError as e:
                print(f"Error Matemático: {e}")
            except ValueError as e:
                print(f"Error de dato inválido: {e}")
            except Exception as e:
                print(f"Error inesperado: {e}")
            
    ### Si las credenciales ingresadas son incorrectas, incrementa el contador de errores y muestra el número de intentos restantes. Si se alcanzan los 3 intentos, bloquea al usuario y cierra el sistema.
    else:
        print ("Usuario y/o contraseña erronea\n\n")
        error_sesion +=1
        intentos = 3 - error_sesion
        if intentos >0:
            print (f"Intentelo de nuevo. Quedan {intentos} intentos \n")
        else:
            print ("■■■■■■    Usuario Bloqueado. Cerrando Sistema     ■■■■■■")