usuario = {}

def registrar_usuario():
    nombre = input("ingrese su nombre de su usuario")
    clave = input("ingrese su contraseña")

    usuario[nombre] = clave
    print("usuario registrado con exito")

def iniciar_seccion():
    nombre = input("ingrese su nombre de su usuario")
    clave = input("ingrese su contraseña")

    if nombre in usuario and usuario[nombre] == clave:
        print("¡Bienvenidos al sistema!")
    else:
        print("usuario o contraseña incorrecta")
  
